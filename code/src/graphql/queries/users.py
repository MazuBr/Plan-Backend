from typing import List
import strawberry
from src.graphql.types.users import Role
from src.database.postgres_connection import Database

@strawberry.type
class UsersQuery:
    @strawberry.field
    def roles(self) -> List[Role]:
        db = Database()
        query = "SELECT * FROM roles"
        db_response = db.fetch_all(query=query)
        return [Role(id=row['id'], name=row['name']) for row in db_response]
