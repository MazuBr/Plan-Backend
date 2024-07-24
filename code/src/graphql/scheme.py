import strawberry
from src.graphql.mutations import Mutation
from src.graphql.queries import Query

schema = strawberry.Schema(query=Query,)
# schema = strawberry.Schema(query=Query, mutation=Mutation)
