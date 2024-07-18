from sqlalchemy import insert
import strawberry

from src.graphql.types.users import Role, RoleInput
from src.database.models.users import roles_table
from src.database.conn.db import engine
from strawberry.experimental.pydantic import type as pyd_type

@strawberry.type
class UserMutation:
    @strawberry.mutation
    def create_role(self, input: RoleInput) -> Role:
        # Логика создания роли
        with engine.connect() as conn:
            result = conn.execute(
                insert(roles_table).values(name=input.name).returning(roles_table.c.id, roles_table.c.name)
            )
            new_role = result.fetchone()
            return Role(id=new_role.id, name=new_role.name)
        