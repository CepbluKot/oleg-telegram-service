from setting_web import db
from sqlalchemy.exc import PendingRollbackError, IntegrityError
from datetime import timedelta, date, time, datetime
from calendar import weekday
from typing import List
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
    price_service = db.Column(db.Float, default=0, nullable=False)
    duration = db.Column(db.Time, default=time(hour=0, minute=0, second=0), nullable=False)
    max_booking = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, name_service, price=None, duration=None, max_booking=None):
        self.name_service = name_service
        self.price_service = price
        self.duration = duration
        self.max_booking = max_booking

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
    name_staff = db.Column(db.String, unique=True, nullable=False)

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
    name_client = db.Column(db.String, nullable=False)
    tg_id = db.Column(db.Integer, unique=True)
    phone_num = db.Column(db.String, nullable=False)

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


class EventSetting(db.Model):
    __tablename__ = 'event_setting'

    __table_args__ = (
        db.UniqueConstraint("name_event", "day_start_g", "day_end_g", "event_time_start", "event_time_end"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_event = db.Column(db.String, default="Work_Day")
    day_start_g = db.Column(db.Date, nullable=False)
    day_end_g = db.Column(db.Date, nullable=False)
    event_time_start = db.Column(db.Time, nullable=False)
    event_time_end = db.Column(db.Time, nullable=False)

    status_repid_day = db.Column(db.Boolean, default=False)
    day_end_rapid = db.Column(db.Date, default=date(year=1917, month=3, day=2))

    weekdays = db.Column(db.ARRAY(db.Integer), default=[])

    def __init__(self, **kwargs):
        # try:

        self.name_event = kwargs['name_event']
        self.day_start_g = kwargs['day_start_g']
        self.day_end_g = kwargs['day_end_g']
        self.event_time_start = kwargs['event_time_start']
        self.event_time_end = kwargs['event_time_end']

        try:
            self.status_repid_day = kwargs['status_repid_day']
        except KeyError:
            print({'message': 'dont get status rapid day'})
            raise ValueError

        try:
            self.day_end_rapid = kwargs['day_end_rapid']
        except KeyError:
            print({'message': 'dont get day_end_rapid'})
            raise ValueError

        try:
            self.weekdays = kwargs['weekdays']
        except KeyError:
            print({'message': 'dont get weekdays'})
            raise ValueError

        try:
            self.save_to_db()
            self.create_days_event()
        except PendingRollbackError:
            db.session.roolback()
            print({'message': 'dont pulling event_setting in database'})
            raise ValueError

        # except KeyError:
        #     print({'message': 'dont create event'})
        #     raise ValueError

    def __repr__(self):
        return f"EventSetting ('{self.name_event, self.day_start_g}')"

    def add_db_event(self, day_start, day_end, time_start, time_end):
        """создание дней к событию"""
        try:
            EventDay(day_start=day_start, day_end=day_end, time_start=time_start, time_end=time_end, setting_id=self.id)
        except:
            self.delete_from_db()
            raise ValueError("not correct input data")

    def create_days_event(self):
        """подготовка дней к созданию"""
        if self.status_repid_day:
            for single_date in self.daterange(self.day_start_g, self.day_end_rapid):
                if len(self.weekdays) and weekday(single_date.year, single_date.month, single_date.day) not in self.weekdays:
                    continue

                if self.day_end_g > self.day_start_g:
                    self.add_db_event(single_date, single_date + timedelta(days=1), self.event_time_start, self.event_time_end)
                elif self.day_start_g == self.day_end_g:
                    self.add_db_event(single_date, single_date, self.event_time_start, self.event_time_end)
        else:
            """Выозов функции создания дня"""
            self.add_db_event(self.day_start_g, self.day_end_g, self.event_time_start, self.event_time_end)

    def daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    @classmethod
    def find_by_id(cls, id_) -> 'EventSetting':
        return cls.query.filter(cls.id == id_).first()

    @classmethod
    def find_by_name_day(cls, id_) -> 'EventSetting':
        return cls.query.filter(cls.id == id_).first()

    @classmethod
    def find_by_all_parameters(cls, name_, day_start_, day_end_, time_start_, time_end_) -> 'EventSetting':
        return cls.query.filter(db.and_(cls.name_event == name_,
                                        cls.day_start_g == day_start_,
                                        cls.day_end_g == day_end_,
                                        cls.event_time_start == time_start_,
                                        cls.event_time_end == time_end_)).first()


    @classmethod
    def change_time(cls, day):
        pass

    @classmethod
    def change_day(cls, day):
        pass

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_from_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class EventDay(db.Model):
    __tablename__ = 'event_day_company'

    __table_args__ = (
         db.UniqueConstraint("event_setting_id", "event_time_start", "event_time_end", "day_start", "day_end"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    day_start = db.Column(db.Date, nullable=False)
    day_end = db.Column(db.Date, nullable=False)

    event_time_start = db.Column(db.Time, nullable=False)
    event_time_end = db.Column(db.Time, nullable=False)

    event_setting_id = db.Column(db.Integer, db.ForeignKey('event_setting.id'))
    connect_event_setting = db.relationship('EventSetting', backref=db.backref('event_day_se', cascade="all, delete-orphan"), lazy='joined')


    def __init__(self,  day_start, day_end, time_start, time_end, setting_id):
        self.day_start = day_start
        self.day_end = day_end
        self.event_time_start = time_start
        self.event_time_end = time_end
        self.event_setting_id = setting_id

        self.save_to_db()

    def __repr__(self):
        return f"EvevntDay ('{self.day_start}', '{self.day_end}', event_setting: {self.event_setting_id}, my id: {self.id} ')"

    @classmethod
    def find_by_event_setting_id(cls, event_id_) -> 'List[EventDay]':
        return cls.query.filter(cls.event_setting_id == event_id_)

    @classmethod
    def find_by_event_day_id(cls, event_day_id_) -> 'EventDay':
        return cls.query.filter(cls.id == event_day_id_).first()

    @classmethod
    def find_by_event_setting_id_and_day(cls, event_day_id_, day: date) -> 'EventDay':
        return cls.query.filter(db.and_(cls.event_setting_id == event_day_id_, cls.day_start == day)).first()

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
    booking_time_start = db.Column(db.Time, default=time(hour=0), nullable=False)
    booking_time_end = db.Column(db.Time, default=time(hour=0), nullable=False)

    booking_day_start = db.Column(db.Date, default=date(year=1, month=1, day=1), nullable=False)
    booking_day_end = db.Column(db.Date, default=date(year=1, month=1, day=1), nullable=False)

    signup_event = db.Column(db.Integer, db.ForeignKey('event_day_company.id')) #день_записи
    connect_event = db.relationship('EventDay', backref=db.backref('event_booking', cascade="all, delete-orphan"), lazy='joined')

    signup_user = db.Column(db.Integer, db.ForeignKey('users_this_company.id')) #человек который записался
    connect_user = db.relationship('CompanyUsers')

    signup_service = db.Column(db.Integer, db.ForeignKey('myservice.id')) #услуга
    connect_service = db.relationship('MyService', backref='service_ab')

    signup_staff = db.Column(db.Integer, db.ForeignKey('mystaff.id'), nullable=False) #тренер\
    connect_staff = db.relationship('MyStaff', backref='staff_booking')

    comment = db.Column(db.TEXT)

    def __init__(self, event_day_id,  day_start, day_end, client_id, service_id, time_start, time_end, staff_id=1):
        self.booking_day_start = day_start
        self.booking_day_end = day_end
        self.signup_event = event_day_id
        self.signup_service = service_id
        self.signup_user = client_id
        self.signup_staff = staff_id
        self.booking_time_start = time_start
        self.booking_time_end = time_end

        try:
            self.save_to_db()
        except IntegrityError:
            db.session.rollback()
            raise IntegrityError

    def __repr__(self):
        return f"AllBooking ('{self.connect_event}')"

    @classmethod
    def find_booking_by_event_id(cls, event_id) -> 'AllBooking':
        if type(event_id) == list:
            return cls.query.filter(cls.signup_event.in_(event_id))
        elif type(event_id) == int:
            return cls.query.filter(cls.signup_event == event_id)

    @classmethod
    def find_exists_booking(cls, event_day_id, client_id, staff_id, time_start, time_end):
        return cls.query.filter_by(db.and_(cls.signup_event == event_day_id,
                                           cls.signup_user == client_id,
                                           cls.signup_staff == staff_id,
                                           cls.time_start == time_start,
                                           cls.time_end == time_end)) is not None

    @classmethod
    def find_by_client_id(cls, _client_id):
        return cls.query.filter(cls.signup_user == _client_id)

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

    event_id = db.Column(db.Integer, db.ForeignKey('event_setting.id'), nullable=False)
    event_connect = db.relationship('EventSetting', backref=db.backref('event_se', cascade="all, delete-orphan"), lazy='joined')

    service_id = db.Column(db.Integer, db.ForeignKey('myservice.id'), nullable=False)
    service_connect = db.relationship('MyService', backref=db.backref('service_se', cascade="all, delete-orphan"), passive_deletes=False)

    count_service_this_event = db.Column(db.JSON, nullable=False)

    def __init__(self, event_id, service_id, windows_service):
        self.event_id = event_id
        self.service_id = service_id
        self.count_service_this_event = rapidjson.dumps(windows_service)

        try:
            self.save_to_db()
        except PendingRollbackError:
            print({"massage": "error connect"})

    @classmethod
    def find_by_event_and_service(cls, event_id, service_name) -> List['ServiceEvent']:
        find_service = MyService.find_by_name(service_name)
        return cls.query.filter(db.and_(cls.service_id == find_service, cls.event_id == event_id)).first()

    @classmethod
    def event_setting_search_by_service(cls, service_name):
        find_service = MyService.find_by_name(service_name)
        try:
            return cls.query.filter(cls.service_id == find_service.id).all()
        except AttributeError:
            return None

    @classmethod
    def event_day_search_by_service(cls, service_name):
        find_service = MyService.find_by_name(service_name)
        try:
            now_date = datetime.now()
            this_day = date(year=now_date.year, month=now_date.month, day=now_date.day)

            return db.session.query(cls.event_id, cls.service_id, MyService.duration, EventSetting.name_event, EventDay). \
                join(MyService, cls.service_id == MyService.id). \
                join(EventDay, cls.event_id == EventDay.event_setting_id).\
                join(EventSetting, cls.event_id == EventSetting.id).\
                filter(db.and_(cls.service_id == find_service.id, EventDay.day_end > date(year=2020, month=1, day=1))).all()
        except AttributeError:
            return None

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
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