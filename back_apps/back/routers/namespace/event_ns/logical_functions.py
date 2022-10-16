import json
from datetime import date
from calendar import Calendar

from .validate import AnswerCalendar
from .queries import find_booking_this_day

cl = Calendar()


def find_boundaries_week(day):
    """Поиск начала и конца недели"""
    mycal = cl.monthdatescalendar(day.year, day.month)
    start_end_week = [] #beginning and end of the week
    all_week = [] #the whole week

    for week in mycal:
        if day in week:
            start_end_week.append(week[0])
            start_end_week.append(week[-1])

            all_week = week
            break

    return start_end_week, all_week


def get_indo_calendar(cor_date: date):
    """Calendar Booking"""

    answer_calendar = []
    start_end_weeks, all_week = find_boundaries_week(cor_date)
    try:
        for one_day in all_week:
            one_answer_booking = AnswerCalendar(day=one_day.strftime('%Y-%m-%d'),
                                                event_day=find_booking_this_day(one_day))

            answer_calendar.append(json.loads(one_answer_booking.json()))
    except:
        return {"message": "not can create calendar, maybe not valid data"}, 404
    return answer_calendar, 200