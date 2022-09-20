from back.models.booking_models import MyStaff
from .schema import StaffSchema

from .validate import FilterStaff as Filter


def _base_query():
    return MyStaff.query


def all_staff():
    data_staff = _base_query()
    api_staff_schema = StaffSchema(many=True)

    return api_staff_schema.dump(data_staff)


def filter_staff(new_filter: Filter):
    data_staff = _base_query()

    if new_filter.name_staff is not None and len(new_filter.name_staff) > 0:
        data_staff = data_staff.filter(MyStaff.name_staff.in_(new_filter.name_staff))

    if new_filter.id is not None and len(new_filter.id) > 0:
        data_staff = data_staff.filter(MyStaff.id.in_(new_filter.id))

    api_staff_schema = StaffSchema(many=True)
    return api_staff_schema.dump(data_staff)