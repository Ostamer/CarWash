from django.contrib import admin
from .models import (
    Car, CarColor, CarType,
    CarWash, CarWashWorkDay, CarWashWorkTime,
    Service, User, UserRole, WashRecord, WashRecordService, Worker, WorkerWorkDay
)
from django.core.exceptions import ValidationError


@admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(CarColor)
class CarColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'value', 'name')


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'gos_number', 'gos_region', 'model', 'user')
    search_fields = ('gos_number',)

    def save_model(self, request, obj, form, change):
        gos_number = form.cleaned_data.get('gos_number')
        gos_region = form.cleaned_data.get('gos_region')

        if gos_number and gos_region:
            car_exists = Car.objects.filter(gos_number=gos_number, gos_region=gos_region)

            if change:
                car_exists = car_exists.exclude(pk=obj.pk)

            if car_exists.exists():
                raise ValidationError("Машина с таким номером и регионом уже существует.")

        super().save_model(request, obj, form, change)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'role')
    search_fields = ('role',)


@admin.register(CarWash)
class CarWashAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'phone_number', 'lattitude_coordinate', 'longitude_coordinate')
    search_fields = ('name', 'address')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'car_wash', 'service_type')
    search_fields = ('name',)
    list_filter = ('service_type',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', "auth_user_id")


@admin.register(CarWashWorkDay)
class CarWashWorkDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'car_wash', 'date', 'started_at', 'ended_at')
    search_fields = ('car_wash__name', 'date')

    def save_model(self, request, obj, form, change):
        if obj.car_wash and obj.date and (not obj.started_at or not obj.ended_at):
            day_of_week = obj.date.strftime('%a').lower()[:3]
            work_time = CarWashWorkTime.objects.filter(car_wash=obj.car_wash, day=day_of_week).first()

            if work_time:
                obj.started_at = work_time.time_from
                obj.ended_at = work_time.time_to

        super().save_model(request, obj, form, change)


@admin.register(CarWashWorkTime)
class CarWashWorkTimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'car_wash', 'day', 'time_from', 'time_to')
    search_fields = ('car_wash__name', 'day')
    list_filter = ('day',)


class WashRecordServiceInline(admin.TabularInline):
    model = WashRecordService
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "service":
            if request.resolver_match.kwargs.get('object_id'):
                obj_id = request.resolver_match.kwargs.get('object_id')
                obj = WashRecord.objects.get(pk=obj_id)
                kwargs["queryset"] = Service.objects.filter(car_wash=obj.car_wash)
            else:
                kwargs["queryset"] = Service.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(WashRecord)
class WashRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'client', 'worker', 'ordered_at', 'started_at', 'finished_at', 'total_price', 'car_wash')
    search_fields = ('car__gos_number', 'user__auth_user_id')
    inlines = [WashRecordServiceInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('total_price',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        total_price = sum(service.service.price for service in obj.washrecordservice_set.all())
        obj.total_price = total_price
        obj.save(update_fields=['total_price'])


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('id', 'car_wash', 'user_id', 'gat_at', 'fired_at')
    search_fields = ('user_id', 'car_wash__name')


@admin.register(WorkerWorkDay)
class WorkerWorkDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'worker', 'started_at', 'ended_at')