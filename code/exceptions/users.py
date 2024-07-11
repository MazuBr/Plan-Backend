from fastapi import HTTPException


class UsernameAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Username already exists")


class EmailAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Email already exists")


class UnknownRegistrationErrorException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Unknown error during registration")
