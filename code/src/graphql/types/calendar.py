from datetime import datetime, date
from enum import Enum
import json
from typing import List, Optional, Union

import strawberry
from strawberry.scalars import JSON


@strawberry.enum
class EventStatus(Enum):
    ACTIVE = "active"
    CANCEL = "cancel"
    PENDING = "pending"


@strawberry.enum
class RepeatTypes(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    MONTHLY_BY_WEEK = "monthly_by_week"
    YEARLY = "yearly"


@strawberry.enum
class DaysOfWeek(Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


@strawberry.type
class Repeat:
    repeat_data: Optional[str] = None
    repeat_until: Optional[str] = None
    delay: Optional[int] = None
    repeat_type: Optional[RepeatTypes] = None


@strawberry.type
class EventUserRole:
    user_id: int
    user_role: str


@strawberry.type
class Calendar:
    id: int
    title: str
    comment: Optional[str] = None
    start_time: int
    end_time: Optional[int] = None
    event_status: EventStatus
    repeat: Repeat
    user_data: EventUserRole


@strawberry.type
class CalendarHumanReadable:
    id: int
    title: str
    comment: Optional[str] = None
    day_event_start: datetime
    end_time: Optional[datetime] = None
    repeat: Optional[Repeat] = None
    event_status: EventStatus


@strawberry.type
class CalendarEventsByDay:
    day: date
    events: list[CalendarHumanReadable]


@strawberry.type
class CalendarDeleteEventsResponse:
    ids: List[int]


@strawberry.type
class UpdatedEvent:
    event_id: int
    title: Optional[str] = None
    comment: Optional[str] = None
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    event_status: Optional[EventStatus] = None
    repeat: Optional[Repeat] = None


@strawberry.type
class DatabaseError:
    error: str


@strawberry.input
class InputWeeklyRepeat:
    days_of_week: List[DaysOfWeek]


@strawberry.input
class InputMonthlyByWeekRepeat:
    days_of_week: DaysOfWeek
    week: int


@strawberry.input
class CalendarDeleteEvents:
    event_id: List[int]


@strawberry.input
class CalendarRestoreEvents:
    event_id: List[int]


@strawberry.input
class CalendarGetEvents:
    start_time: int
    end_time: int
    time_zone: str


class RepeatData:
    def to_dict(self):
        return self.__dict__

    @classmethod
    def expected_keys(cls) -> str:
        return "Undefined"

    @classmethod
    def from_dict(cls, data: dict, type):
        try:
            return cls(**data)
        except TypeError as e:
            expected = cls.expected_keys()
            raise ValueError(
                f'Invalid data for {type}: {data}, Expected keys "{expected}"'
            ) from e


class RepeatDataDaily(RepeatData):
    def __init__(self, daily: int):
        self.daily = daily

    @classmethod
    def expected_keys(cls) -> str:
        return "daily"


class RepeatDataWeekly(RepeatData):
    def __init__(self, days_of_week: int):
        self.days_of_week = days_of_week

    @classmethod
    def expected_keys(cls) -> str:
        return "days_of_week"


class RepeatDataMonthly(RepeatData):
    def __init__(self, day_of_month: int):
        self.day_of_month = day_of_month

    @classmethod
    def expected_keys(cls) -> str:
        return "day_of_month"


class RepeatDataMonthlyByWeek(RepeatData):
    def __init__(self, days_of_week: int, week: int):
        self.days_of_week = days_of_week
        self.week = week

    @classmethod
    def expected_keys(cls) -> List[str]:
        return ["days_of_week", "week"]


class RepeatDataYearly(RepeatData):
    def __init__(self, day_of_year: int):
        self.day_of_year = day_of_year

    @classmethod
    def expected_keys(cls) -> str:
        return "day_of_year"


RepeatDataType = Union[
    RepeatDataDaily,
    RepeatDataWeekly,
    RepeatDataMonthly,
    RepeatDataYearly,
    RepeatDataMonthlyByWeek,
]


@strawberry.input
class InputRepeat:
    repeat_until: Optional[int] = None
    delay: Optional[int] = None
    repeat_type: RepeatTypes
    repeat_data: Optional[str] = None

    def get_repeat_data(self) -> RepeatDataType:
        monthly_by_week_check = self.repeat_type == RepeatTypes.MONTHLY_BY_WEEK
        print('monthly_by_week_check: ', monthly_by_week_check)
        if self.repeat_data is None and not monthly_by_week_check:
            return None
        elif self.repeat_data is None and monthly_by_week_check:
            raise ValueError(
                'Invalid data for RepeatTypes.MONTHLY_BY_WEEK: null, Expected keys "day_of_month"'
            )
        data = json.loads(self.repeat_data)
        if self.repeat_type == RepeatTypes.DAILY:
            return RepeatDataDaily.from_dict(data, self.repeat_type)
        elif self.repeat_type == RepeatTypes.WEEKLY:
            return RepeatDataWeekly.from_dict(data, self.repeat_type)
        elif self.repeat_type == RepeatTypes.MONTHLY:
            return RepeatDataMonthly.from_dict(data, self.repeat_type)
        elif monthly_by_week_check:
            return RepeatDataMonthly.from_dict(data, self.repeat_type)
        elif self.repeat_type == RepeatTypes.YEARLY:
            return RepeatDataMonthly.from_dict(data, self.repeat_type)
        else:
            raise ValueError("Unknown repeat type")

    def set_repeat_data(self, data: RepeatDataType):
        self.repeat_data = json.dumps(data.to_dict())


@strawberry.input
class CalendarCreateEvent:
    title: str
    comment: Optional[str] = None
    start_time: int
    end_time: Optional[int] = None
    repeat: Optional[InputRepeat] = None


@strawberry.input
class CalendarUpdateEvents:
    event_id: int
    title: Optional[str]
    comment: Optional[str]
    start_time: Optional[int]
    end_time: Optional[int]
    event_status: Optional[EventStatus]
    repeat: Optional[InputRepeat]
    


class EventNotFoundError(Exception):
    def __init__(self, message: str):
        self.message = message
        self.status_code = 204

    def __str__(self):
        return self.message
