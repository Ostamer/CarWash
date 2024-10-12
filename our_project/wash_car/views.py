from rest_framework import generics, status
from rest_framework.response import Response
from .models import Car, CarColor, CarType, CarWash, Service, User, WashRecord, WorkerWorkDay, CarWashWorkDay,\
    CarWashWorkTime
from .serializers import CarSerializer, CarColorSerializer, CarTypeSerializer, CarWashSerializer, ServiceSerializer,\
    UserSerializer, WashRecordSerializer, WorkerWorkDaySerializer, CarWashWorkDaySerializer, CarWashWorkTimeSerializer,\
    UserCarsSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from .WashRecordAlgoritm import get_available_time_slots_for_week
from django.shortcuts import get_object_or_404


class CarWashAvailableTimeView(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        car_wash_id = self.kwargs.get('car_wash_id')
        car_wash = get_object_or_404(CarWash, id=car_wash_id)
        available_slots_for_week = get_available_time_slots_for_week(car_wash)
        available_times = {
            car_wash.id: available_slots_for_week
        }
        return Response(available_times)


class CarWashViewSet(generics.ListAPIView):
    queryset = CarWash.objects.all()
    serializer_class = CarWashSerializer


class CarWashDetailView(generics.RetrieveAPIView):
    queryset = CarWash.objects.all()
    serializer_class = CarWashSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'car_wash_id'


class CarWashServiceListView(generics.ListAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        car_wash_id = self.kwargs['car_wash_id']
        return Service.objects.filter(car_wash_id=car_wash_id)


class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceDetailView(generics.RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'service_id'


class CarTypeListView(generics.ListAPIView):
    queryset = CarType.objects.all()
    serializer_class = CarTypeSerializer


class CarColorListView(generics.ListAPIView):
    queryset = CarColor.objects.all()
    serializer_class = CarColorSerializer


class UserMeView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCarsView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = UserCarsSerializer


class CarWashRecordView(generics.ListAPIView):
    serializer_class = WashRecordSerializer

    def get_queryset(self):
        car_wash_id = self.kwargs.get('car_wash_id')
        if car_wash_id:
            return WashRecord.objects.filter(car_wash_id=car_wash_id)
        return WashRecord.objects.none()


class CarListView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def perform_create(self, serializer):
        serializer.save()


class WorkerWorkDayListView(generics.ListCreateAPIView):
    queryset = WorkerWorkDay.objects.all()
    serializer_class = WorkerWorkDaySerializer

    def perform_create(self, serializer):
        serializer.save()


class CarDetailView(generics.RetrieveUpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'car_id'


class CarWashWorkDayViewSet(viewsets.ModelViewSet):
    queryset = CarWashWorkDay.objects.all()
    serializer_class = CarWashWorkDaySerializer


class CarWashWorkTimeViewSet(viewsets.ModelViewSet):
    queryset = CarWashWorkTime.objects.all()
    serializer_class = CarWashWorkTimeSerializer


class WashRecordViewSet(viewsets.ModelViewSet):
    queryset = WashRecord.objects.all()
    serializer_class = WashRecordSerializer

    @action(detail=False, methods=['post'], url_path='', url_name='create_wash_record')
    def create_wash_record(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            wash_record = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

