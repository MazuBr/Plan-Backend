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
                INSERT INTO calendar (title, comment, start_time, end_time, is_repeat, repeat_until, event_status)
                VALUES (%(title)s, %(comment)s, %(start_time)s, %(end_time)s, %(is_repeat)s, %(repeat_until)s, %(event_status)s)
                RETURNING id, title, comment, start_time, end_time, is_repeat, repeat_until, event_status
            )
            , inserted_association AS (
                INSERT INTO calendar_user_association (calendar_id, user_id, role)
                SELECT id, %(user_id)s, 'creator' 
                FROM new_calendar
                RETURNING calendar_id, user_id, role
            )
            SELECT 
                nc.id, nc.title, nc.comment, nc.start_time, nc.end_time, nc.is_repeat, nc.repeat_until, 
                ia.user_id, ia.role, event_status
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
            "event_status": (
                input.event_status.value
                if input.event_status is not None
                else "pending"
            ),
            "repeat_until": None,
        }

        new_event = db.fetch_one(query=query, params=data)
        return Calendar(
            id=new_event.get("id"),
            title=new_event.get("title"),
            comment=new_event.get("comment"),
            start_time=new_event.get("start_time"),
            end_time=new_event.get("end_time"),
            event_status=new_event.get("event_status"),
            repeat=Repeat(
                is_repeat=new_event.get("is_repeat"),
                repeat_until=new_event.get("repeat_until"),
            ),
            user_data=EventUserRole(
                user_id=new_event.get("user_id"), user_role=new_event.get("role")
            ),
        )

    @strawberry.mutation
    def delete_event(
        self, input: CalendaDeleteEvents, info: info
    ) -> CalendaDeleteEventsResponse:
        user_id: int = info.context.get("request").state.user_id
        db = Database()
        query = """
            UPDATE calendar
                SET is_delete = TRUE
                WHERE id = ANY(%(ids)s::int[])
                AND is_delete = FALSE
                AND EXISTS (
                SELECT 1
                FROM calendar_user_association
                WHERE user_id = %(user_id)s 
                AND calendar_user_association.calendar_id = calendar.id
                )
                RETURNING id;
        """

        new_event = db.fetch_all(
            query=query, params={"ids": input.event_id, "user_id": user_id}
        )

        if isinstance(new_event, tuple) and new_event[1] == "Server error":
            return DatabaseError("Database error")
        ids = [event["id"] for event in new_event]
        return CalendaDeleteEventsResponse(ids=ids)

    @strawberry.mutation
    def update_event(self, input: CalendaUpdateEvents, info: info) -> UpdatedEvent:
        db = Database()

        query = """
            UPDATE calendar
            SET 
                title = COALESCE(%(title)s, title),
                comment = COALESCE(%(comment)s, comment),
                start_time = COALESCE(%(start_time)s, start_time),
                end_time = COALESCE(%(end_time)s, end_time)
                event_status = COALESCE(%(event_status)s, end_time)
            WHERE id = %(event_id)s
            AND EXISTS (
                SELECT 1
                FROM calendar_user_association
                WHERE user_id = %(user_id)s 
                AND calendar_user_association.calendar_id = calendar.id
            )
            and is_delete = FALSE
            RETURNING id, title, comment, start_time, end_time, event_status;
        """

        params = {
            "event_id": input.event_id,
            "title": input.title,
            "comment": input.comment,
            "start_time": input.start_time,
            "end_time": input.end_time,
            "event_status": input.event_status,
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
                event_status=updated_event["event_status"],
            )

        except Exception as e:
            return DatabaseError(error=str(e))
