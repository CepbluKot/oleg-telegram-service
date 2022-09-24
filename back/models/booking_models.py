from setting_web import db
from datetime import timedelta, date
from calendar import weekday
from typing import List, Optional
import rapidjson


class DefaultSetting(db.Model):
    __tablename__ = 'default_setting'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_event = db.Column(db.Time)
    end_event = db.Column(db.Time)
    delta_time = db.Column(db.Time)
    default_services = db.Column(db.JSON)

    def __int__(self, start_event, end_event, delta_time, default_services):
        self.start_event = start_event
        self.end_event = end_event
        self.delta_time = delta_time
        self.default_services = default_services

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_from_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class MyService(db.Model):
    __tablename__ = 'myservice'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_service = db.Column(db.String, unique=True)
    price_service = db.Column(db.Float)
    duration = db.Column(db.Time)
    max_booking = db.Column(db.Integer)

    def __init__(self, name_service, price=None, duration=None, max_booking=None):
        self.name_service = name_service
        self.price_service = price
        self.duration=duration
        self.max_booking=max_booking

    def __repr__(self):
        return f"Service ('{self.name_service}')"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_from_db(self):
        db.session.commit()

    @classmethod
    def find_by_name(cls, name_s) -> "MyService":
        return cls.query.filter_by(name_service=name_s).first()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class MyStaff(db.Model):
    __tablename__ = 'mystaff'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_staff = db.Column(db.String)

    def __init__(self, name_staff):
        self.name_staff = name_staff
        self.save_to_db()

    def __repr__(self):
        return f"Staff ('{self.name_staff}')"

    @classmethod
    def find_my_id(cls, id_) -> 'MyStaff':
        return cls.query.filter(MyStaff.id == id_).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_from_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class CompanyUsers(db.Model):
    __tablename__ = 'users_this_company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_client = db.Column(db.String)
    tg_id = db.Column(db.Integer, unique=True)
    phone_num = db.Column(db.String)

    def __init__(self, new_name, tg_id, phone_num):
        self.name_client = new_name
        self.tg_id = tg_id
        self.phone_num = phone_num
        self.save_to_db()

    def __repr__(self):
        return f"User ('{self.name_client}', {self.tg_id})"

    @classmethod
    def find_by_tg_id(cls, tg_id_) -> 'CompanyUsers':
        return cls.query.filter(cls.tg_id == tg_id_).first()

    @classmethod
    def find_by_phone(cls, phone_) -> 'CompanyUsers':
        return cls.query.filter(cls.phone_num == phone_).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_from_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Event(db.Model):
    __tablename__ = 'event_company'

    __table_args__ = (
        db.UniqueConstraint("name_event", "day_start", "day_end", "start_event", "end_event"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_event = db.Column(db.String, default="Work_Day")
    day_start = db.Column(db.Date, nullable=False)
    day_end = db.Column(db.Date, nullable=False)
    start_event = db.Column(db.Time)
    end_event = db.Column(db.Time)
    weekdays = db.Column(db.ARRAY(db.Integer), default=None)
    many_day = db.Column(db.ARRAY(db.Date), default=None)

    """weekday: 
    'Mon' -> 0
    'Thus' -> 1
    ...
    'Sun' -> 6
    """

    def __init__(self, name, day_start, day_end, start_event, end_event, weekdays_list=None):
        self.name_event = name
        self.day_start = day_start
        self.day_end = day_end
        self.start_event = start_event
        self.end_event = end_event
        self.weekdays = weekdays_list

        print(weekdays_list, day_end - day_start)
        if weekdays_list is not None or day_end - day_start > timedelta(days=0):
            print('EEEEEEEEEEEEEE')
            days = []
            for single_date in self.daterange(day_start, day_end):
                    if weekdays_list is not None and len(weekdays_list) != 0:
                        if weekday(single_date.year, single_date.month, single_date.day) not in weekdays_list:
                            continue
                    print('bbbb')
                    days.append(date(single_date.year, single_date.month, single_date.day))

            self.many_day = days

        try:
            self.save_to_db()
        except:
            print("ERROR ADD EVENT")

    def __repr__(self):
        return f"Event ('{self.name_event, self.day_start}')"

    def daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    @classmethod
    def find_by_id(cls, id_) -> 'Event':
        return cls.query.filter(cls.id == id_).first()

    @classmethod
    def find_by_name_day(cls, id_) -> 'Event':
        return cls.query.filter(cls.id == id_).first()

    @classmethod
    def find_by_all_parameters(cls, name_, day_start_, day_end_, time_start_, time_end_) -> 'Event':
        return cls.query.filter(db.and_(cls.name_event == name_,
                                        cls.day_start == day_start_,
                                        cls.day_end == day_end_,
                                        cls.start_event == time_start_,
                                        cls.end_event == time_end_)).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_from_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class AllBooking(db.Model):
    __tablename__ = 'all_booking'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time_start = db.Column(db.Time)
    time_end = db.Column(db.Time)
    day_booking = db.Column(db.Date)

    signup_event = db.Column(db.Integer, db.ForeignKey('event_company.id')) #день_записи
    connect_event = db.relationship('Event', backref='event_booking')

    signup_user = db.Column(db.Integer, db.ForeignKey('users_this_company.id')) #человек который записался
    connect_user = db.relationship('CompanyUsers')

    signup_service = db.Column(db.Integer, db.ForeignKey('myservice.id')) #услуга
    connect_service = db.relationship('MyService', backref='service_ab')

    signup_staff = db.Column(db.Integer, db.ForeignKey('mystaff.id')) #тренер
    connect_staff = db.relationship('MyStaff')
    comment = db.Column(db.TEXT)

    def __init__(self, event_id, client_id, service_id, time_start, time_end, staff_id):
        self.signup_event = event_id
        self.signup_service = service_id
        self.signup_user = client_id
        self.signup_staff = staff_id
        self.time_start = time_start
        self.time_end = time_end


    @classmethod
    def find_booking_by_event_id(cls, event_id):
        if type(event_id) == list:
            return cls.query.filter(cls.signup_event.in_(event_id))
        elif type(event_id) == int:
            return cls.query.filter(cls.signup_event == event_id)



    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_from_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class ServiceEvent(db.Model):
    __tablenmae__ = 'event_service'

    __table_args__ = (
        db.UniqueConstraint("event_id", "service_id"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    event_id = db.Column(db.Integer, db.ForeignKey('event_company.id'), nullable=False)
    event_connect = db.relationship('Event', backref=db.backref('event_se', cascade="all, delete-orphan"), lazy='joined')

    service_id = db.Column(db.Integer, db.ForeignKey('myservice.id'), nullable=False)
    service_connect = db.relationship('MyService', backref=db.backref('service_se', cascade="all, delete-orphan"), passive_deletes=False)

    count_service_this_event = db.Column(db.JSON, nullable=False)

    def __init__(self, event_id, service_id, windows_service):
        self.event_id = event_id
        self.service_id = service_id
        self.count_service_this_event = rapidjson.dumps(windows_service)

        self.save_to_db()

    @classmethod
    def find_by_event_and_service(cls, event_id, service_name) -> List['ServiceEvent']:
        find_service = MyService.find_by_name(service_name)
        return cls.query.filter(db.and_(cls.service_id == find_service, cls.event_id == event_id)).first()

    @classmethod
    def event_search_by_service(cls, service_name):
        find_service = MyService.find_by_name(service_name)
        try:
            return cls.query.filter(db.and_(cls.service_id == find_service.id)).options(db.load_only(cls.event_id)).all()
        except AttributeError:
            return None

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            print("DONT ADD CONNECT SERVICE AND EVENT")

    def save_many_to_db(self, objects: list):
        try:
            db.session.add_all(objects)
            db.session.commit()
        except:
            print("DONT ADD CONNECT SERVICE AND EVENT")

    def update_from_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class ServiceStaffConnect(db.Model):
    __tablename__ = 'service_staff_connect'

    __table_args__ = (
        db.UniqueConstraint("service_id", "staff_id"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(db.Integer, db.ForeignKey('myservice.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('mystaff.id'), nullable=False)

    service_connect = db.relationship('MyService', backref='ssc_service_se')
    staff_connect = db.relationship('MyStaff', backref='ssc_staff_se')

    def __init__(self, name_service, name_staff):
        find_ser = MyService.query.filter(MyService.name_service == name_service).first()
        find_sf = MyStaff.query.filter(MyStaff.name_staff == name_staff).first()

        if find_ser and find_ser is not None:
            find_repetition = db.session.query(ServiceStaffConnect.query.filter(db.and_(
            ServiceStaffConnect.staff_id == find_sf.id,
            ServiceStaffConnect.service_id == find_ser.id)).exists()).scalar()

            if not find_repetition:
                try:
                    self.service_id = find_ser.id
                    self.staff_id = find_sf.id
                    self.save_to_db()
                except:
                    print("ERROR ~ DON'T CREATED ServiceStaffConnect")
            else:
                print("ERROR ~ DON'T CREATED ServiceStaffConnect")
        else:
            print("ERROR ~ DON'T CREATED ServiceStaffConnect")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_connect(cls, name_service, name_staff) -> 'ServiceStaffConnect':
        con = cls.query.join(MyService).join(MyStaff)
        con = con.filter(db.and_(MyService.name_service == name_service, MyStaff.name_staff == name_staff))
        return con.first()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()