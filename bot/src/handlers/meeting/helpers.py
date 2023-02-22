from enum import Enum

from base import BaseContextManager
from schemas.responses import UserResponse
from telegram.ext import ContextTypes


class ContextKeys(str, Enum):
    USER = "USER"
    COMMENT = "COMMENT"
    MEETING_FORMAT = "MEETING_FORMAT"
    TIMESLOTS = "TIMESLOTS"
    TIMESLOT = "TIMESLOT"


class MeetingContextManager(BaseContextManager):
    def set_user(self, context: ContextTypes.DEFAULT_TYPE, user: UserResponse):
        self.set(context, ContextKeys.USER, user)

    def get_user(self, context: ContextTypes.DEFAULT_TYPE):
        return self.get(context, ContextKeys.USER)

    def get_user_id(self, context: ContextTypes.DEFAULT_TYPE):
        user_id = None
        user = self.get_user(context)
        if user and isinstance(user, dict):
            user_id = user.get("id")
        return user_id

    def set_meeting_format(self, context: ContextTypes.DEFAULT_TYPE, meeting_format: str):
        self.set(context, ContextKeys.MEETING_FORMAT, meeting_format)

    def get_meeting_format(self, context: ContextTypes.DEFAULT_TYPE):
        return self.get(context, ContextKeys.MEETING_FORMAT)

    def set_meeting_comment(self, context: ContextTypes.DEFAULT_TYPE, comment: str):
        self.set(context, ContextKeys.COMMENT, comment)

    def get_comment(self, context: ContextTypes.DEFAULT_TYPE):
        return self.get(context, ContextKeys.COMMENT)

    def set_timeslots(self, context: ContextTypes.DEFAULT_TYPE, timeslots: list):
        self.set(context, ContextKeys.TIMESLOTS, timeslots)

    def get_timeslots(self, context: ContextTypes.DEFAULT_TYPE):
        return self.get(context, ContextKeys.TIMESLOTS)

    def set_timeslot(self, context: ContextTypes.DEFAULT_TYPE, timeslot: dict):
        self.set(context, ContextKeys.TIMESLOT, timeslot)

    def get_timeslot(self, context: ContextTypes.DEFAULT_TYPE):
        return self.get(context, ContextKeys.TIMESLOT)


context_manager = MeetingContextManager()