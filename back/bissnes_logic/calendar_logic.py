import calendar as cl
from datetime import date, time
from api.api_booking import get_filter_booking
from api.api_workig_date import work_date_service


def freedom_items(service, this_date, this_time: time):
    data_booking = get_filter_booking(my_service=service, my_date=this_date, g_time_start=0, g_time_end=int(this_time.hour) + 1)
    data_day = work_date_service(check_day=this_date, name_service=service)

    free_items = data_day['free_items'][service]
    for one_bk in data_booking:
        if one_bk["time_end"] < this_time:
            free_items -= 1

        if free_items == 0:
            return "Error"

    return free_items


