from typing import List, Optional
from enum import Enum
import strawberry
from datetime import datetime, date


@strawberry.enum
class EventStatus(Enum):
    ACTIVE = "active"
    CANCEL = "cancel"
    PENDING = "pending"


@strawberry.input
class CalendarGetEvents:
    start_time: int
    end_time: int
    time_zone: str


@strawberry.type
class Repeat:
    is_repeat: Optional[bool] = None
    repeat_until: Optional[str] = None


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


@strawberry.input
class CalendarCreateEvent:
    title: str
    comment: Optional[str] = None
    start_time: int
    end_time: Optional[int] = None
    event_status: Optional[EventStatus] = None


@strawberry.input
class CalendaDeleteEvents:
    event_id: List[int]


@strawberry.type
class CalendaDeleteEventsResponse:
    ids: List[int]


@strawberry.input
class CalendaUpdateEvents:
    event_id: int
    title: Optional[str] = None
    comment: Optional[str] = None
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    event_status: Optional[EventStatus] = None


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
