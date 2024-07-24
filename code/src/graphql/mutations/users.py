# from sqlalchemy import insert
# import strawberry

# from src.graphql.types.users import Role, RoleInput
# from src.database.postgres_connection import Database


# @strawberry.type
# class UserMutation:
#     @strawberry.mutation
#     def create_role(self, input: RoleInput) -> Role:
#         db = Database()
#         query = "insert into roles"
#         db_response = db.fetch_all(query=query)
#         return Role(id=new_role.id, name=new_role.name)
