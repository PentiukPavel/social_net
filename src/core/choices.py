from enum import IntEnum, StrEnum


class UserSex(IntEnum):
    MALE = 1
    FEMALE = 2


class APIMessages(StrEnum):
    NOT_INVITE_YOURSELF = "You can't invite yourself."
    ALREADY_INVITATED = "You have already invitaded this person."
    INVITATION_LIMIT_EXCEEDED = "Limit of invitations is exceeded."


class EmailSubject(StrEnum):
    INVITATION = "You have an invitaion."
