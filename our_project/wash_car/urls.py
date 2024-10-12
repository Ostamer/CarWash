from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarWashViewSet, CarWashDetailView, CarWashServiceListView, ServiceListView,\
    ServiceDetailView, CarTypeListView, CarColorListView, CarWashAvailableTimeView, UserMeView, \
    CarListView, CarDetailView, WashRecordViewSet, CarWashRecordView, WorkerWorkDayListView,\
    CarWashWorkDayViewSet, CarWashWorkTimeViewSet, UserCarsView

from .yasg import urlpatterns as doc_url

router = DefaultRouter()
router.register(r'wash-record', WashRecordViewSet, basename='wash-record')
router.register(r'car-wash-work-day', CarWashWorkDayViewSet, basename='car-wash-work-day')
router.register(r'car-wash-work-time', CarWashWorkTimeViewSet, basename='car-wash-work-time')

urlpatterns = [
    path('car-wash/', CarWashViewSet.as_view(), name='car-wash-list'),
    path('car-wash/<int:car_wash_id>/', CarWashDetailView.as_view(), name='car-wash-detail'),
    path('car-wash/<int:car_wash_id>/service/', CarWashServiceListView.as_view(), name='car-wash-service-list'),
    path('car-wash/<int:car_wash_id>/available-times/', CarWashAvailableTimeView.as_view(), name='car-wash-available-time'),
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('services/<int:service_id>/', ServiceDetailView.as_view(), name='service-detail'),
    path('car-types/', CarTypeListView.as_view(), name='car-type-list'),
    path('car-colors/', CarColorListView.as_view(), name='car-color-list'),
    path('user/me/', UserMeView.as_view(), name='user-me'),
    path('car/', CarListView.as_view(), name='car-list'),
    path('car/<int:car_id>/', CarDetailView.as_view(), name='car-detail'),
    path('user/<int:user_id>/cars/', UserCarsView.as_view(), name='user-cars'),
    path('car-wash/<int:car_wash_id>/wash-records/', CarWashRecordView.as_view(), name='car-wash-record'),
    path('worker-work-day/', WorkerWorkDayListView.as_view(), name='worker-work-day'),
    path('', include(router.urls)),
]

urlpatterns += doc_url