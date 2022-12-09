from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram import types
from time import sleep
from aiogram.dispatcher.filters import CommandStart
import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher import FSMContext
import random
import sqlite3
import statistics as st
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import IsReplyFilter
from aiogram.dispatcher.filters.state import StatesGroup, State
from collections import Counter



# Базовые настройки для соединения с созданным ботом
API_TOKEN = ''
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
# Подключаемся/создаем базу данных
bd = sqlite3.connect('datasciense.db')
cur = bd.cursor()


GROUP_DS_55_ID = -1001883554676
bd.commit()
# Создаем таблицу(если её еще не существет) всех пользователей чатика. Столбцы: id, имя в чате, пол, возраст, город, репутация, библиотека-роль, о себе, почему ДС)
bd.execute('CREATE TABLE IF NOT EXISTS Users (id int NOT NULL, chat_name NULL, sex NULL, age int NULL, city NULL, rep int, libstate NULL, aself NULL, whyds NULL, PRIMARY KEY(id))')
# НЕ ПРИОРИТЕТНАЯ ЗАДАЧА Создаем таблицу данных блица, ответы будем визуализировать графиками:
bd.execute(
    'CREATE TABLE IF NOT EXISTS Blic ('
    'id int NOT NULL,'
    'cat_dog NULL, '
    'pizza_suchi NULL, '
    'sea_mount NULL, '
    'flat_house NULL, '
    'train_plain NULL, '
    'tea_coffe NULL, '
    'tv_tube NULL, '
    'andr_ios NULL,  '
    'tatoo NULL, '
    'drive NULL, '
    'parent_kid NULL, '
    'films NULL, '
    'melody NULL, '
    'knigas NULL, '
    'PRIMARY KEY(id))')
bd.execute('CREATE TABLE IF NOT EXISTS Base (id NOT NULL, name NULL, desc NULL, fullv NULL, args NULL, example NULL, dopinfo NULL, erors NULL, meth_args NULL, cat1 NULL, cat2 NULL, cat3 NULL, file NULL, PRIMARY KEY(id))')
# команда подтверждающая изменения в БД
bd.commit()

# инлайн кнопки для основного меню и реакцию на старт
button1 = InlineKeyboardButton(text='ПРОФИЛЬ🧐', callback_data='profile')
button2 = InlineKeyboardButton(text='БЛИЦ🧾', callback_data='blic')
button3 = InlineKeyboardButton(text='СКЛАД ДС💌', callback_data='base')
button4 = InlineKeyboardButton(text='ОСНОВНОЕ МЕНЮ', callback_data='menu')


class Profile(StatesGroup):
    ProfileSex = State()
    ProfileAge = State()
    ProfileCity = State()
    ProfileAself = State()
    ProfileWhyDs = State()
class Blic(StatesGroup):
    cat_dog = State()
    pizza_suchi = State()
    sea_mount = State()
    flat_house = State()
    train_plain = State()
    tea_coffe = State()
    tv_tube = State()
    andr_ios = State()
    tatoo = State()
    drive = State()
    parent_kid = State()
    music = State()
    films = State()
    books = State()
@dp.message_handler(CommandStart())
async def first_step(message: types.Message):
    user_id = message.from_user.id
    fellows = cur.execute('SELECT id FROM Users').fetchall()
    fellows_list = [x[0] for x in fellows]
    main_menu = InlineKeyboardMarkup(row_width=2)
    main_menu.insert(button1)
    main_menu.insert(button2)
    # MainMenu.insert(button3)
    await bot.send_sticker(
        chat_id=message.chat.id,
        sticker="CAACAgIAAxkBAAEGt_ZjkD9sRrXH8R2XpQsYpRyafOfHJAACphgAAhRjYUrTgchlOAQs7ysE"
    )
    if user_id in fellows_list:
        # получим ник, который он указал при заполнении профиля
        # переменная с текстовым сообщением приветствием
        fellow_message = f'Рад снова тебя видеть, {message.from_user.first_name}. Нас уже {len(fellows_list)}'
        # сама реакция, бот отвечает приветственным сообщением
        # Объект message имеет много методов. Проще их использовать. Пока здесь только исправлю
        await bot.send_message(chat_id=user_id, text=fellow_message, parse_mode="MarkDown", reply_markup=main_menu)
        # получим информацию участвовал ли этот юзер в блице
        victory_id = cur.execute('SELECT id FROM Blic').fetchall()
        victory_id_list = [x[0] for x in victory_id]
        # сценарий если участвовал
        if user_id in victory_id_list:
            good_person = f'Твой профиль заполнен и ты прошёл блиц. Давай обнимися, что ли? Золотый ты человечек'
            await  bot.send_message(chat_id=user_id, text=good_person, parse_mode="MarkDown")
        # сценарий если не участвовал
        elif user_id not in victory_id_list:
            vitctorina_user = f'Твой профиль заполнен, но ты не прошёл викторину. ' \
                              f'Пройди, когда будет время. Мне нужны данные для настоящего *Data Science*'
            await bot.send_message(chat_id=user_id, text=vitctorina_user, parse_mode="MarkDown", reply_markup=main_menu)
        # ловим ошибку
        else:
            await message.answer(text='Ошибка, напиши моим авторам')
    # напишем сценарий для случаев, если юзер не в базе
    elif user_id not in fellows_list:
        welcome = (f'Привяу, я Староста.\n'
                   f'Я много учился раньше, а сейчас помогаю тем, кто учится прямо сейчас. Кстати благодаря курсу я нашёл {len(fellows_list)} друзей.\nНажми кнопку "ПРОФИЛЬ" чтобы рассказать чуть больше о себе\n'
                   f'Еще я провожу мини-исследования. Нажми кнопку "БЛИЦ", чтобы ответить на небольшой блиц и поделиться рекомендациями по фильмам, книгам, музыке\n')
        cur.execute('INSERT INTO Users(id, rep) VALUES(?, ?)', (user_id, 0))
        bd.commit()
        await bot.send_message(chat_id=user_id, text=welcome, parse_mode="MarkDown", reply_markup=main_menu)

# Заготовка для работы непосредственно с библиотекой. Недоработана
@dp.callback_query_handler(text='base')
async def myfunc(call):
    funcs = cur.execute('SELECT func FROM Base WHERE func NOT NULL').fetchall()
    funcs_list = [x[0] for x in funcs]
    buttonb1 = InlineKeyboardButton(text='СПИСОК', callback_data='funlis')
    buttonb2 = InlineKeyboardButton(text='ДОБАВИТЬ', callback_data='addfun')
    base_menu = InlineKeyboardMarkup(row_width=2)
    base_menu.insert(buttonb1)
    base_menu.insert(buttonb2)
    base_mes = f'Это библиотека полезных функций. Сейчас в библиотеке {len(funcs_list)} функций. ' \
               f'Нажми "СПИСОК" чтобы посмотреть библиотеку. ' \
               f'Нажми "ДОБАВИТЬ" чтобы добавить информацию по новой функции'
    await bot.send_message(chat_id=call.from_user.id, text=base_mes, parse_mode="MarkDown")

