from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text

from quiz.q import quiz_callback, cmd_quiz


def register_quiz_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(quiz_callback, Text(startswith=['quiz@']))
    dp.register_message_handler(cmd_quiz, chat_type='private', commands=["quiz"])
