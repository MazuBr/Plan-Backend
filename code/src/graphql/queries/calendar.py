import strawberry

from src.database.postgres_connection import Database
from src.graphql.types.calendar import CalendarGetEvents, CalendarHumanReadable, Repeat, CalendarEventsByDay
@strawberry.type
class EventQuery:
    @strawberry.field
    def events(self, input: CalendarGetEvents) -> list[CalendarEventsByDay]:
        query = """
        SELECT
            id,
            title,
            comment,
            to_timestamp(start_time)::date AS event_date,
            to_timestamp(start_time) AS start_time,
            to_timestamp(end_time) AS end_time,
            is_repeat,
            repeat_until
        FROM
            calendar
        WHERE
            start_time BETWEEN %(start_time)s AND %(end_time)s
        ORDER BY
            start_time ASC;
        """
        db = Database()

        db_response: list[dict] = db.fetch_all(query=query, params={'start_time': input.start_time, 'end_time': input.end_time})
        events_by_day = {}
        for row in db_response:
            event = CalendarHumanReadable(
                    id=row.get('id'),
                    title=row.get('title'),
                    comment=row.get('comment'),
                    day_event_start=row.get('start_time'),
                    end_time=row.get('end_time'),
                    repeat=Repeat(is_repeat=row.get('is_repeat'), repeat_until=row.get('repeat_until'))
                )
            event_date = row.get('event_date')
            if event_date not in events_by_day:
                events_by_day[event_date] = []
            events_by_day[event_date].append(event)
            
        return [
            CalendarEventsByDay(day=day, events=events) for day, events in events_by_day.items()
        ]
    