# Заготовка для реакции на кнопку СПИСОК
# Пусть пока закоментированы будут, чтобы лишних ошибок не было
# @dp.callback_query_handler(text='funlis')
# async def funlist(call):
#     funcs = cur.execute('SELECT func FROM Base WHERE func NOT NULL').fetchall()
#     funcs_list = [x[0] for x in funcs]
#     await bot.send_message(chat_id=call.from_user.id, text=funcs_list, parse_mode="MarkDown", reply_markup=BaseMenu)

# Заготовка для реакции на кнопку ДОБАВИТЬ
# @dp.callback_query_handler(text='addfun')
# async def addfun(call):
#     funcs = cur.execute('SELECT func FROM Base WHERE func NOT NULL').fetchall()
#     funcs_list = [x[0] for x in funcs]
#     await bot.send_message(chat_id=call.from_user.id, text=funcs_list, parse_mode="MarkDown", reply_markup=BaseMenu)


@dp.callback_query_handler(text='profile')
async def pro_file(call):
    user_id = call.from_user.id
    myprofile = cur.execute('SELECT sex FROM Users WHERE id=' + str(user_id)).fetchone()
    mycheck = cur.execute('SELECT * FROM Users WHERE id=' + str(user_id)).fetchone()
    button11 = InlineKeyboardButton(text='Заполнить профиль', callback_data='addprofile')
    if myprofile is not None:
        myinfo = (
            f'*Карточка начинающего ДСера*\n'
            f'*Позывной*: {mycheck[1]}\n'
            f'*Пол*: {mycheck[2]}\n'
            f'*Возраст*: {mycheck[3]}\n'
            f'*Город*: {mycheck[4]}\n'
            f'*Репутация*: {mycheck[5]}\n'
            f'*О себе*:{mycheck[7]}\n'
            f'*Почему DS*: {mycheck[8]}\n'
        )
        profile_menu = InlineKeyboardMarkup(row_width=2)
        profile_menu.insert(button11)
        profile_menu.insert(button4)
        await bot.send_message(chat_id=user_id, text=myinfo, parse_mode="MarkDown", reply_markup=profile_menu)
    elif myprofile is None:
        profile_menu1 = InlineKeyboardMarkup(row_width=2)
        profile_menu1.insert(button11)
        profile_menu1.insert(button4)
        await bot.send_message(
            chat_id=call.from_user.id, 
            text='Сделай доброе DS-дело, хороший человек, заполни профиль!', 
            parse_mode="MarkDown", reply_markup=profile_menu1
        )
    await bot.send_message(chat_id=user_id, text="Чтобы посмотреть профиль юзера, напиши в ответ на любое его сообщение 'профиль'", parse_mode="MarkDown")

@dp.callback_query_handler(text='addprofile')
async def addprofile_new(call):
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    profile_sex = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text='Мужской🧔🏻‍♂️', callback_data='iman')
    button2 = InlineKeyboardButton(text='Женский👩🏻‍🦰', callback_data='iwomen')
    button3 = InlineKeyboardButton(text='Другой🧌', callback_data='inone')
    profile_sex.insert(button1)
    profile_sex.insert(button2)
    profile_sex.insert(button3)
    await bot.send_message(
        chat_id=user_id, 
        text='Чудесно, актуальная информация - клад для молодого DS-ера. '
             'Сейчас я задам тебе несколько вопросов. Сначала укажи свой пол', 
        parse_mode="MarkDown",  reply_markup=profile_sex
    )
    await Profile.ProfileSex.set()
    cur.execute('UPDATE Users SET chat_name == ? WHERE id == ?', (user_name, user_id))
    bd.commit()


