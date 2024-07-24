from sqlalchemy import insert
import strawberry

from src.graphql.types.calendar import CalendarCreateEvent,\
    Calendar, Repeat
from src.database.postgres_connection import Database


@strawberry.type
class CreateEventMutation:
    @strawberry.mutation
    def create_event(self, input: CalendarCreateEvent) -> Calendar:
        db = Database()
        query = '''
            INSERT INTO calendar (title, comment, start_time, end_time, is_repeat, repeat_until)
            VALUES (%(title)s, %(comment)s, %(start_time)s, %(end_time)s, %(is_repeat)s, %(repeat_until)s)
            RETURNING id, title, comment, start_time, end_time, is_repeat, repeat_until;
        '''

        data = {
            'title': input.title,
            'comment': input.comment if input.comment is not None else '',
            'start_time': input.start_time,
            'end_time': input.end_time if input.end_time is not None else None,
            'is_repeat': False,
            'repeat_until': None
        }

        new_event = db.fetch_one(query=query, params=data)
        print('event1: ', new_event)
        return Calendar(
            id=new_event.get('id'),
            title=new_event.get('title'),
            comment=new_event.get('comment'),
            start_time=new_event.get('start_time'),
            end_time=new_event.get('end_time'),
            repeat=Repeat(
                is_repeat=new_event.get('is_repeat'),
                repeat_until=new_event.get('repeat_until')
            )
        )


