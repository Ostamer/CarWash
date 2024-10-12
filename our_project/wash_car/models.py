from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.CASCADE)
    permission = models.ForeignKey('AuthPermission', models.CASCADE)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.CASCADE)
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
    user = models.ForeignKey(AuthUser, models.CASCADE)
    group = models.ForeignKey(AuthGroup, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.CASCADE)
    permission = models.ForeignKey(AuthPermission, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Car(models.Model):
    user = models.ForeignKey('User', models.CASCADE, blank=True, null=True)
    car_color = models.ForeignKey('CarColor', models.SET_NULL, blank=True, null=True)
    car_type = models.ForeignKey('CarType', models.SET_NULL, blank=True, null=True)
    gos_number = models.CharField(max_length=20, blank=True, null=True)
    gos_region = models.IntegerField(blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'car'

    def __str__(self):
        return f"{self.car_color.name} {self.car_type.name} {self.gos_number} {self.gos_region}" or ""


class CarColor(models.Model):
    value = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'car_color'

    def __str__(self):
        return self.name or ""


class CarType(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'car_type'

    def __str__(self):
        return self.name or ""


class CarWash(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    lattitude_coordinate = models.TextField(blank=True, null=True)
    longitude_coordinate = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'car_wash'

    def __str__(self):
        return self.name


class CarWashWorkDay(models.Model):
    car_wash = models.ForeignKey(CarWash, models.DO_NOTHING, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    started_at = models.TimeField(blank=True, null=True)
    ended_at = models.TimeField(blank=True, null=True)

    class Meta:
        db_table = 'car_wash_work_day'

    def __str__(self):
        return f"{self.date}. {self.started_at}-{self.ended_at}"


class CarWashWorkTime(models.Model):
    DAYS_OF_WEEK = [
        ('mon', 'Понедельник'),
        ('tue', 'Вторник'),
        ('wed', 'Среда'),
        ('thu', 'Четверг'),
        ('fri', 'Пятница'),
        ('sat', 'Суббота'),
        ('sun', 'Воскресенье'),
    ]

    car_wash = models.ForeignKey(CarWash, models.DO_NOTHING, blank=True, null=True)
    day = models.TextField(max_length=3, choices=DAYS_OF_WEEK)
    time_from = models.TimeField(blank=True, null=True)
    time_to = models.TimeField(blank=True, null=True)

    class Meta:
        db_table = 'car_wash_work_time'

    def __str__(self):
        return f"{self.day}. {self.time_from}-{self.time_to}"


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.CASCADE)

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
    SERVICE_TYPES = (
        ('основная', 'Основная'),
        ('дополнительная', 'Дополнительная'),
    )
    car_wash = models.ForeignKey(CarWash, models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    car_type = models.ForeignKey(CarType, models.CASCADE, blank=True, null=True)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)

    class Meta:
        db_table = 'service'

    def __str__(self):
        return f"{self.car_wash.name} {self.name}"


class User(models.Model):
    auth_user_id = models.IntegerField(blank=True, null=True)
    user_role = models.ForeignKey('UserRole', models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return f"{self.id}" or ""


class UserRole(models.Model):
    role = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'user_role'

    def __str__(self):
        return self.role


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
        db_table = 'wash_record'

    def __str__(self):
        return f"{self.id}"


class WashRecordService(models.Model):
    wash_record = models.ForeignKey(WashRecord, models.CASCADE, blank=True, null=True)
    service = models.ForeignKey(Service, models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'wash_record_service'


class Worker(models.Model):
    car_wash = models.ForeignKey(CarWash, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    gat_at = models.DateField(blank=True, null=True)
    fired_at = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'worker'

    def __str__(self):
        return f"{self.id}" or ""


class WorkerWorkDay(models.Model):
    started_at = models.TimeField(blank=True, null=True)
    ended_at = models.TimeField(blank=True, null=True)
    worker = models.ForeignKey(Worker, models.DO_NOTHING, blank=True, null=True)
    car_wash_work_day = models.ForeignKey(CarWashWorkDay, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'worker_work_day'

    def __str__(self):
        return f"{self.started_at}-{self.ended_at}. {self.worker.user.auth_user_id}" or ""
