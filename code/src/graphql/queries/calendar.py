import json

import strawberry
from strawberry.types import info

from src.database.postgres_connection import Database
from src.graphql.types.calendar import (
    CalendarGetEvents,
    CalendarHumanReadable,
    CalendarEventsByDay,
    Calendar,
    Repeat,
)


@strawberry.type
class CalendarQuery:
    @strawberry.field
    def calendar(
        self, input: CalendarGetEvents, info: info
    ) -> list[CalendarEventsByDay]:
        user_id: int = info.context.get("request").state.user_id
        query = """
        SELECT
            c.id,
            title,
            comment,
            (to_timestamp(start_time) AT TIME ZONE %(time_zone)s)::date AS event_date,
            to_timestamp(start_time) AS start_time,
            to_timestamp(end_time) AS end_time,
            repeat_data,
            repeat_until, delay, repeat_type,
            status as event_status
        FROM
            calendar c
        LEFT JOIN calendar_user_association on calendar_id = c.id
        WHERE
            start_time BETWEEN %(start_time)s AND %(end_time)s
            and user_id = %(user_id)s
            and is_delete = false
        ORDER BY
            start_time ASC;
        """
        db = Database()

        db_response: list[dict] = db.fetch_all(
            query=query,
            params={
                "start_time": input.start_time,
                "end_time": input.end_time,
                "user_id": user_id,
                "time_zone": input.time_zone,
            },
        )
        events_by_day = {}
        for row in db_response:
            if row.get("repeat_data"):
                repeat = Repeat(
                    repeat_data=json.dumps(row.get("repeat_data")),
                    delay=row.get("delay"),
                    repeat_until=row.get("repeat_until"),
                    repeat_type=row.get("repeat_type"),
                )
            else:
                repeat = None
            event = CalendarHumanReadable(
                id=row.get("id"),
                title=row.get("title"),
                comment=row.get("comment"),
                day_event_start=row.get("start_time"),
                end_time=row.get("end_time"),
                event_status=row.get("event_status"),
                repeat=repeat,
            )

            event_date = row.get("event_date")
            if event_date not in events_by_day:
                events_by_day[event_date] = []
            events_by_day[event_date].append(event)

        return [
            CalendarEventsByDay(day=day, events=events)
            for day, events in events_by_day.items()
        ]

    @strawberry.field
    def calendar_epoch(self, input: CalendarGetEvents) -> list[Calendar]:
        print("input1: ", input)
        query = """
        SELECT
            id,
            title,
            comment,
            start_time,
            end_time,
            repeat_data
        FROM
            calendar
        WHERE
            start_time BETWEEN %(start_time)s AND %(end_time)s
            and is_delete = false
        ORDER BY
            start_time ASC;
        """
        db = Database()

        db_response: list[dict] = db.fetch_all(
            query=query,
            params={"start_time": input.start_time, "end_time": input.end_time},
        )
        return [
            Calendar(
                id=row.get("id"),
                title=row.get("title"),
                comment=row.get("comment"),
                start_time=row.get("start_time"),
                end_time=row.get("end_time"),
                repeat=Repeat(
                    repeat=Repeat(
                        **(
                            row.get("repeat_data")
                            if row.get("repeat_data") is not None
                            else {}
                        )
                    ),
                ),
            )
            for row in db_response
        ]
