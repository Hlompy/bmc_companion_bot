from enum import Enum


class States(str, Enum):
    TYPING_PHONE = "TYPING_PHONE"
    TYPING_FIRST_NAME = "TYPING_FIRST_NAME"
    TYPING_LAST_NAME = "TYPING_LAST_NAME"
    TYPING_AGE = "TYPING_AGE"
    TYPING_TEST_SCORE = "TYPING_TEST_SCORE"
    TYPING_COMMENT = "TYPING_COMMENT"
    TYPING_MEETING_FORMAT = "TYPING_MEETING_FORMAT"
    TYPING_TIME_SLOT = "TYPING_TIME_SLOT"
    TYPING_MEETING_SLOT = "TYPING_MEETING_SLOT"
    TYPING_MEETING_CONFIRM = "TYPING_MEETING_CONFIRM"
    TYPING_MEETING_LIST = "TYPING_MEETING_LIST"
