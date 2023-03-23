import re

from app import schedule_service_v1, user_service_v1
from core.constants import BotState
from decorators import at, t
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from ui.buttons import BTN_START_MENU

from .enums import States
from .helpers import context_manager
from .messages import psychologist_meeting_message
from .root_handlers import back_to_start_menu


@t
def ask_for_feedback(state: str):
    @at
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        text = ""
        buttons = [[BTN_START_MENU]]
        keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
        chat_data = update.message.chat
        telegram_login = chat_data.username
        user = user_service_v1.get_user(username=telegram_login)

        if update.message.text == "Главное меню":
            text = "Выполняется переход в главное меню"
            await update.message.reply_text(text=text, reply_markup=keyboard, resize_keyboard=True)
            await back_to_start_menu(update, context)
            return BotState.END

        if user is None:
            text = "Ваших данных нет в базе"
            await update.message.reply_text(text=text, reply_markup=keyboard, resize_keyboard=True)
            await back_to_start_menu(update, context)
            return BotState.END
        meetings = schedule_service_v1.get_meetings_by_user(user_id=user.id, past="True")

        if not meetings:
            text = "У вас еще не было консультаций."
            await update.message.reply_text(text=text, reply_markup=keyboard, resize_keyboard=True)
            await back_to_start_menu(update, context)
            return BotState.END

        if state == States.TYPING_MEETING_NUMBER:
            text = (
                "Введите порядковый номер консультации, "
                "для которой хотите оставить обратную связь"
            )
            for index, meeting in enumerate(meetings):
                psychologist = user_service_v1.get_user(id=meeting.psychologist)
                meeting_format = "Online" if meeting.format == 10 else "Очно"
                add_meeting = (
                    f"\n{index + 1}. {psychologist.first_name} "
                    f"{psychologist.last_name} "
                    f"{meeting.date_start} {meeting_format}. "
                    f"Тема: {meeting.comment[:30]}"
                )
                text += add_meeting
            await update.message.reply_text(text=text, reply_markup=keyboard, resize_keyboard=True)

        elif state == States.CHECK_IS_FEEDBACK_LEFT:
            number_of_meeting = re.findall("\\d+", update.message.text) or []

            if not number_of_meeting or int(number_of_meeting[0]) > len(meetings):
                text = "Введен неправильный номер !\nНет консультации под таким номером."
                await update.message.reply_text(text=text, reply_markup=keyboard)
                return States.TYPING_MEETING_NUMBER
            meeting = meetings[int(number_of_meeting[0]) - 1] if meetings else {}
            context_manager.set_meeting(context, meeting)
            feedback = schedule_service_v1.get_feedback_by_user_and_meeting(
                user=user.id,
                meeting=meeting.id,
            )
            if feedback:
                context_manager.set_feedback(context, feedback)
                feedback_text = feedback[0].text
                text = (
                    "Вы уже оставляли обратную связь для этой встречи: \n"
                    f"{feedback_text} \n"
                    "Оставьте отзыв заново (мы обновим его)."
                    "Оцените насколько вам было комфортно на консультации:"
                )
            else:
                context_manager.set_feedback(context, feedback)
                text = "Оцените насколько вам было комфортно на консультации:"
            await update.message.reply_text(text=text, reply_markup=keyboard, resize_keyboard=True)

        elif state == States.TYPING_COMFORT_SCORE:
            score_text = update.message.text
            comfort_score = re.findall("\\d+", score_text) or []
            if not comfort_score or int(comfort_score[0]) not in range(1, 11):
                text = "Введите корректную оценку\nВведите число 1 до 10."
                await update.message.reply_text(
                    text=text, reply_markup=keyboard, resize_keyboard=True
                )
                return States.CHECK_IS_FEEDBACK_LEFT
            context_manager.set_comfort_score(context, comfort_score[0])
            text = (
                "Оцените насколько вам стало лучше после консультации от 1 до 10 \nВведите число:"
            )
            await update.message.reply_text(text=text, reply_markup=keyboard, resize_keyboard=True)

        elif state == States.TYPING_BETTER_SCORE:
            better_score = re.findall("\\d+", update.message.text) or []
            if not better_score or int(better_score[0]) not in range(1, 11):
                text = "Введите корректную оценку\nВведите число 1 до 10."
                await update.message.reply_text(
                    text=text, reply_markup=keyboard, resize_keyboard=True
                )
                return States.TYPING_COMFORT_SCORE
            context_manager.set_better_score(context, better_score[0])
            text = "Введите ваш отзыв:"
            await update.message.reply_text(text=text, reply_markup=keyboard, resize_keyboard=True)

        elif state == States.FEEDBACK_SAVED:
            context_manager.set_feedback_text(context, update.message.text)
            feedback = context_manager.get_feedback(context)
            meeting = context_manager.get_meeting(context)
            feedback_text = context_manager.get_feedback_text(context)
            text = "Спасибо за ваш отзыв."
            comfort_score = int(context_manager.get_comfort_score(context))
            better_score = int(context_manager.get_better_score(context))
            if feedback:
                schedule_service_v1.update_feedback(
                    feedback_id=feedback[0].id,
                    text=feedback_text,
                    comfort_score=comfort_score,
                    better_score=better_score,
                )
            else:
                schedule_service_v1.create_feedback(
                    meeting_id=meeting.id,
                    user_id=user.id,
                    text=feedback_text,
                    comfort_score=comfort_score,
                    better_score=better_score,
                )
            if user.id == meeting.user:
                psychologist_chat_id = user_service_v1.get_user(id=meeting.psychologist).chat_id
                meeting_format = "Онлайн" if meeting.format == 10 else "Очно"
                if psychologist_chat_id:
                    message = await psychologist_meeting_message(
                        meeting_format, user, meeting, header="Вам оставлена обратная связь:\n"
                    )
                    await context.bot.send_message(chat_id=psychologist_chat_id, text=message)
            await update.message.reply_text(text=text, reply_markup=keyboard, resize_keyboard=True)
            await back_to_start_menu(update, context)
            return BotState.END

        return state

    return inner
