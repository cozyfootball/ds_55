import ast
import random
from typing import List

from aiogram import types
from aiogram.utils.exceptions import MessageCantBeDeleted

<<<<<<< HEAD
from ds_55 import bot, GROUP_DS_55_ID
=======
from create_bot import bot, GROUP_DS_55_ID
>>>>>>> bd007c7840a6d1be9595fa11ad358c2fadbcbcfb

quiz_db = {}  # Словарь-хранилище для активных опросов


class Quiz:
    type: str = "quiz"
    # question: str = ''  # Текст вопроса
    # explanation: str = ''  # Текст объяснения правильного варианта
    # options: List[str] = []

    def __init__(self, question, options, correct_option_id, explanation=''):
        self.correct_option_id: int = correct_option_id
        self.question: str = question  # Текст вопроса
        self.explanation: str = explanation  # Текст объяснения правильного варианта
        self.options: List[str] = [*options]
        self.correct_option_id: int = correct_option_id


async def cmd_quiz(message: types.Message):
    try:
        await message.delete()
    except MessageCantBeDeleted:
        pass

    if not message.get_args():
        await message.answer(
            "{'вопрос': 'ПРИМЕР', 'объяснение': 'ПРИМЕР', "
            "'неправильные варианты': ['ПРИМЕР1', 'ПРИМЕР2',], "
            "'правильный вариант': 'ПРИМЕР'}"
        )
        return

    text = message.get_args()
    try:
        dict_quiz = ast.literal_eval(text)
    except ValueError:
        print(text)
        return

    options = dict_quiz['неправильные варианты']
    options.append(dict_quiz['правильный вариант'])
    random.shuffle(options)
    correct_option_id = options.index(dict_quiz['правильный вариант'])

    quiz = Quiz(
        question=dict_quiz['вопрос'],
        explanation=dict_quiz['объяснение'],
        options=options,
        correct_option_id=correct_option_id
    )
    quiz_db[message.chat.id] = quiz

    poll = await message.answer_poll(
        question=quiz.question,
        explanation=quiz.explanation,
        options=quiz.options,
        correct_option_id=quiz.correct_option_id,
        type='quiz'
    )

    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Да", callback_data=f'quiz@yes@{poll.message_id}')
    item2 = types.InlineKeyboardButton("Нет", callback_data=f'quiz@no@{poll.message_id}')
    markup.add(item1, item2)

    await message.answer('Всё правильно? Публикуем в чате?', reply_markup=markup)


async def quiz_callback(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except MessageCantBeDeleted:
        pass
    
    poll_id = int(callback.data.split('@')[2])
    if callback.data.split('@')[1] == 'yes':
        quiz = quiz_db[callback.message.chat.id]
        await bot.send_poll(
            chat_id=GROUP_DS_55_ID,
            question=quiz.question,
            explanation=quiz.explanation,
            options=quiz.options,
            correct_option_id=quiz.correct_option_id,
            type='quiz'
        )
    else:
        await bot.delete_message(callback.message.chat.id, poll_id)

    del quiz_db[callback.message.chat.id]
