from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('wash_car.urls')),
    path('', include('wash_car.yasg'))
]
