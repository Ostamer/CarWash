# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Car(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    car_color = models.ForeignKey('CarColor', models.DO_NOTHING, blank=True, null=True)
    car_type = models.ForeignKey('CarType', models.DO_NOTHING, blank=True, null=True)
    gos_number = models.TextField(blank=True, null=True)
    gos_region = models.IntegerField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'car'


class CarColor(models.Model):
    value = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'car_color'


class CarType(models.Model):
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'car_type'


class CarWash(models.Model):
    name = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.TextField(blank=True, null=True)
    lattitude_coordinate = models.TextField(blank=True, null=True)
    longitude_coordinate = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'car_wash'


class CarWashWorkDay(models.Model):
    car_wash = models.ForeignKey(CarWash, models.DO_NOTHING, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    started_at = models.TimeField(blank=True, null=True)
    ended_at = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'car_wash_work_day'


class CarWashWorkTime(models.Model):
    car_wash = models.ForeignKey(CarWash, models.DO_NOTHING, blank=True, null=True)
    day = models.TextField(blank=True, null=True)
    time_from = models.TimeField(blank=True, null=True)
    time_to = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'car_wash_work_time'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Service(models.Model):
    car_wash = models.ForeignKey(CarWash, models.DO_NOTHING, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    car_type = models.ForeignKey(CarType, models.DO_NOTHING, blank=True, null=True)
    service_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service'


class User(models.Model):
    user_role = models.ForeignKey('UserRole', models.DO_NOTHING, blank=True, null=True)
    auth_user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class UserRole(models.Model):
    role = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_role'


class WashRecord(models.Model):
    car = models.ForeignKey(Car, models.DO_NOTHING, blank=True, null=True)
    client = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    car_wash = models.ForeignKey(CarWash, models.DO_NOTHING, blank=True, null=True)
    total_price = models.IntegerField(blank=True, null=True)
    worker = models.ForeignKey('Worker', models.DO_NOTHING, blank=True, null=True)
    car_wash_work_day = models.ForeignKey(CarWashWorkDay, models.DO_NOTHING, blank=True, null=True)
    ordered_at = models.TimeField(blank=True, null=True)
    started_at = models.TimeField(blank=True, null=True)
    finished_at = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wash_record'


class WashRecordService(models.Model):
    wash_record = models.ForeignKey(WashRecord, models.DO_NOTHING, blank=True, null=True)
    service = models.ForeignKey(Service, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wash_record_service'


class Worker(models.Model):
    car_wash = models.ForeignKey(CarWash, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    gat_at = models.DateField(blank=True, null=True)
    fired_at = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'worker'


class WorkerWorkDay(models.Model):
    started_at = models.TimeField(blank=True, null=True)
    ended_at = models.TimeField(blank=True, null=True)
    worker = models.ForeignKey(Worker, models.DO_NOTHING, blank=True, null=True)
    car_wash_work_day = models.ForeignKey(CarWashWorkDay, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'worker_work_day'
