from sqlalchemy import Column, String, Table, BigInteger, Boolean, ForeignKey

from src.database.conn.db import meta

calendar = Table('calendar', meta,
                    Column('id', BigInteger, primary_key=True),
                    Column('title', String),
                    Column('comment', String),
                    Column('start_time', BigInteger),
                    Column('end_time', BigInteger),
                    Column('is_repeat', Boolean),
                    Column('repeat_until', BigInteger),
                    )

event_user_association = Table('event_user_association', meta,
                    Column('calendar_id', BigInteger, ForeignKey('calendar.id')),
                    Column('user_id', BigInteger, ForeignKey('users.id')))