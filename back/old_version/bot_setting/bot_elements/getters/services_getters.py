from queries.queries_workig_date import weeks_in_all_event, get_filter_work_day
from queries.queries_services import all_service
import re

from datetime import datetime, date

def get_all_services_names():
    data_map_service = all_service()
    services = []

    for one_service in data_map_service:
        services.append(one_service['name_service'])

    return services


def get_service_weeks(service_name: str):
    weeks = []
    data_mas_service = weeks_in_all_event(name_service=service_name)

    for one_weeks in data_mas_service:
        start_week = str(one_weeks[0])
        end_week = str(one_weeks[1])

        weeks.append(start_week + ' - ' + end_week)

    return weeks


def get_service_days(service_name: str, service_week: str):
    days = []

    sep = re.split(' - ', service_week)

    start_week = datetime.strptime(sep[0], '%Y-%m-%d').date()
    end_week = datetime.strptime(sep[1], '%Y-%m-%d').date()

    res_map_data = get_filter_work_day(name_service=service_name, between_start=start_week, between_end=end_week)
    for one_day in res_map_data:
        days.append(one_day['day'])

    return days


