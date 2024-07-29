import strawberry
from strawberry.types import info

from src.graphql.types.calendar import (
    CalendarCreateEvent,
    Calendar,
    Repeat,
    CalendaDeleteEvents,
    DatabaseError,
    CalendaDeleteEvents,
    CalendaDeleteEventsResponse,
    CalendaUpdateEvents,
    UpdatedEvent,
    EventUserRole,
)
from src.database.postgres_connection import Database


@strawberry.type
class EventMutation:
    @strawberry.mutation
    def create_event(self, input: CalendarCreateEvent, info: info) -> Calendar:
        user_id: int = info.context.get("request").state.user_id
        db = Database()
        query = """
            WITH new_calendar AS (
                INSERT INTO calendar (title, comment, start_time, end_time, is_repeat, repeat_until)
                VALUES (%(title)s, %(comment)s, %(start_time)s, %(end_time)s, %(is_repeat)s, %(repeat_until)s)
                RETURNING id, title, comment, start_time, end_time, is_repeat, repeat_until
            )
            , inserted_association AS (
                INSERT INTO calendar_user_association (calendar_id, user_id, role)
                SELECT id, %(user_id)s, 'creator' 
                FROM new_calendar
                RETURNING calendar_id, user_id, role
            )
            SELECT 
                nc.id, nc.title, nc.comment, nc.start_time, nc.end_time, nc.is_repeat, nc.repeat_until, 
                ia.user_id, ia.role
            FROM 
                new_calendar nc
            JOIN 
                inserted_association ia
            ON 
                nc.id = ia.calendar_id;
        """

        data = {
            "user_id": user_id,
            "title": input.title,
            "comment": input.comment if input.comment is not None else "",
            "start_time": input.start_time,
            "end_time": input.end_time if input.end_time is not None else None,
            "is_repeat": False,
            "repeat_until": None,
        }

        new_event = db.fetch_one(query=query, params=data)
        print("new_event: ", new_event)
        return Calendar(
            id=new_event.get("id"),
            title=new_event.get("title"),
            comment=new_event.get("comment"),
            start_time=new_event.get("start_time"),
            end_time=new_event.get("end_time"),
            repeat=Repeat(
                is_repeat=new_event.get("is_repeat"),
                repeat_until=new_event.get("repeat_until"),
            ),
            user_data=EventUserRole(
                user_id=new_event.get("user_id"), user_role=new_event.get("role")
            ),
        )

    @strawberry.mutation
    def delete_event(self, input: CalendaDeleteEvents) -> CalendaDeleteEventsResponse:
        db = Database()
        query = """
            UPDATE calendar set is_delete = True WHERE id = ANY(%(ids)s::int[]) and is_delete = false RETURNING id;
        """

        new_event = db.fetch_all(query=query, params={"ids": input.event_id})
        if isinstance(new_event, str) and new_event.startswith("Server error"):
            return DatabaseError("Database error")

        return CalendaDeleteEventsResponse(ids=[event["id"] for event in new_event])

    @strawberry.mutation
    def update_event(self, input: CalendaUpdateEvents) -> UpdatedEvent:
        db = Database()

        query = """
            UPDATE calendar
            SET 
                title = COALESCE(%(title)s, title),
                comment = COALESCE(%(comment)s, comment),
                start_time = COALESCE(%(start_time)s, start_time),
                end_time = COALESCE(%(end_time)s, end_time)
            WHERE id = %(event_id)s
            and is_delete = FALSE
            RETURNING id, title, comment, start_time, end_time;
        """

        params = {
            "event_id": input.event_id,
            "title": input.title,
            "comment": input.comment,
            "start_time": input.start_time,
            "end_time": input.end_time,
        }

        try:
            updated_event = db.fetch_one(query=query, params=params)
            if not updated_event:
                return DatabaseError(error="Event not found or no changes made")

            return UpdatedEvent(
                event_id=updated_event["id"],
                title=updated_event["title"],
                comment=updated_event["comment"],
                start_time=updated_event["start_time"],
                end_time=updated_event["end_time"],
            )

        except Exception as e:
            return DatabaseError(error=str(e))
