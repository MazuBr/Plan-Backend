from typing import List

import strawberry

from src.graphql.types.users import Role
from src.graphql.mutations import Mutation

@strawberry.type
class Query:
    @strawberry.field
    def roles(self) -> List[Role]:
        return [Role(id=1, name="admin")]
    

schema = strawberry.Schema(query=Query, mutation=Mutation)