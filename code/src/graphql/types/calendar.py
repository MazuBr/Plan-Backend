from typing import List, Optional, Union

import strawberry
from datetime import datetime, date


@strawberry.input
class CalendarGetEvents:
    start_time: int
    end_time: int


@strawberry.type
class Repeat:
    is_repeat: Optional[bool] = None
    repeat_until: Optional[str] = None


@strawberry.type
class Calendar:
    id: int
    title: str
    comment: Optional[str] = None
    start_time: int
    end_time: Optional[int] = None
    repeat: Repeat


@strawberry.type
class CalendarHumanReadable:
    id: int
    title: str
    comment: Optional[str] = None
    day_event_start: datetime
    end_time: Optional[datetime] = None
    repeat: Repeat


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


@strawberry.input
class CalendaDeleteEvents:
    event_id: List[int]


@strawberry.type
class CalendaDeleteEventsResponse:
    ids: List[int]


@strawberry.input
class CalendaUpdateEvents:
    event_id: int
    title: Optional[str]
    comment: Optional[str]
    start_time: Optional[int] = None
    end_time: Optional[int] = None


@strawberry.type
class UpdatedEvent:
    event_id: int
    title: Optional[str]
    comment: Optional[str]
    start_time: Optional[int] = None
    end_time: Optional[int] = None


@strawberry.type
class DatabaseError:
    error: str
