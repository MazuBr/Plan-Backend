import strawberry

@strawberry.type
class Role:
    id: int
    name: str

@strawberry.input
class RoleInput:
    name: str