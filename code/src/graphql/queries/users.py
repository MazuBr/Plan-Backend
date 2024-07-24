from typing import List
import strawberry
from src.graphql.types.users import Role

@strawberry.type
class UsersQuery:
    @strawberry.field
    def roles(self) -> List[Role]:
        return [Role(id=1, name="admin")]
