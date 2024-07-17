from fastapi import HTTPException


class UsernameAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail={'username': 'already exists'})


class EmailAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail={'email': 'already exists'})


class UnknownRegistrationErrorException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail={'error': 'unknown registration error'})
