from .models import CarWashWorkDay, WashRecord, Worker, WashRecordService
from rest_framework import serializers
from datetime import datetime, timedelta


def get_car_wash_working_hours(car_wash, current_date):
    work_day = CarWashWorkDay.objects.filter(car_wash=car_wash, date=current_date).first()

    if not work_day:
        return None, None

    return work_day.started_at, work_day.ended_at


def get_workers_on_shift(car_wash, current_date):
    workers = Worker.objects.filter(
        car_wash=car_wash,
        workerworkday__car_wash_work_day__date=current_date
    ).distinct()

    return workers


def get_free_slots(worker, current_date, time_slots):
    worker_orders = WashRecord.objects.filter(
        worker=worker,
        car_wash_work_day__date=current_date
    ).values_list('ordered_at', flat=True)
    formatted_times = [t.strftime('%H:%M') for t in worker_orders]
    times = [datetime.strptime(t, "%H:%M") for t in formatted_times]
    exclude_time_slots = []
    for time in times:
        exclude_time_slots.append(time.strftime("%H:%M"))
        for _ in range(2):
            time += timedelta(minutes=15)
            exclude_time_slots.append(time.strftime("%H:%M"))
    exclude_time_slots = sorted(set(exclude_time_slots))

    filtered_list = [item for item in time_slots if item not in exclude_time_slots]
    print(filtered_list)
    return set(filtered_list)


def get_free_slots_for_car_wash(car_wash, current_date):
    start_time, end_time = get_car_wash_working_hours(car_wash, current_date)
    if start_time is None or end_time is None:
        return []

    workers = get_workers_on_shift(car_wash, current_date)
    if not workers:
        return []

    time_slots = []
    current_time = start_time
    while current_time < end_time:
        time_slots.append(current_time.strftime('%H:%M'))
        current_time = (datetime.combine(datetime.today(), current_time) + timedelta(minutes=15)).time()
    time_slots = set(time_slots)
    free_slots = set()
    for worker in workers:
        slots_for_current_worker = get_free_slots(worker, current_date, time_slots)
        free_slots = free_slots | slots_for_current_worker

    return sorted(free_slots)


def get_available_time_slots_for_week(car_wash):
    available_times_for_week = {}
    today = datetime.today().date()

    for day_offset in range(7):
        current_date = today + timedelta(days=day_offset)
        available_slots = get_free_slots_for_car_wash(car_wash, current_date)
        available_times_for_week[current_date.strftime('%Y-%m-%d')] = available_slots

    return available_times_for_week


def get_available_worker(car_wash, current_date, requested_time):
    workers = get_workers_on_shift(car_wash, current_date)

    available_workers = []
    for worker in workers:
        time_slots = [requested_time.strftime('%H:%M')]
        free_slots = get_free_slots(worker, current_date, time_slots)
        if requested_time.strftime('%H:%M') in free_slots:
            # Получаем последнюю запись для рабочего
            last_wash_record = WashRecord.objects.filter(worker=worker).order_by('-ordered_at').first()
            last_record_time = last_wash_record.ordered_at if last_wash_record else datetime.min
            available_workers.append((worker, last_record_time))

    if not available_workers:
        return None

    # Сортируем доступных рабочих по последнему времени записи (от позднего к раннему)
    available_workers.sort(key=lambda x: x[1], reverse=True)

    # Возвращаем рабочего с самым поздним временем последней записи
    return available_workers[0][0]


def create_wash_record(car, time, services, car_wash):
    current_date = time.date()
    worker = get_available_worker(car_wash, current_date, time)
    if not worker:
        raise serializers.ValidationError("Нет доступных мойщиков на выбранное время.")
    wash_record = WashRecord.objects.create(
        car=car,
        client=None,
        car_wash=car_wash,
        total_price=0,
        worker=worker,
        ordered_at=None,
        started_at=None,
        finished_at=None,
    )

    total_price = sum(service.price for service in services)
    for service in services:
        WashRecordService.objects.create(wash_record=wash_record, service=service)

    wash_record.total_price = total_price
    wash_record.save(update_fields=['total_price'])
    return wash_record


