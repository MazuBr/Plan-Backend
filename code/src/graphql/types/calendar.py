from typing import Optional

import strawberry
from datetime import datetime, date
@strawberry.type
class Repeat:
    is_repeat: bool
    repeat_until: str


@strawberry.type
class Calendar:
    id: int
    title: str
    comment: str
    start_time: int
    end_time: int
    repeat: Repeat


@strawberry.type
class CalendarHumanReadble:
    id: int
    title: str
    comment: str
    day_event_start: datetime
    end_time: datetime
    repeat: Repeat

@strawberry.type
class CalendarEventsByDay:
    day = date
    events: list[CalendarHumanReadble]

@strawberry.input
class CalendarCreateEvent:
    title: str
    comment: Optional[str] = None
    start_time: int
    end_time: Optional[int] = None


@strawberry.input
class CalendarGetEvents:
    start_time: int
    end_time: int
