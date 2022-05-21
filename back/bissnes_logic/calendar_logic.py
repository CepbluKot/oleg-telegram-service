import calendar as cl
from datetime import date, time
from api.api_booking import get_filter_booking
from api.api_workig_date import get_filter_work_day

from datetime import datetime


def freedom_items(service, this_date, this_time: time):
    data_booking = get_filter_booking(my_service=service, my_date=this_date, g_time_start=0, g_time_end=int(this_time.hour) + 1)
    data_day = get_filter_work_day(check_day=this_date, name_service=service)

    free_items = data_day[0]['service_this_day'][service]
    for one_bk in data_booking:
        time_type = datetime.strptime(one_bk['time_end'], '%H:%M:%S').time()

        if time_type > this_time:
            print(time_type)
            free_items -= 1

        if free_items == 0:
            return "Error"

    return free_items


