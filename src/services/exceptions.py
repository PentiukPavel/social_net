class NotSelf(Exception):
    def __init__(self, current_user):
        message = f"User - {current_user} is not an owner."
        super().__init__(message)


class NotInviteYourSelf(Exception):
    def __init__(self, current_user):
        message = f"User - {current_user} can't invite himself."
        super().__init__(message)


class InvalidUserId(Exception):
    def __init__(self, user_id: int):
        message = f"Wrong user id - {user_id}"
        super().__init__(message)


class AlreadyInvitated(Exception):
    def __init__(self, user_id: int):
        message = f"User - {user_id} already has been invitated"
        super().__init__(message)
