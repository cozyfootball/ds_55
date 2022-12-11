from typing import List, Dict

from aiogram import types
from aiogram.utils.exceptions import MessageCantBeDeleted

from create_bot import bot, GROUP_DS_55_ID


class Quiz:
    def __init__(self, poll_type, question, options, correct_option_id, explanation=''):
        self.poll_type: str = poll_type
        self.correct_option_id: int = correct_option_id
        self.question: str = question  # Текст вопроса
        self.explanation: str = explanation  # Текст объяснения правильного варианта
        self.options: List[str] = [*options]


async def quiz_callback(callback: types.CallbackQuery) -> None:
    try:
        await callback.message.delete()
    except MessageCantBeDeleted:
        pass

    poll_id = int(callback.data.split('@')[2])

    if callback.data.split('@')[1] == 'yes':
        quiz = quiz_db[callback.message.chat.id]
        await bot.send_poll(
            chat_id=GROUP_DS_55_ID,
            type=quiz.poll_type,
            question=quiz.question,
            explanation=quiz.explanation,
            options=quiz.options,
            correct_option_id=quiz.correct_option_id,
        )

    await bot.delete_message(callback.message.chat.id, poll_id)
    del quiz_db[callback.message.chat.id]


async def input_quiz(message: types.Message) -> None:

    quiz = Quiz(
        poll_type=message.poll.type,
        question=message.poll.question,
        explanation=message.poll.explanation,
        options=[x.text for x in message.poll.options],
        correct_option_id=message.poll.correct_option_id
    )
    quiz_db[message.chat.id] = quiz

    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Да", callback_data=f'quiz@yes@{message.message_id}')
    item2 = types.InlineKeyboardButton("Нет", callback_data=f'quiz@no@{message.message_id}')
    markup.add(item1, item2)

    await message.answer('Всё правильно? Публикуем в чате?', reply_markup=markup)


quiz_db: Dict[int, Quiz] = {}  # Словарь-хранилище для активных опросов
