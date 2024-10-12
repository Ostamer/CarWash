from rest_framework import serializers
from .models import Car, CarColor, CarType, CarWash, Service, User, UserRole, WashRecord, WorkerWorkDay, \
    WashRecordService, CarWashWorkTime, CarWashWorkDay, Worker
from datetime import datetime
from .WashRecordAlgoritm import get_available_worker


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

    def validate(self, data):
        gos_number = data.get('gos_number')
        gos_region = data.get('gos_region')

        if gos_number and gos_region:
            car_exists = Car.objects.filter(gos_number=gos_number, gos_region=gos_region).exists()

            if car_exists:
                raise serializers.ValidationError("Машина с таким номером и регионом уже существует.")

        return data


class CarColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarColor
        fields = '__all__'


class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = '__all__'


class CarWashSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarWash
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    user_role = serializers.PrimaryKeyRelatedField(queryset=UserRole.objects.all(), write_only=True)
    user_role_display = serializers.CharField(source='user_role.role', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'auth_user_id', 'user_role', 'user_role_display']


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'price', 'service_type']


class WashRecordServiceSerializer(serializers.ModelSerializer):
    service_id = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), source='service', write_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = WashRecordService
        fields = ['id', 'service', 'service_id']


class WashRecordSerializer(serializers.ModelSerializer):
    service_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=True
    )
    services = WashRecordServiceSerializer(source='washrecordservice_set', many=True, read_only=True)

    class Meta:
        model = WashRecord
        fields = ['id', 'car', 'services', 'car_wash', 'ordered_at', 'car_wash_work_day', 'service_ids']

    def validate_service_ids(self, service_ids):
        if not service_ids:
            raise serializers.ValidationError("Необходимо выбрать хотя бы одну услугу.")

        primary_services = Service.objects.filter(id__in=service_ids, service_type='основная')
        if primary_services.count() > 1:
            raise serializers.ValidationError("Может быть выбрана только одна основная услуга.")

        return service_ids

    def get_car_wash_work_day(self, car_wash, ordered_at):
        current_date = datetime.combine(datetime.today(), ordered_at).date()
        return CarWashWorkDay.objects.filter(
            car_wash=car_wash,
            date=current_date
        ).first()

    def create(self, validated_data):
        service_ids = validated_data.pop('service_ids')
        services = Service.objects.filter(id__in=service_ids)
        car = validated_data.get('car')
        car_wash = validated_data.get('car_wash')
        ordered_at = validated_data.get('ordered_at', datetime.now().time())
        current_date = datetime.today().date()

        car_wash_work_day = self.get_car_wash_work_day(car_wash, ordered_at)
        if not car_wash_work_day:
            raise serializers.ValidationError("Нет рабочего дня для указанного времени.")

        worker = get_available_worker(car_wash, current_date, ordered_at)
        if not worker:
            raise serializers.ValidationError("Нет доступных мойщиков на выбранное время.")

        wash_record = WashRecord.objects.create(
            car=car,
            client=None,
            car_wash=car_wash,
            total_price=0,
            worker=worker,
            ordered_at=ordered_at,
            started_at=None,
            finished_at=None,
            car_wash_work_day=car_wash_work_day
        )

        total_price = 0
        for service in services:
            WashRecordService.objects.create(wash_record=wash_record, service=service)
            total_price += service.price

        wash_record.total_price = total_price
        wash_record.save(update_fields=['total_price'])

        return wash_record

    def update(self, instance, validated_data):
        service_ids = validated_data.pop('service_ids', None)
        if service_ids:
            services = Service.objects.filter(id__in=service_ids)
        else:
            services = instance.washrecordservice_set.all()

        instance.car_wash_work_day = validated_data.get('car_wash_work_day', instance.car_wash_work_day)
        instance.car = validated_data.get('car', instance.car)
        instance.client = validated_data.get('client', instance.client)
        instance.car_wash = validated_data.get('car_wash', instance.car_wash)
        instance.ordered_at = validated_data.get('ordered_at', instance.ordered_at)
        instance.worker = validated_data.get('worker', instance.worker)
        instance.started_at = validated_data.get('started_at', instance.started_at)
        instance.finished_at = validated_data.get('finished_at', instance.finished_at)
        car_wash = validated_data.get('car_wash', instance.car_wash)
        ordered_at = validated_data.get('ordered_at', instance.ordered_at)
        car_wash_work_day = self.get_car_wash_work_day(car_wash, ordered_at)
        if car_wash_work_day:
            instance.car_wash_work_day = car_wash_work_day

        instance.save()

        existing_services = {s.service.id: s for s in instance.washrecordservice_set.all()}
        new_services_ids = [s.id for s in services]

        for service_id in list(existing_services.keys()):
            if service_id not in new_services_ids:
                existing_services[service_id].delete()

        for service in services:
            if service.id not in existing_services:
                WashRecordService.objects.create(wash_record=instance, service=service)

        total_price = sum(service.price for service in instance.washrecordservice_set.all())
        instance.total_price = total_price
        instance.save(update_fields=['total_price'])

        return instance


class CarWashWorkTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarWashWorkTime
        fields = '__all__'

    def validate(self, data):
        car_wash = data.get('car_wash')
        day = data.get('day')

        if CarWashWorkTime.objects.filter(car_wash=car_wash, day=day).exists():
            raise serializers.ValidationError(f"Для автомойки'{car_wash}', график работы на '{day}' уже существует")

        return data


class CarWashWorkDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarWashWorkDay
        fields = '__all__'

    def validate(self, data):
        car_wash = data.get('car_wash')
        date = data.get('date')

        if CarWashWorkDay.objects.filter(car_wash=car_wash, date=date).exists():
            raise serializers.ValidationError(f"Для автомойки '{car_wash}', время работы на дату '{date}' уже существует")

        if car_wash and date and (not data.get('started_at') or not data.get('ended_at')):
            day_of_week = date.strftime('%a').lower()[:2]
            work_time = CarWashWorkTime.objects.filter(car_wash=car_wash, day=day_of_week).first()

            if work_time:
                data['started_at'] = work_time.time_from
                data['ended_at'] = work_time.time_to

        return data


class UserCarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

    def validate(self, data):
        user_id = data.get('user_id')

        result = Car.objects.filter(user=user_id).exists()
        return result


class WorkerWorkDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerWorkDay
        fields = '__all__'


class WorkerSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Worker
        fields = ['id', 'car_wash', 'user', 'user_name', 'gat_at', 'fired_at']
