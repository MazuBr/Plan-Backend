from datetime import datetime, date
from enum import Enum
from typing import List, Optional

import strawberry
from strawberry.scalars import JSON


@strawberry.enum
class EventStatus(Enum):
    ACTIVE = "active"
    CANCEL = "cancel"
    PENDING = "pending"


@strawberry.enum
class RepeatTypes(Enum):
    DAYLY = "dayly"
    WEEKLY = "weekly"
    MONTHY = "monthly"
    MONTHLY_BY_WEEK = "monthly_by_week"
    YEARLY = "yearly"

@strawberry.enum
class DaysOfWeek(Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


@strawberry.type
class Repeat:
    is_repeat: Optional[bool] = None
    repeat_until: Optional[str] = None
    delay: Optional[int] = None
    repeate_type: Optional[RepeatTypes] = None


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
    repeat: Repeat
    event_status: EventStatus


@strawberry.type
class CalendarEventsByDay:
    day: date
    events: list[CalendarHumanReadable]


@strawberry.type
class CalendaDeleteEventsResponse:
    ids: List[int]


@strawberry.type
class UpdatedEvent:
    event_id: int
    title: Optional[str] = None
    comment: Optional[str] = None
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    event_status: Optional[EventStatus] = None


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
class RepeatData:
    weekly: Optional[InputWeeklyRepeat] = None
    monthly_by_week: Optional[InputMonthlyByWeekRepeat] = None
    def __post_init__(self):
        if (self.weekly is not None and self.monthly_by_week is not None) or (self.weekly is None and self.monthly_by_week is None):
            raise ValueError("You must specify either 'weekly' or 'monthly_by_week', but not both.")


@strawberry.input
class CalendaDeleteEvents:
    event_id: List[int]


@strawberry.input
class CalendaRestoreEvents:
    event_id: List[int]


@strawberry.input
class CalendarGetEvents:
    start_time: int
    end_time: int
    time_zone: str


@strawberry.input
class InputRepeat:
    repeat_until: Optional[str] = None
    delay: Optional[int] = None
    repeate_type: RepeatTypes
    repeat_data: RepeatData


@strawberry.input
class CalendarCreateEvent:
    title: str
    comment: Optional[str] = None
    start_time: int
    end_time: Optional[int] = None
    repeat: Optional[InputRepeat] = None


@strawberry.input
class CalendaUpdateEvents:
    event_id: int
    title: Optional[str] = None
    comment: Optional[str] = None
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    event_status: Optional[EventStatus] = None
    repeat: Optional[InputRepeat] = None


class EventNotFoundError(Exception):
    def __init__(self, message: str):
        self.message = message
        self.status_code = 204

    def __str__(self):
        return self.message