@dp.callback_query_handler(text=['iman', 'iwomen', 'inone'], state=Profile.ProfileSex)
async def sex_age(call, state: FSMContext):
    user_id = call.from_user.id
    age_quest = f'С этим все ясно. Теперь мне нужен твой возраст. Напиши его в сообщении'
    if call.data == 'iman':
        cur.execute('UPDATE Users SET sex == ? WHERE id == ?', ('man', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest)
        await Profile.ProfileAge.set()
    elif call.data == 'iwomen':
        cur.execute('UPDATE Users SET sex == ? WHERE id == ?', ('woman', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest)
        await Profile.ProfileAge.set()
    elif call.data == 'inone':
        cur.execute('UPDATE Users SET sex == ? WHERE id == ?', ('noone', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest)
        await Profile.ProfileAge.set()


@dp.message_handler(state=Profile.ProfileAge)
async def age_city(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    mes = message.text
    if mes.isdigit():
        if 18 < int(mes) < 88:
            cur.execute('UPDATE Users SET age == ? WHERE id == ?', (mes, user_id))
            bd.commit()
            await bot.send_message(
                chat_id=user_id,
                text='Хорошо, теперь напиши из какого ты города'
            )
            await Profile.ProfileCity.set()
        else:
            await bot.send_message(chat_id=user_id,
                                   text='Сомневаюсь, что тебе меньше 19 и больше 88. Может ты опечатался?')
    else:
        await bot.send_message(chat_id=user_id,
                               text='Пришли свою настоящую цифру')

@dp.message_handler(state=Profile.ProfileCity)
async def city_aself(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    mes = message.text
    if 3 < len(mes) < 35:
        cur.execute('UPDATE Users SET city == ? WHERE id == ?', (mes, user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text='Пару слов о себе')
        await Profile.ProfileAself.set()
    else:
        await bot.send_message(chat_id=user_id,
                               text='Что за город такой? Выдуманный чтоли?')

@dp.message_handler(state=Profile.ProfileAself)
async def aself_ds(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    mes = message.text
    if 5 < len(mes) < 228:
        cur.execute('UPDATE Users SET aself == ? WHERE id == ?', (mes, user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text='Ну и финалочка. Почему выбрал/выбрала DS?')
        await Profile.ProfileWhyDs.set()
    else:
        await bot.send_message(chat_id=user_id,
                               text='Надо написать хоть то-то дельное')

@dp.message_handler(state=Profile.ProfileWhyDs)
async def my_ds(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    mes = message.text
    if 5 < len(mes) < 228:
        cur.execute('UPDATE Users SET whyds == ? WHERE id == ?', (mes, user_id))
        bd.commit()
        await state.reset_state()
        mycheck = cur.execute('SELECT * FROM Users WHERE id=' + str(user_id)).fetchone()
        myinfo = (
            f'*Карточка начинающего ДСера*\n'
            f'*Позывной*: {mycheck[1]}\n'
            f'*Пол*: {mycheck[2]}\n'
            f'*Возраст*: {mycheck[3]}\n'
            f'*Город*: {mycheck[4]}\n'
            f'*Репутация*: {mycheck[5]}\n'
            f'*О себе*:{mycheck[7]}\n'
            f'*Почему DS*: {mycheck[8]}\n'
        )
        await bot.send_message(chat_id=user_id, text=myinfo, parse_mode="MarkDown")
    else:
        await bot.send_message(chat_id=user_id,
                               text='Надо написать хоть то-то дельное')

@dp.message_handler(IsReplyFilter(is_reply=True))
async def print_func(message: types.Message):
    message_lower = message.text.lower()
    rep_id = message.reply_to_message.from_user.id
    rep_name = message.reply_to_message.from_user.first_name
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    mention_rep = "[" + rep_name + "](tg://user?id=" + str(rep_id) + ")"
    if message.from_user.id == 840994663:
        sleep(3)
        maga_phrase = ['Ну что сказать, ну что сказать, человек мой дорогой?',
                       'КВН заказывали?',
                       'Да ты мне не рассказывай, ты им рассказывай',
                       'Cмекаешь?',
                       'Ты тут самый крутой',
                       'Может посплетничаем?',
                       'Любишь кататься - люби и катайся',
                       'Вообще-то да',
                       'Еще чего, какие глупости',
                       'Посветуй фильмец какой-нибудь'
                       'Где сейчас можно недорого отдохнуть?',
                       'Как я тебя понимаю'
                       'Ну вот и я о том же',
                       'А можно тост?']
        forfun = random.choice(maga_phrase)
        await message.answer(
            text=forfun, parse_mode="MarkDown")
    elif message_lower.find('пасиб') > -1 or message_lower.find('лагодар') > -1:
        if user_id == rep_id:
            await message.answer(
                text=f'{mention_rep} ты так-то человечек хороший. Все это уже поняли. Может про DS что нить накидаешь?',
                parse_mode="MarkDown")
        elif user_id != rep_id:
            user_rate_cur = cur.execute('SELECT rep FROM Users WHERE id=' + str(rep_id)).fetchone()
            if not user_rate_cur:
                await message.answer(
                    text=f'{rep_name}, к сожалению, я тебя знаю и не могу повысить твою репутацию. '
                         f'Напиши /start, чтобы это исправить',
                    parse_mode="MarkDown"
                )
            elif user_rate_cur[0] >= 0:
                user_rate_fin = user_rate_cur[0] + 1
                funfact = ['приятный человек.',
                           'мудрый собеседник.'
                           'всегда умеет найти правильные слова.',
                           'человек с большой буквЫ.',
                           'наиприятнейшая личность в контексте DS',
                           'цветок добра',
                           'расшарил(а) мудрость',
                           'авторитетен и ТОЧКА',
                           'задаёт хороший тон',
                           'умеет делать красиво',
                           'выручил на пятерочку. Ай молодца!',
                           'продолжает хорошую традицию',
                           'благоприятно влияет на общий фон.',
                           'хорошо умеет принимать благодароность.',
                           'однозначно личность часа.']
                forfun = random.choice(funfact)
                await message.answer(
                    text=f' {mention_rep} {forfun}.\n+1 в твою личную *коллекцию благодарностей*.'
                         f'\n*Уровень* коллективной благодарности: {user_rate_fin} ⭐️',
                    parse_mode="MarkDown"
                )
                cur.execute('UPDATE Users SET rep == ? WHERE id == ?', (user_rate_fin, rep_id))
                bd.commit()
    elif message_lower.find('профил') > -1:
        mycheck = cur.execute('SELECT * FROM Users WHERE id=' + str(rep_id)).fetchone()
        if not mycheck[4]:
            await message.answer(
                text=f'{rep_name} пока еще не чувствует себя ДСером, '
                     f'у него нет профиля и ему нечего рассказывать о себе',
                parse_mode="MarkDown")

        elif len(mycheck[7]) >= 3:
            myinfo = (
                f'*Профиль {rep_name}*\n'
                f'*Позывной*: {mycheck[1]}\n'
                f'*Пол*: {mycheck[2]}\n'
                f'*Возраст*: {mycheck[3]}\n'
                f'*Город*: {mycheck[4]}\n'
                f'*Репутация*: {mycheck[5]}\n'
                f'*О себе*:{mycheck[7]}\n'
                f'*Почему DS*: {mycheck[8]}\n'
            )
            await bot.send_message(chat_id=message.from_user.id, text=myinfo, parse_mode="MarkDown")
            await message.delete()

    elif message_lower.find('пока') > -1:
        await bot.send_sticker(
            chat_id=GROUP_DS_55_ID,
            sticker="CAACAgIAAxkBAAEGvlZjkluuNc9rcXyHz2CfH5v4Tgs6HQACtBQAAtdB - UrTW2cy7dEMQysE"
        )
    elif message.reply_to_message.from_user.is_bot:
        sleep(2)
        all_phrases = ['Ну что сказать, ну что сказать, человек мой дорогой?',
                       'Точное время 4 часа 20 минут',
                       'Да ты мне не рассказывай, ты им рассказывай',
                       'А вот эту мудрость мы поставим под сомнение',
                       'А что если я Робокот или Робокоп?',
                       'Уважьте меня кто-нибудь',
                       'Какова твоя нулевая гипотеза?',
                       'По статистике каждый ДСер еще тот аналитик',
                       'Как-то раз заснул и сниться мне p-value',
                       'Ну вот скажи, мне студент, в чем сила?',
                       'Улыбайтесь — это всех раздражает!',
                       'Ты тут кого-нибудь знаешь? Им можно доверять?',
                       'Я импортозамещеный искуственный интеллект. Прекол?',
                       'Мудрость не всегда приходит с возрастом. Бывает, что возраст приходит один.',
                       'В тюрьме столько не сидят, сколько вы в интернете',
                       'Если Вас окружают одни дураки, значит Вы центральный.',
                       'Как сделать хорошо? Сделать плохо, а потом так же, как было.',
                       'Лучше переспать, чем недоесть.',
                       'Каждый человек по-своему прав, а по-моему — нет',
                       'А вот и Data-бродяга science-симпатяга',
                       'Милейший ты мой',
                       'Я щас закончу вообще всё!',
                       'Не бери в голову',
                       'Иногда приходиться прикинуться дурачком, чтобы не выглядеть идиотом']
        forfun = random.choice(all_phrases)
        await message.answer(text=forfun, parse_mode="MarkDown")

# Новичок в группе
@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_member(message):
    await message.answer(f"У нас пополнение - {message.new_chat_members[0].get_mention(as_html=True)}. Вкратце расскажи про свой путь DSeра, нам реально интересно", parse_mode='HTML')
    await bot.send_sticker(chat_id=message.chat.id, sticker='CAACAgIAAxkBAAEGl9tjhNncRF99x78OPh02Wk6byzBeEgACXgwAApS4UEtOn6EuKYdYXisE')

# Заготовка для реакции на кнопку БЛИЦ
@dp.callback_query_handler(text='blic')
async def my_blic(call):
    user_id = call.from_user.id
    mypvic = cur.execute('SELECT id FROM Blic').fetchall()
    mypvic_list = [x[0] for x in mypvic]
    button11 = InlineKeyboardButton(text='Пройти БЛИЦ', callback_data='addvictory')
    if user_id in mypvic_list:
        mypvic = cur.execute('SELECT * FROM Blic WHERE id=' + str(user_id)).fetchone()
        myansw = (f'*Мои ответы на викторину:\n'
                  f'Кошки/собаки: {mypvic[1]}\n'
                  f'Пицца/суши: {mypvic[2]}\n'
                  f'Море/горы: {mypvic[3]}\n'
                  f'Квартира/дом: {mypvic[4]}\n'
                  f'Самолет/поезд:{mypvic[5]}\n'
                  f'Чай/кофе: {mypvic[6]}\n'
                  f'ТВ/Youtube: {mypvic[7]}\n'
                  f'Андроид/ios: {mypvic[8]}\n'
                  f'Татуировки: {mypvic[9]}\n'
                  f'Водительство: {mypvic[10]}\n'
                  f'Родительство: {mypvic[11]}\n'
                  f'Мои фильмы: {mypvic[12]}\n'
                  f'Моя музыка: {mypvic[13]}\n'
                  f'Мои книги: {mypvic[14]}\n*')
        victorina_menu = InlineKeyboardMarkup(row_width=2)
        victorina_menu.insert(button11)
        victorina_menu.insert(button4)
        await bot.send_message(chat_id=call.from_user.id, text=myansw, parse_mode="MarkDown", reply_markup=victorina_menu)
    elif user_id not in mypvic_list:
        user_id = call.from_user.id
        victorina_menu1 = InlineKeyboardMarkup(row_width=2)
        victorina_menu1.insert(button11)
        victorina_menu1.insert(button4)
        await bot.send_message(chat_id=call.from_user.id, text='Ты еще не прошёл викторину. Сейчас готов?', parse_mode="MarkDown", reply_markup=victorina_menu1)
        cur.execute('INSERT INTO Blic(id, knigas) VALUES(?, ?)', (user_id, 0))
        bd.commit()


@dp.callback_query_handler(text='addvictory')
async def addvictory(call):
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    vic_q1 = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text='🐈', callback_data='cat')
    button2 = InlineKeyboardButton(text='🐕‍🦺', callback_data='dog')
    vic_q1.insert(button1)
    vic_q1.insert(button2)
    await bot.send_message(
        chat_id=user_id,
        text='Кошки или Собаки?', parse_mode="MarkDown",  reply_markup=vic_q1)
    await Blic.cat_dog.set()

@dp.callback_query_handler(text=['cat', 'dog'], state=Blic.cat_dog)
async def cat_dog(call, state: FSMContext):
    user_id = call.from_user.id
    age_quest = f'Пицца или суши?'
    vic_q2 = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text='🍕', callback_data='pizza')
    button2 = InlineKeyboardButton(text='🍣', callback_data='suchi')
    vic_q2.insert(button1)
    vic_q2.insert(button2)
    if call.data == 'cat':
        cur.execute('UPDATE Blic SET cat_dog == ? WHERE id == ?', ('🐈', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q2)
        await Blic.pizza_suchi.set()
    elif call.data == 'dog':
        cur.execute('UPDATE Blic SET cat_dog == ? WHERE id == ?', ('🐕‍🦺', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q2)
        await Blic.pizza_suchi.set()
@dp.callback_query_handler(text=['pizza', 'suchi'], state=Blic.pizza_suchi)
async def pizza_suchi(call, state: FSMContext):
    user_id = call.from_user.id
    age_quest = f'Море или горы?'
    vic_q3 = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text='🏖', callback_data='sea')
    button2 = InlineKeyboardButton(text='🏔', callback_data='mount')
    vic_q3.insert(button1)
    vic_q3.insert(button2)
    if call.data == 'pizza':
        cur.execute('UPDATE Blic SET pizza_suchi == ? WHERE id == ?', ('🍕', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q3)
        await Blic.sea_mount.set()
    elif call.data == 'suchi':
        cur.execute('UPDATE Blic SET pizza_suchi == ? WHERE id == ?', ('🍣', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q3)
        await Blic.sea_mount.set()

@dp.callback_query_handler(text=['sea', 'mount'], state=Blic.sea_mount)
async def sea_mount(call, state: FSMContext):
    user_id = call.from_user.id
    age_quest = f'Квартира или дом?'
    vic_q4 = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text='🏢', callback_data='flat')
    button2 = InlineKeyboardButton(text='🏡', callback_data='house')
    vic_q4.insert(button1)
    vic_q4.insert(button2)
    if call.data == 'sea':
        cur.execute('UPDATE Blic SET sea_mount == ? WHERE id == ?', ('🏖', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q4)
        await Blic.flat_house.set()
    elif call.data == 'mount':
        cur.execute('UPDATE Blic SET sea_mount == ? WHERE id == ?', ('🏔', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q4)
        await Blic.flat_house.set()

@dp.callback_query_handler(text=['flat', 'house'], state=Blic.flat_house)
async def flat_house(call, state: FSMContext):
    user_id = call.from_user.id
    age_quest = f'Самолет или поезд?'
    vic_q5 = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text='🚂', callback_data='train')
    button2 = InlineKeyboardButton(text='✈', callback_data='plain')
    vic_q5.insert(button1)
    vic_q5.insert(button2)
    if call.data == 'flat':
        cur.execute('UPDATE Blic SET flat_house == ? WHERE id == ?', ('🏢', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q5)
        await Blic.train_plain.set()
    elif call.data == 'house':
        cur.execute('UPDATE Blic SET flat_house == ? WHERE id == ?', ('🏡', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q5)
        await Blic.train_plain.set()
@dp.callback_query_handler(text=['train', 'plain'], state=Blic.train_plain)
async def train_plain(call, state: FSMContext):
    user_id = call.from_user.id
    age_quest = f'Чай или кофе?'
    vic_q6 = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text='🫖', callback_data='tea')
    button2 = InlineKeyboardButton(text='☕️', callback_data='coffe')
    vic_q6.insert(button1)
    vic_q6.insert(button2)
    if call.data == 'train':
        cur.execute('UPDATE Blic SET train_plain == ? WHERE id == ?', ('🚂', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q6)
        await Blic.tea_coffe.set()
    elif call.data == 'plain':
        cur.execute('UPDATE Blic SET train_plain == ? WHERE id == ?', ('✈️', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q6)
        await Blic.tea_coffe.set()

@dp.callback_query_handler(text=['tea', 'coffe'], state=Blic.tea_coffe)
async def tea_coffe(call, state: FSMContext):
    user_id = call.from_user.id
    age_quest = f'Телевизор или Youtube?'
    vic_q7 = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text='📺', callback_data='tv')
    button2 = InlineKeyboardButton(text='🖥', callback_data='tube')
    vic_q7.insert(button1)
    vic_q7.insert(button2)
    if call.data == 'tea':
        cur.execute('UPDATE Blic SET tea_coffe == ? WHERE id == ?', ('🫖', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q7)
        await Blic.tv_tube.set()
    elif call.data == 'coffe':
        cur.execute('UPDATE Blic SET tea_coffe == ? WHERE id == ?', ('☕️️', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q7)
        await Blic.tv_tube.set()
@dp.callback_query_handler(text=['tv', 'tube'], state=Blic.tv_tube)
async def tv_tube(call, state: FSMContext):
    user_id = call.from_user.id
    age_quest = f'Android или iPhone?'
    vic_q8 = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text='📱ios', callback_data='and')
    button2 = InlineKeyboardButton(text='📵android', callback_data='ios')
    vic_q8.insert(button1)
    vic_q8.insert(button2)
    if call.data == 'tv':
        cur.execute('UPDATE Blic SET tv_tube == ? WHERE id == ?', ('📺', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q8)
        await Blic.andr_ios.set()
    elif call.data == 'tube':
        cur.execute('UPDATE Blic SET tv_tube == ? WHERE id == ?', ('🖥️', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q8)
        await Blic.andr_ios.set()
@dp.callback_query_handler(text=['and', 'ios'], state=Blic.andr_ios)
async def tatoo(call, state: FSMContext):
    user_id = call.from_user.id
    age_quest = f'Есть татуировки?'
    vic_q9 = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text='✅', callback_data='yes_tatoo')
    button2 = InlineKeyboardButton(text='⛔️', callback_data='no_tatoo')
    vic_q9.insert(button1)
    vic_q9.insert(button2)
    if call.data == 'and':
        cur.execute('UPDATE Blic SET andr_ios == ? WHERE id == ?', ('📱ios', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q9)
        await Blic.tatoo.set()
    elif call.data == 'ios':
        cur.execute('UPDATE Blic SET andr_ios == ? WHERE id == ?', ('📵android', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q9)
        await Blic.tatoo.set()
@dp.callback_query_handler(text=['yes_tatoo', 'no_tatoo'], state=Blic.tatoo)
async def drive(call, state: FSMContext):
    user_id = call.from_user.id
    age_quest = f'Водишь машину?'
    vic_q10 = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text='✅', callback_data='yes_drive')
    button2 = InlineKeyboardButton(text='⛔️', callback_data='no_drive')
    vic_q10.insert(button1)
    vic_q10.insert(button2)
    if call.data == 'yes_tatoo':
        cur.execute('UPDATE Blic SET tatoo == ? WHERE id == ?', ('✅', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q10)
        await Blic.drive.set()
    elif call.data == 'no_tatoo':
        cur.execute('UPDATE Blic SET tatoo == ? WHERE id == ?', ('⛔️', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q10)
        await Blic.drive.set()
@dp.callback_query_handler(text=['yes_drive', 'no_drive'], state=Blic.drive)
async def parent_kid(call, state: FSMContext):
    user_id = call.from_user.id
    age_quest = f'Есть дети?'
    vic_q11 = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text='✅', callback_data='yes_kid')
    button2 = InlineKeyboardButton(text='⛔️', callback_data='no_kid')
    vic_q11.insert(button1)
    vic_q11.insert(button2)
    if call.data == 'yes_drive':
        cur.execute('UPDATE Blic SET drive == ? WHERE id == ?', ('✅', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q11)
        await Blic.parent_kid.set()
    elif call.data == 'no_drive':
        cur.execute('UPDATE Blic SET drive == ? WHERE id == ?', ('⛔️', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q11)
        await Blic.parent_kid.set()
@dp.callback_query_handler(text=['yes_kid', 'no_kid'], state=Blic.parent_kid)
async def films(call, state: FSMContext):
    user_id = call.from_user.id
    age_quest = f'Порекомендуй 3 фильма/сериала сокурсникам'
    if call.data == 'yes_kid':
        cur.execute('UPDATE Blic SET parent_kid == ? WHERE id == ?', ('✅', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest)
        await Blic.films.set()
    elif call.data == 'no_kid':
        cur.execute('UPDATE Blic SET parent_kid == ? WHERE id == ?', ('⛔️', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest)
        await Blic.films.set()
@dp.message_handler(state=Blic.films)
async def films(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    mes = message.text
    cur.execute('UPDATE Blic SET films == ? WHERE id == ?', (mes, user_id))
    bd.commit()
    await bot.send_message(chat_id=user_id,
                               text='Порекомендуй 3 музыкальных трека/группы сокурсникам')
    await Blic.music.set()
@dp.message_handler(state=Blic.music)
async def music(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    mes2 = message.text
    cur.execute('UPDATE Blic SET melody == ? WHERE id == ?', (mes2, user_id))
    bd.commit()
    await bot.send_message(chat_id=user_id,
                               text='Порекомендуй 3 книги сокурсникам')
    await Blic.books.set()


@dp.message_handler(state=Blic.books)
async def books(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    mes = message.text
    cur.execute('UPDATE Blic SET knigas == ? WHERE id == ?', (mes, user_id))
    bd.commit()
    mypvic = cur.execute('SELECT * FROM Blic WHERE id=' + str(user_id)).fetchone()
    myansw = (f'*Мои ответы на викторину*:\n'
              f'*Кошки/собаки*: {mypvic[1]}\n'
              f'*Пицца/суши*: {mypvic[2]}\n'
              f'*Море/горы*: {mypvic[3]}\n'
              f'*Квартира/дом*: {mypvic[4]}\n'
              f'*Самолет/поезд*:{mypvic[5]}\n'
              f'*Чай/кофе*: {mypvic[6]}\n'
              f'*ТВ/Youtub*: {mypvic[7]}\n'
              f'*Андроид/ios*: {mypvic[8]}\n'
              f'*Татуировки*: {mypvic[9]}\n'
              f'*Водительство*: {mypvic[10]}\n'
              f'*Родительство*: {mypvic[11]}\n'
              f'*Мои фильмы*: {mypvic[12]}\n'
              f'*Моя музыка*: {mypvic[13]}\n'
              f'*Мои книги*: {mypvic[14]}\n')
    victorina_menu = InlineKeyboardMarkup(row_width=2)
    victorina_menu.insert(button4)
    await bot.send_message(chat_id=user_id,
                           text=myansw, reply_markup=victorina_menu)

    await state.reset_state()
# Реакция на кнопку возврата в основное меню(клавиатура)
@dp.callback_query_handler(text='menu')
async def menu(call):
    main_menu = InlineKeyboardMarkup(row_width=2)
    main_menu.insert(button1)
    main_menu.insert(button2)
    await bot.send_message(
        chat_id=call.from_user.id,
        text='ОСНОВНОЕ МЕНЮ',
        parse_mode="MarkDown",
        reply_markup=main_menu
    )
class IsVIP(BoundFilter):
    async def check(self, call) -> bool:
        if call.from_user.id in mykings:
            return True

mykings= []
kingmes = []
@dp.message_handler(text='55')
async def test_your_luck(message: types.Message):
    user_id = message.from_user.id
    fellows = cur.execute('SELECT id FROM Users WHERE rep > 0').fetchall()
    fellows_list = [x[0] for x in fellows]
    fellows2 = cur.execute('SELECT id FROM Blic').fetchall()
    fellows_list2 = [x[0] for x in fellows2]
    final_fellows = fellows_list2 + fellows_list
    for i in fellows_list:
            mykings.append(i)
    for i in fellows_list2:
            mykings.append(i)

    if user_id in fellows_list and user_id in fellows_list2:
        button21 = InlineKeyboardButton(text='DS Истина👏🏻', callback_data='mytrue')
        button22 = InlineKeyboardButton(text='Типичный DS🧐', callback_data='myfact')
        button23 = InlineKeyboardButton(text='Наш коллектив👨‍👩‍👦‍👦', callback_data='mycom')
        button24 = InlineKeyboardButton(text='Наша музыка🎼', callback_data='mymusic')
        button25 = InlineKeyboardButton(text='Наши фильмы🎥', callback_data='myfilms')
        button26 = InlineKeyboardButton(text='Наши книги📓', callback_data='mybooks')
        button27 = InlineKeyboardButton(text='Наша репутация🔝', callback_data='myreput')
        luck = InlineKeyboardMarkup(row_width=2)
        luck.insert(button21)
        luck.insert(button22)
        luck.insert(button23)
        luck.insert(button24)
        luck.insert(button25)
        luck.insert(button26)
        luck.insert(button27)
        mymes = await bot.send_message(
            chat_id=GROUP_DS_55_ID,
            text='Пришло время поделиться истиной.🪙',
            parse_mode="MarkDown",
            reply_markup=luck
        )
        kingmes.clear()
        kingmes.append(mymes.message_id)

    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text='Прости, но ларец с мудростями доступен только ДС-личностей(заполненные: профиль+блиц).'
        )



@dp.callback_query_handler(text='myfact')
async def myfact_func(call):
    all_anim = cur.execute('SELECT cat_dog  FROM Blic').fetchall()
    base_list = [x[0] for x in all_anim]
    counter_animals = Counter(base_list)
    all_animals = counter_animals.get('🐈') + counter_animals.get('🐕\u200d🦺')
    cats_perc = round(counter_animals.get('🐈') / all_animals * 100, 3)
    dogs_perc = round(counter_animals.get('🐕\u200d🦺') / all_animals * 100, 3)
    animal_q = (f'Любители шерстянкых товарищей на месте? Результаты честных выборов\n'
                f'🐈Партия любителей кошек -*{cats_perc}%*🐈\n'
                f'🐕\u200d🦺Партия любителей собак - *{dogs_perc}%*🐕\u200d🦺')


    all_e = cur.execute('SELECT pizza_suchi FROM Blic').fetchall()
    base_list_ps = [x[0] for x in all_e]
    counter_eat = Counter(base_list_ps)
    all_eat = counter_eat.get('🍣') + counter_eat.get('🍕')
    pizza_perc = round(counter_eat.get('🍕') / all_eat * 100, 3)
    suchi_perc = round(counter_eat.get('🍣') / all_eat * 100, 3)
    eat_q = (f'Любители пощекотать вкусовые рецепторы на месте? Результаты честных выборов\n'
                f'🍣Партия любителей есть палочками - *{pizza_perc}%🍣*\n'
                f'🍕Партия любителей есть руками - *{suchi_perc}%🍕*')

    all_seamou = cur.execute('SELECT sea_mount FROM Blic').fetchall()
    base_list_sm = [x[0] for x in all_seamou]
    counter_sm = Counter(base_list_sm)
    all_seamount = counter_sm.get('🏖') + counter_sm.get('🏔')
    sea_perc = round(counter_sm.get('🏖') / all_seamount * 100, 3)
    mount_perc = round(counter_sm.get('🏔') / all_seamount * 100, 3)
    seam_q = (f'Любители хорошо отдохнуть? Результаты честных выборов\n'
                f'🏖Партия любителей морского воздуха - *{sea_perc}%*🏖\n'
                f'🏔Партия любителей горного воздуха - *{mount_perc}%*🏔')

    all_flh = cur.execute('SELECT flat_house FROM Blic').fetchall()
    base_list_fh = [x[0] for x in all_flh]
    counter_fh = Counter(base_list_fh)
    all_flathouse = counter_fh.get('🏡') + counter_fh.get('🏢')
    home_perc = round(counter_fh.get('🏡') / all_flathouse * 100, 3)
    flat_perc = round(counter_fh.get('🏢') / all_flathouse * 100, 3)
    flath_q = (f'Любители крыши дома своего на месте? Результаты честных выборов\n'
                f'🏢Партия многоквартирной суеты - *{flat_perc}%🏢*\n'
                f'🏡Партия загородного домашнего уюта - *{home_perc}%*🏡')

    all_tp = cur.execute('SELECT train_plain FROM Blic').fetchall()
    base_list_tp = [x[0] for x in all_tp]
    counter_tp = Counter(base_list_tp)
    all_trainplain = counter_tp.get('✈️') + counter_tp.get('🚂')
    plain_perc = round(counter_tp.get('✈️') / all_trainplain * 100, 3)
    train_perc = round(counter_tp.get('🚂') / all_trainplain * 100, 3)
    train_q = (f'Любители путешествовать на месте? Результаты честных выборов\n'
                f'️🚂Партия поездной романтики - *{train_perc}%*🚂\n'
                f'✈️Партия рыбы или мяса - *{plain_perc}%*✈️')

    all_tc = cur.execute('SELECT tea_coffe FROM Blic').fetchall()
    base_list_tc = [x[0] for x in all_tc]
    counter_tc = Counter(base_list_tc)
    all_tea_coffe = counter_tc.get('🫖') + counter_tc['☕️']
    tea_perc = round(counter_tc.get('🫖') / all_tea_coffe * 100, 3)
    coffe_perc = round(counter_tc['☕️'] / all_tea_coffe * 100, 3)
    tea_q = (f'Любители теплых напитков на месте? Результаты честных выборов\n'
                f'🫖Партия чайного спокойствия- *{tea_perc}%*🫖\n'
                f'☕️Партия кофейной суеты - *{coffe_perc}%*☕️')


    all_tt = cur.execute('SELECT tv_tube FROM Blic').fetchall()
    base_list_tt = [x[0] for x in all_tt]
    counter_tt = Counter(base_list_tt)
    all_tv_tube = counter_tt['🖥️'] + counter_tt['📺']
    tube_perc = round(counter_tt['🖥️️'] / all_tv_tube * 100, 3)
    tv_perc = round(counter_tt['📺'] / all_tv_tube * 100, 3)
    tv_q = (f'Любители повтыкать в экран на месте? Результаты честных выборов\n'
                f'📺Партия ТВ - староверов  - *{tv_perc}%*📺\n'
                f'🖥️Партия блогеров и подписок - *{tube_perc}%*🖥️')

    all_ai = cur.execute('SELECT andr_ios FROM Blic').fetchall()
    base_list_ai = [x[0] for x in all_ai]
    counter_ai = Counter(base_list_ai)
    all_andr = counter_ai['📵android'] + counter_ai.get('📱ios')
    aios_perc = round(counter_ai['📵android️'] / all_andr * 100, 3)
    andr_perc = round(counter_ai.get('📱ios') / all_andr * 100, 3)
    tel_q = (f'Любители потыкать в экран на месте? Результаты честных выборов\n'
                f'Партия яблочников  - *{aios_perc}%*📱ios\n'
                f'Партия андроидов - *{andr_perc}%*📵android')

    all_tat = cur.execute('SELECT tatoo FROM Blic').fetchall()
    base_list_tat = [x[0] for x in all_tat]
    counter_tat = Counter(base_list_tat)
    all_tatoo = counter_tat.get('✅') + counter_tat.get('⛔️')
    yest_perc = round(counter_tat.get('✅') / all_tatoo * 100, 3)
    not_perc = round(counter_tat.get('⛔️') / all_tatoo * 100, 3)
    tatoo_q = (f'Любите живопись по телу? Результаты честных выборов\n'
                f'Партия яркой внешности  - *{yest_perc}%*\n'
                f'Партия чистого тела - *{not_perc}%*')

    all_dr = cur.execute('SELECT drive FROM Blic').fetchall()
    base_list_dr = [x[0] for x in all_dr]
    counter_dr = Counter(base_list_dr)
    all_drive = counter_dr.get('✅') + counter_dr.get('⛔️')
    yesdr_perc = round(counter_dr.get('✅') / all_drive * 100, 3)
    notdr_perc = round(counter_dr.get('⛔️') / all_drive * 100, 3)
    drive_q = (f'Водитель или пешеход? Результаты честных выборов\n'
                f'Партия водителей - *{yesdr_perc}%*\n'
                f'Партия исключительно пешеходов - *{notdr_perc}%*')

    all_pk= cur.execute('SELECT parent_kid FROM Blic').fetchall()
    base_list_pk = [x[0] for x in all_pk]
    counter_pk = Counter(base_list_pk)
    all_parentkid = counter_pk.get('✅') + counter_pk.get('⛔️')
    yest_kid = round(counter_pk.get('✅') / all_drive* 100, 3)
    not_kid = round(counter_pk.get('⛔️') / all_drive * 100, 3)
    pk_q = (f'Родитель или все еще ребенок? Результаты честных выборов\n'
                f'Партия пока еще детей  - *{yest_kid}%*\n'
                f'Партия уже родителей- *{not_kid}%*')
    list_q = [pk_q, drive_q, tatoo_q, tel_q, tv_q, tea_q, train_q, flath_q, seam_q, eat_q, animal_q]
    analyst = random.choice(list_q)
    await bot.edit_message_text(chat_id=GROUP_DS_55_ID, message_id=kingmes[-1], text=analyst, parse_mode="MarkDown")
    mykings.clear()

@dp.callback_query_handler(IsVIP(), text='mycom')
async def mytrue_func(call):
    user_id = call.from_user.id
    base_count = cur.execute('SELECT id FROM Users').fetchall()
    blic_count = cur.execute('SELECT id FROM Blic').fetchall()
    base_info = cur.execute('SELECT age FROM Users WHERE age > 0').fetchall()
    base_info_m = cur.execute('SELECT age FROM Users WHERE age > 0 AND sex == "man"').fetchall()
    base_info_w = cur.execute('SELECT age FROM Users WHERE age > 0 AND sex == "woman"').fetchall()
    base_list = [x[0] for x in base_info]
    base_list_m = [x[0] for x in base_info_m]
    base_list_w = [x[0] for x in base_info_w]
    user_age_avg = sum(base_list) / len(base_list)
    user_age_med = st.median(base_list)
    user_age_avg_m = sum(base_list_m) / len(base_list_m)
    user_age_avg_w = sum(base_list_w) / len(base_list_w)
    user_age_med_m = st.median(base_list_m)
    user_age_med_w = st.median(base_list_w)
    base_max = cur.execute('SELECT MAX(age) FROM Users').fetchone()
    base_min = cur.execute('SELECT MIN(age) FROM Users').fetchone()
    mess = (f'С вашего позволения, я поделюсь *аналитикой* по чату:\n'
            f'На текущую секундочку в чате {len(base_list)} *настоящих мастеров DS*.\n'
            f'Средний возраст *элиты чата {round(user_age_avg, 2)}*\n'
            f'*🗿 - {round(user_age_avg_m, 2)}         👩🏻‍🦰 - {round(user_age_avg_w, 2)}*\n'
             f'Медианый возраст *золотого фонда чата {user_age_med}*\n'
            f'*🗿 - {user_age_med_m}         👩🏻‍🦰 - {user_age_med_w}*\n'
            f'*Диапазон возрастов чата {base_min[0]} - {base_max[0]}*\n'
            f'Внимание! Я вижу в чате еще *{len(base_count)-len(base_list)} живых юзеров*.\n'
            f'*Напишите* /start в отдельном чате со мной и заполните свои профили. Давайте еще лучше узнаем друг друга.\n'
            f'*А еще всего {len(blic_count)} прошли блиц.* Поторопитесь, на вершине еще остались места.')
    await bot.edit_message_text(chat_id=GROUP_DS_55_ID, message_id=kingmes[-1], text=mess, parse_mode="MarkDown")
    sleep(3)
    if len(base_list_w) > len(base_list_m):
        dolya = round(len(base_list_w)/len(base_list)*100, 3)
        await bot.send_message(
            chat_id=GROUP_DS_55_ID,
            text=f'Гинекократия наметилась.\nДевушки владеют контрольным пакетом чата в размере *{dolya}%*', parse_mode="MarkDown")
    elif len(base_list_w) < len(base_list_m):
        dolya = round(len(base_list_m) / len(base_list)*100, 3)
        await bot.send_message(
            chat_id=GROUP_DS_55_ID,
            text=f'Мужское большинство и в ДСе?\nКонтрольный пакет пареньков *{dolya}%*', parse_mode="MarkDown")
    elif len(base_list_w) == len(base_list_m):
        await bot.send_message(
            chat_id=GROUP_DS_55_ID,
            text=f'Я люблю когда так бывает. Объявляю половое равенство в чате', parse_mode="MarkDown")
    mykings.clear()
@dp.callback_query_handler(IsVIP(), text='myreput')
async def myreput_func(call):
    top_of_rate = cur.execute('SELECT id, rep FROM Users ORDER BY rep DESC').fetchall()
    chat_member1 = await bot.get_chat_member(chat_id=GROUP_DS_55_ID, user_id=top_of_rate[0][0])
    first_name1 = chat_member1.user.first_name
    mention1 = "[" + first_name1 + "](tg://user?id=" + str(top_of_rate[0][0]) + ")"
    chat_member2 = await bot.get_chat_member(chat_id=GROUP_DS_55_ID, user_id=top_of_rate[1][0])
    first_name2 = chat_member2.user.first_name
    mention2 = "[" + first_name2 + "](tg://user?id=" + str(top_of_rate[1][0]) + ")"
    chat_member3 = await bot.get_chat_member(chat_id=GROUP_DS_55_ID, user_id=top_of_rate[2][0])
    first_name3 = chat_member3.user.first_name
    mention3 = "[" + first_name3 + "](tg://user?id=" + str(top_of_rate[2][0]) + ")"
    chat_member4 = await bot.get_chat_member(chat_id=GROUP_DS_55_ID, user_id=top_of_rate[3][0])
    first_name4 = chat_member4.user.first_name
    mention4 = "[" + first_name4 + "](tg://user?id=" + str(top_of_rate[3][0]) + ")"
    chat_member5 = await bot.get_chat_member(chat_id=GROUP_DS_55_ID, user_id=top_of_rate[4][0])
    first_name5 = chat_member5.user.first_name
    mention5 = "[" + first_name5 + "](tg://user?id=" + str(top_of_rate[4][0]) + ")"
    fin_mes = (
        f'Извольте ознакомиться с самыми приятными собеседниками:\n'
        f'Генеральный директор уважения - {mention1}.\n'
        f'Баллы уважения {top_of_rate[0][1]}🦄🦄🦄\n'
        f'Зам. генерального директора по престижу - {mention2}.\n'
        f'Уровень престижа {top_of_rate[1][1]}👑👑\n'
        f'Зам. генерального директора по авторитету - {mention3}.\n'
        f'Очки авторитета {top_of_rate[2][1]}🐗🐗\n'
        f'Зам. генерального директора по репутации - {mention4}.\n' 
        f'Репутационный итог {top_of_rate[3][1]}🌈🌈\n'
        f'Тамада - баянист - {mention5}.\n'
        f'Удачных мероприятий {top_of_rate[4][1]}🕺💃\n'
    )
    await bot.edit_message_text(chat_id=GROUP_DS_55_ID, message_id=kingmes[-1], text=fin_mes, parse_mode="MarkDown")
    await bot.send_sticker(chat_id=GROUP_DS_55_ID, sticker='CAACAgIAAxkBAAEGuQxjkKkuzFF33YjLCqoAASeVh1jwrdwAAhwDAAKiivEHzzHg8L3QHs4rBA')
    user_id = call.from_user.id
    user_rate_cur = cur.execute('SELECT rep FROM Users WHERE id=' + str(user_id)).fetchone()
    user_name = call.from_user.first_name
    mention = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    if not user_rate_cur:
        await bot.send_message(
            chat_id=GROUP_DS_55_ID,
            text=f'EERRORR>>> USER NOT FOUND!!!! {mention}, твой авторитет мне неизвестен\nВозможно пришло время дать /start нашему знакомству?',
            parse_mode="MarkDown")
    else:
        await bot.send_message(
            chat_id=GROUP_DS_55_IDd,
            text=f'Репутация {mention}, на текущий момент составляет - {user_rate_cur[0]} ⭐️\n', parse_mode="MarkDown")
    mykings.clear()

@dp.callback_query_handler(IsVIP(), text='mytrue')
async def myrrueds_func(call):
   base_whyds = cur.execute('SELECT id, chat_name, whyds FROM Users WHERE whyds NOT NULL').fetchall()
   one_ds = random.choice(base_whyds)
   rand_emo = ['🤌', '✊🏻', '💪🏻', '🫡']
   mention = "[" + one_ds[1] + "](tg://user?id=" + str(one_ds[0]) + ")"
   mess = (f'Перед тем как прийти сюда, многие задавались вопросом:\n'
                f'Что такое этот *DataSciene?*{random.choice(rand_emo)}'
                f'Когда дедлайн был близок и времени уже не оставалось, я дал слабину.\n'
                f'Подумал, что это не моё, хотел вернуться на домашний диван.\n'
                f'{mention} перубедил(а) меня своей мудростью.\n'
                f'Мудрость: *{one_ds[2]}* {random.choice(rand_emo)}')
   await bot.edit_message_text(chat_id=GROUP_DS_55_ID, message_id=kingmes[-1],
        text=mess, parse_mode="MarkDown")
   mykings.clear()
@dp.callback_query_handler(IsVIP(), text='mybooks')
async def mybooks_func(call):
    book_r = cur.execute('SELECT knigas FROM Blic WHERE knigas NOT NULL').fetchall()
    one_ds = random.choice(book_r)
    mess = (f'Рубрика *уютные рекомендации - книги*\n'
            f'📌{one_ds[0]}📌\n'
            f'Это *явно стоит* прочесть🙊!')
    await bot.edit_message_text(chat_id=GROUP_DS_55_ID, message_id=kingmes[-1],
        text=mess, parse_mode="MarkDown")
    mykings.clear()
@dp.callback_query_handler(IsVIP(), text='myfilms')
async def myfilms_func(call):
    fil_r = cur.execute('SELECT films FROM Blic WHERE films NOT NULL').fetchall()
    one_ds = random.choice(fil_r)
    mess = (f'Рубрика *приятные рекомендации - фильмы/сериалы*\n'
            f'📌{one_ds[0]}📌\n'
            f'Это *явно стоит* посмотреть🙈!')
    await bot.edit_message_text(chat_id=GROUP_DS_55_ID, message_id=kingmes[-1],
        text=mess, parse_mode="MarkDown")
    mykings.clear()
@dp.callback_query_handler(IsVIP(), text='mymusic')
async def myfilms_func(call):
    mus_r = cur.execute('SELECT melody FROM Blic WHERE melody NOT NULL').fetchall()
    one_ds = random.choice(mus_r)
    mess = (f'Рубрика *мелодичные рекомендации - музыка*\n'
            f'📌{one_ds[0]}📌\n'
            f'Это *явно стоит* услышать🙉!')
    await bot.edit_message_text(chat_id=GROUP_DS_55_ID, message_id=kingmes[-1],
        text=mess, parse_mode="MarkDown")
    mykings.clear()
@dp.message_handler()
async def check_user(message: types.Message):
    # chat_name = message.from_user.first_name
    user_id = message.from_user.id
    fellows = cur.execute('SELECT id FROM Users').fetchall()
    fellows_list = [x[0] for x in fellows]
    if user_id not in fellows_list:
        cur.execute('INSERT INTO Users(id, rep) VALUES(?, ?)', (user_id, 0))
        bd.commit()



# Техническая часть, чтобы бот работал не уходил в игнор от большого количества запросов.
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
