from aiogram import executor
from aiogram import types
from time import sleep
from aiogram.dispatcher.filters import CommandStart
import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher import FSMContext
import random
import matplotlib.pyplot as plt
import sqlite3
import io
import statistics as st
import pandas as pd
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import IsReplyFilter
from aiogram.dispatcher.filters.state import StatesGroup, State
from create_bot import bot, dp, GROUP_DS_55_ID



# Базовые настройки для соединения с созданным ботом



# Подключаемся/создаем базу данных
bd = sqlite3.connect('datasciense.db')
cur = bd.cursor()
bd.commit()

# инлайн кнопки для основного меню и реакцию на старт
button1 = InlineKeyboardButton(text='ПРОФИЛЬ🧐', callback_data='profile')
button2 = InlineKeyboardButton(text='БЛИЦ🧾', callback_data='blic')
button3 = InlineKeyboardButton(text='ССЫЛОЧКИ💌', callback_data='base')
button4 = InlineKeyboardButton(text='ОСНОВНОЕ МЕНЮ©️', callback_data='menu')
button5 = InlineKeyboardButton(text='МОЯ УЧЁБА🤓', callback_data='educ')
button6 = InlineKeyboardButton(text='ВЭБЫ🖥', callback_data='webs')
button7 = InlineKeyboardButton(text='ССЫЛОЧНАЯ📑', callback_data='links')

class Profile(StatesGroup):
    ProfileSex = State()
    ProfileAge = State()
    ProfileCity = State()
    ProfileAself = State()
    ProfileWhyDs = State()

class Educ(StatesGroup):
    EducProgress = State()
    EducType = State()
    EducFlow = State()
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
    main_menu.add(button1, button2, button5, button6, button7)

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
            good_person = f'Твой профиль заполнен и ты прошёл блиц. Ты супер!'
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
        main_menu = InlineKeyboardMarkup(row_width=2)
        main_menu.add(button1, button2, button5)
        welcome = (f'Привяу, я Староста.\n'
                   f'Я много учился раньше, а сейчас помогаю тем, кто учится прямо сейчас. Кстати благодаря курсу я нашёл {len(fellows_list)} друзей.\nНажми кнопку "ПРОФИЛЬ" чтобы рассказать чуть больше о себе\n'
                   f'Еще я провожу мини-исследования. Нажми кнопку "БЛИЦ", чтобы ответить на небольшой блиц и поделиться рекомендациями по фильмам, книгам, музыке\n')
        cur.execute('INSERT INTO Users(id, rep) VALUES(?, ?)', (user_id, 0))
        bd.commit()
        await bot.send_message(chat_id=user_id, text=welcome, parse_mode="MarkDown", reply_markup=main_menu2)

# Заготовка для работы непосредственно с библиотекой. Недоработана
# @dp.callback_query_handler(text='base')
# async def myfunc(call):
#     buttonb1 = InlineKeyboardButton(text='СВИТОК©️', callback_data='funlis')
#     buttonb2 = InlineKeyboardButton(text='ДОБАВИТЬ🧷', callback_data='addfun')
#     base_menu = InlineKeyboardMarkup(row_width=2)
#     base_menu.insert(buttonb1)
#     base_menu.insert(buttonb2)
#     base_mes = f'Это библиотека полезных функций. Сейчас в библиотеке {len(funcs_list)} функций. ' \
#                f'Нажми "СПИСОК" чтобы посмотреть библиотеку. ' \
#                f'Нажми "ДОБАВИТЬ" чтобы добавить информацию по новой функции'
#     await bot.send_message(chat_id=call.from_user.id, text=base_mes, parse_mode="MarkDown", reply_markup=base_menu)

# Заготовка для реакции на кнопку СПИСОК
# Пусть пока закоментированы будут, чтобы лишних ошибок не было
# @dp.callback_query_handler(text='funlis')
# async def funlist(call):
#     funcs = cur.execute('SELECT func FROM Base WHERE func NOT NULL').fetchall()
#     funcs_list = [x[0] for x in funcs]
#     await bot.send_message(chat_id=call.from_user.id, text=funcs_list, parse_mode="MarkDown", reply_markup=BaseMenu)



@dp.callback_query_handler(text='webs')
async def webs_list(call):
    funcs = cur.execute('SELECT * FROM Webs').fetchall()
    descs = []
    links = []
    for i in funcs:
        descs.append(i[0])
        links.append(i[1])

    links_list = f'Всего записей: {len(links)}\n'
    for i in range(len(links)):
        mes = '<a href="' + links[i] + '">' + descs[i] + '</a>'
        links_list = links_list + mes + '\n'

    await bot.send_message(chat_id=call.from_user.id, text=links_list, parse_mode="HTML")

@dp.callback_query_handler(text='links')
async def webs_list(call):
    funcs_p = cur.execute('SELECT * FROM Base WHERE category == "Python"').fetchall()
    descs_p = []
    links_p = []
    for i in funcs_p:
        descs_p.append(i[1])
        links_p.append(i[2])

    links_list_p = f'Всего полезных по Python: {len(links_p)}\n'
    for i in range(len(links_p)):
        mes = '<a href="' + links_p[i] + '">' + descs_p[i] + '</a>'
        links_list_p = links_list_p + mes + '\n'

    await bot.send_message(chat_id=call.from_user.id, text=links_list_p, parse_mode="HTML")
    sleep(1)
    funcs_e = cur.execute('SELECT * FROM Base WHERE category == "EDA"').fetchall()
    descs_e = []
    links_e = []
    for i in funcs_e:
        descs_e.append(i[1])
        links_e.append(i[2])

    links_list_e = f'Всего полезных по EDA: {len(links_e)}\n'
    for i in range(len(links_e)):
        mes = '<a href="' + links_e[i] + '">' + descs_e[i] + '</a>'
        links_list_e = links_list_e + mes + '\n'

    await bot.send_message(chat_id=call.from_user.id, text=links_list_e, parse_mode="HTML")
    sleep(1)
    funcs_s = cur.execute('SELECT * FROM Base WHERE category == "Statistics"').fetchall()
    descs_s = []
    links_s = []
    for i in funcs_s:
        descs_s.append(i[1])
        links_s.append(i[2])

    links_list_s = f'Всего полезных по Статистике: {len(links_s)}\n'
    for i in range(len(links_s)):
        mes = '<a href="' + links_s[i] + '">' + descs_s[i] + '</a>'
        links_list_s = links_list_s + mes + '\n'

    await bot.send_message(chat_id=call.from_user.id, text=links_list_s, parse_mode="HTML")
    sleep(1)
    funcs_m = cur.execute('SELECT * FROM Base WHERE category == "ML"').fetchall()
    descs_m = []
    links_m = []
    for i in funcs_m:
        descs_m.append(i[1])
        links_m.append(i[2])

    links_list_m = f'Всего полезных по ML: {len(links_m)}\n'
    for i in range(len(links_m)):
        mes = '<a href="' + links_m[i] + '">' + descs_m[i] + '</a>'
        links_list_m = links_list_m + mes + '\n'

    await bot.send_message(chat_id=call.from_user.id, text=links_list_m, parse_mode="HTML")

@dp.callback_query_handler(text='educ')
async def educ(call):
    user_id = call.from_user.id
    myprofile = cur.execute('SELECT progress FROM Users WHERE id=' + str(user_id)).fetchone()
    mycheck = cur.execute('SELECT progress, type_educ, flow_num  FROM Users WHERE id=' + str(user_id)).fetchone()
    button11 = InlineKeyboardButton(text='Изменить данные', callback_data='addeduc')
    button12 = InlineKeyboardButton(text='Обновить прогресс', callback_data='updprog')
    if myprofile is not None:
        myinfo = (
            f'*Мои данные*\n'
            f'*Текущий прогресс*: {mycheck[0]}%\n'
            f'*Тип обучения*: {mycheck[1]}\n'
            f'*Когорта*: {mycheck[2]}\n'
        )
        profile_menu = InlineKeyboardMarkup(row_width=2)
        profile_menu.add(button11, button12, button4)
        await bot.send_message(chat_id=user_id, text=myinfo, parse_mode="MarkDown", reply_markup=profile_menu)
@dp.callback_query_handler(text='addeduc')
async def addeduc(call):
    user_id = call.from_user.id
    await bot.send_message(chat_id=user_id, text='Укажи номер своей первоначальной когорты(той с который началось обучение по курсу)', parse_mode="MarkDown")
    await Educ.EducFlow.set()


@dp.message_handler(state=Educ.EducFlow)
async def educ_cp(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    mes = message.text
    if mes.isdigit():
        if 0 < int(mes) < 56:
            cur.execute('UPDATE Users SET flow_num == ? WHERE id == ?', (mes, user_id))
            bd.commit()
            cp_keyb = InlineKeyboardMarkup(row_width=2)
            button1 = InlineKeyboardButton(text='Я с ЦП🤌', callback_data='cp')
            button2 = InlineKeyboardButton(text='Сам пришёл✊🏻', callback_data='nocp')
            cp_keyb.add(button1, button2)
            await bot.send_message(
                chat_id=user_id,
                text='Принято. Ты по программе ЦП(Цифровые профессии) или по собственному желанию?', reply_markup=cp_keyb
            )
            await Educ.EducType.set()
        else:
            await bot.send_message(chat_id=user_id,
                                   text='Мне нужен номер твоей первоначальной когорты в цифрах. А ты что вводишь?')
    else:
        await bot.send_message(chat_id=user_id, text='Я что по твоему какая-то шутка?')


@dp.callback_query_handler(text=['cp', 'nocp'], state=Educ.EducType)
async def educ_fin(call, state: FSMContext):
    user_id = call.from_user.id
    if call.data == 'cp':
        cur.execute('UPDATE Users SET type_educ == ? WHERE id == ?', ('ЦП', user_id))
        bd.commit()
    elif call.data == 'nocp':
        cur.execute('UPDATE Users SET type_educ == ? WHERE id == ?', ('Без ЦП', user_id))
        bd.commit()
    await bot.send_message(chat_id=user_id,
                               text=f'Понятненько. Напомни, пожалуйста, свой текущий прогресс по курсу?')
    await Educ.EducProgress.set()
@dp.message_handler(state=Educ.EducProgress)
async def educ_pro(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    mes = message.text

    if mes.isdigit():
        if 0 < int(mes) < 101:
            cur.execute('UPDATE Users SET progress == ? WHERE id == ?', (mes, user_id))
            bd.commit()
            main_menu = InlineKeyboardMarkup(row_width=2)
            main_menu.add(button4)
            await bot.send_message(chat_id=user_id,
                           text=f'Всё заполнено! УРА!!!', reply_markup=main_menu)
            await state.reset_state()
        else:
            await bot.send_message(chat_id=user_id,
                                   text=f'Я жду двухзначное число(процент прохождения курса)')


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
        profile_menu.add(button11, button4)
        await bot.send_message(chat_id=user_id, text=myinfo, parse_mode="MarkDown", reply_markup=profile_menu)
    elif myprofile is None:
        profile_menu1 = InlineKeyboardMarkup(row_width=2)
        profile_menu1.add(button11, button4)
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
    profile_sex.add(button1, button2, button3)
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
    if message_lower.find('пасиб') > -1 or message_lower.find('лагодар') > -1:
        if user_id == rep_id:
            await message.answer(
                text=f'{mention_rep} ты так-то человечек хороший. Все это уже поняли. Может про DS что нить накидаешь?',
                parse_mode="MarkDown")
        elif user_id != rep_id:
            user_rate_cur = cur.execute('SELECT rep FROM Users WHERE id == ?', (rep_id,)).fetchone()
            # Если нет юзера в базе, то добавляем его туда сразу с рейтингом 1
            if not user_rate_cur:
                user_rate_fin = 1
                cur.execute('INSERT INTO Users (id, rep) VALUES(?, ?)', (rep_id, user_rate_fin))
                bd.commit()

            # если юзер есть, то обновляем его данные
            else:
                user_rate_fin = user_rate_cur[0] + 1
                cur.execute('UPDATE Users SET rep == ? WHERE id == ?', (user_rate_fin, rep_id))
                bd.commit()

            funfact = ['отзывчивая личность.',
                       'мудрый собеседник.',
                       'всегда сумеет найти нужные слова.',
                       'человечище!!!.',
                       'хорошого дня, привет от меня',
                       'рупор истины',
                       'расшарил(а) мудрость',
                       'готов(а) делиться знаниями, респект.',
                       'задаёт правильные ценности',
                       'добрая личность',
                       'умник или умница!',
                       'чудесный индивидуум',
                       'статистически успешен']
            forfun = random.choice(funfact)
            await message.answer(
                text=f' {mention_rep} {forfun}.\n+1 в твою личную коллекцию благодарностей.'
                     f'\nУровень коллективной благодарности: {user_rate_fin} ⭐️',
                parse_mode="MarkDown"
            )
    elif message_lower.find('профил') > -1 and len(message_lower) <= 7:
        mycheck = cur.execute('SELECT * FROM Users WHERE id=' + str(rep_id)).fetchone()
        mention_rep = "[" + rep_name + "](tg://user?id=" + str(rep_id) + ")"
        if mycheck[3] is None:
            await message.answer(
                text=f'{mention_rep} стесняется себя и своих сокурсников\n' 
                     f'Может намекнем стесняшке, что мы тут все свои и не кусаемcя🥹?',
                parse_mode="MarkDown")
            await message.delete()
        else:
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

    elif message_lower.find('покаж') > -1:
        sleep(5)
        await bot.send_sticker(
            chat_id=GROUP_DS_55_ID,
            sticker="CAACAgIAAxkBAAEGvlZjkluuNc9rcXyHz2CfH5v4Tgs6HQACtBQAAtdB-UrTW2cy7dEMQysE"
        )
    elif message_lower.find('откат') > -1 and len(message_lower) == 5:
        moders_id = [29720838, 90185253, 176814724, 1332281468, 780602845, 1595322394, 1623224307, 150360155, 877073259, 105685914]
        if message.from_user.id in moders_id:
            user_rate_cur = cur.execute('SELECT rep FROM Users WHERE id == ?', (rep_id,)).fetchone()
            user_rate_fin = user_rate_cur[0] - 1
            cur.execute('UPDATE Users SET rep == ? WHERE id == ?', (user_rate_fin, rep_id))
            bd.commit()
            await message.answer(
                text=f'Репутация {mention_rep} скорректирована в связи с ошибочным начислением'
                    f'\nКорректная репутация: {user_rate_fin} ⭐️',
                parse_mode="MarkDown"
        )
        await message.delete()
    elif message.reply_to_message.from_user.is_bot:
        sleep(4)
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
                       'Наконец-то умные мысли',
                       'Вот это я понимаю аналитика',
                       'Вот кстати да',
                       'Умные мысли часто преследуют его, но он оказывается быстрее'
                       'Однозначно он мой герой',
                       'Я это понимаю, ты это понимаешь',
                       'Прислушайтесь к мудрецу',
                       'И сразу на душе потеплело',
                       'У матросов есть вопросы',
                       'Интересная история',
                       '💩',
                       '🤝',
                       '💋',
                       'Иногда приходиться прикинуться дурачком, чтобы не выглядеть идиотом',
                       'Hello guys, u menya vse nice',
                       'Ну что сказать, ну что сказать, человек мой дорогой?',
                       'КВН заказывали?',
                       'Да ты мне не рассказывай, ты им рассказывай',
                       'Cмекаешь?',
                       'Ты тут самый крутой',
                       'Не всем дано это понять',
                       'Может посплетничаем?',
                       'Любишь кататься - люби и катайся',
                       'Вообще-то да',
                       'Еще чего, какие глупости',
                       'Вообще-то, но в данный момент нет',
                       'Ну допустим...',
                       'Как я тебя понимаю',
                       'Ну вот и я о том же',
                       'А можно тост?'
                       ]
        forfun = random.choice(all_phrases)
        await message.answer(text=forfun, parse_mode="MarkDown")

# Новичок в группе
@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_member(message):
    await message.answer(f"Милейшие, у нас новичок- {message.new_chat_members[0].get_mention(as_html=True)}.\n Пару слов о себе и о том, как нашёл(нашла) этот чат сможешь?", parse_mode='HTML')
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
        victorina_menu.add(button11, button4)
        await bot.send_message(chat_id=call.from_user.id, text=myansw, parse_mode="MarkDown", reply_markup=victorina_menu)
    elif user_id not in mypvic_list:
        user_id = call.from_user.id
        victorina_menu1 = InlineKeyboardMarkup(row_width=2)
        victorina_menu1.add(button11, button4)
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
    vic_q1.add(button1, button2)
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
    vic_q2.add(button1, button2)
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
    vic_q3.add(button1, button2)
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
    vic_q4.add(button1, button2)
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
    button1 = InlineKeyboardButton(text='🚝', callback_data='train')
    button2 = InlineKeyboardButton(text='✈', callback_data='plain')
    vic_q5.add(button1, button2)
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
    vic_q6.add(button1, button2)
    if call.data == 'train':
        cur.execute('UPDATE Blic SET train_plain == ? WHERE id == ?', ('🚝', user_id))
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
    vic_q7.add(button1, button2)
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
    vic_q8.add(button1, button2)
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
    vic_q9.add(button1, button2)
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
    vic_q10.add(button1, button2)
    if call.data == 'yes_tatoo':
        cur.execute('UPDATE Blic SET tatoo == ? WHERE id == ?', ('🎨', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q10)
        await Blic.drive.set()
    elif call.data == 'no_tatoo':
        cur.execute('UPDATE Blic SET tatoo == ? WHERE id == ?', ('🗒', user_id))
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
    vic_q11.add(button1, button2)
    if call.data == 'yes_drive':
        cur.execute('UPDATE Blic SET drive == ? WHERE id == ?', ('🚕', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q11)
        await Blic.parent_kid.set()
    elif call.data == 'no_drive':
        cur.execute('UPDATE Blic SET drive == ? WHERE id == ?', ('🦵🏻', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest, reply_markup=vic_q11)
        await Blic.parent_kid.set()
@dp.callback_query_handler(text=['yes_kid', 'no_kid'], state=Blic.parent_kid)
async def films(call, state: FSMContext):
    user_id = call.from_user.id
    age_quest = f'Порекомендуй 3 фильма/сериала сокурсникам'
    if call.data == 'yes_kid':
        cur.execute('UPDATE Blic SET parent_kid == ? WHERE id == ?', ('👩‍👦‍👦', user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text=age_quest)
        await Blic.films.set()
    elif call.data == 'no_kid':
        cur.execute('UPDATE Blic SET parent_kid == ? WHERE id == ?', ('👶🏻', user_id))
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
    victorina_menu.add(button4)
    await bot.send_message(chat_id=user_id,
                           text=myansw, reply_markup=victorina_menu)

    await state.reset_state()
# Реакция на кнопку возврата в основное меню(клавиатура)
@dp.callback_query_handler(text='menu')
async def menu(call):
    main_menu = InlineKeyboardMarkup(row_width=2)
    main_menu.add(button1, button2, button5)
    await bot.send_message(
        chat_id=call.from_user.id,
        text='ОСНОВНОЕ МЕНЮ',
        parse_mode="MarkDown",
        reply_markup=main_menu
    )


mykings= []
kingmes = []
@dp.message_handler(text=['55', 'бот', 'секрет'])
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
        button21 = InlineKeyboardButton(text='DS истина👏🏻', callback_data='mytrue')
        button22 = InlineKeyboardButton(text='Типичный DS🧐', callback_data='myfact')
        button23 = InlineKeyboardButton(text='Наш коллектив👨‍👩‍👦‍👦', callback_data='mycom')
        button24 = InlineKeyboardButton(text='Наша музыка🎼', callback_data='mymusic')
        button25 = InlineKeyboardButton(text='Наши фильмы🎥', callback_data='myfilms')
        button26 = InlineKeyboardButton(text='Наши книги📓', callback_data='mybooks')
        button27 = InlineKeyboardButton(text='Репутация🔝', callback_data='myreput')
        button28 = InlineKeyboardButton(text='Один из нас🔝', callback_data='rrr')
        luck = InlineKeyboardMarkup(row_width=2)
        luck.add(button21, button22, button23, button24, button25, button26, button27, button28)
        mymes = await bot.send_message(
            chat_id=message.chat.id,
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

    await message.delete()

@dp.callback_query_handler(text='rrr')
async def myfriend_func(call):
    base_aself = cur.execute('SELECT id, chat_name, aself FROM Users WHERE aself NOT NULL').fetchall()
    one_ds = random.choice(base_aself)
    rand_emo = ['🤌', '✊🏻', '💪🏻', '🫡']
    mention = "[" + one_ds[1] + "](tg://user?id=" + str(one_ds[0]) + ")"
    mess = (f'*Современный ДСер*, какой он?\n'
            f'Один из нас *описывает* себя{random.choice(rand_emo)} так\n'
            f'*{one_ds[2]}*\n'
            f'Позвольте представить важного члена коллектива:\n'
            f'Наша глубокоУважаемая личность {mention}\n'
            f'*Лови респект от коллектива{random.choice(rand_emo)}*')
    await bot.edit_message_text(chat_id=GROUP_DS_55_ID, message_id=kingmes[-1],
                                text=mess, parse_mode="MarkDown")
    mykings.clear()


blic_dict = {'🐈': 'Кошатники',
             '🐕\u200d🦺': 'Собачники',
             '🍕': 'Пиццаеды',
             '🍣': 'Сушиеды',
             '🏖': 'Пляжники',
             '🏔': 'Горапокорители',
             '🏢': 'Квартирщики',
             '🏡': 'Доможители',
             '🚝': 'Поездолюбители',
             '✈️': 'Самолетчики',
             '🥃': 'Чаевники',
             '🥛': 'Кофеинонаркоманы',
             '📺': 'Зомобящеры',
             '🖥️': 'Зумеры-ютуберы',
             '📱ios': 'Айфонорабы',
             '📵android': 'Андроидоэлита',
             '🚕': 'Водятлы',
             '🦵🏻': 'Пешики',
             '👩‍👦‍👦': 'Родители',
             '👶🏻': 'Пока сами дети',
             '🎨': 'Живопись по телу',
             '🗒': 'Чистота туловища'

             }
@dp.callback_query_handler(text='myfact')
async def myfact_func(call):
    sql_rand = random.randint(1, 11)
    if sql_rand == 1:
        group_select = cur.execute('SELECT cat_dog  FROM Blic WHERE cat_dog NOT NULL').fetchall()
    elif sql_rand == 2:
        group_select = cur.execute('SELECT pizza_suchi FROM Blic WHERE pizza_suchi NOT NULL').fetchall()
    elif sql_rand == 3:
        group_select = cur.execute('SELECT sea_mount FROM Blic WHERE sea_mount NOT NULL').fetchall()
    elif sql_rand == 4:
        group_select = cur.execute('SELECT flat_house FROM Blic WHERE flat_house NOT NULL').fetchall()
    elif sql_rand == 5:
        group_select = cur.execute('SELECT train_plain FROM Blic WHERE train_plain NOT NULL').fetchall()
    elif sql_rand == 6:
        group_select = cur.execute('SELECT tea_coffe FROM Blic WHERE tea_coffe NOT NULL').fetchall()
    elif sql_rand == 7:
        group_select = cur.execute('SELECT tv_tube FROM Blic WHERE tv_tube NOT NULL').fetchall()
    elif sql_rand == 8:
        group_select = cur.execute('SELECT andr_ios FROM Blic WHERE andr_ios NOT NULL').fetchall()
    elif sql_rand == 9:
        group_select = cur.execute('SELECT tatoo FROM Blic WHERE tatoo NOT NULL').fetchall()
    elif sql_rand == 10:
        group_select = cur.execute('SELECT drive FROM Blic WHERE drive NOT NULL').fetchall()
    elif sql_rand == 11:
        group_select = cur.execute('SELECT parent_kid FROM Blic WHERE parent_kid NOT NULL').fetchall()

    base_list = [x[0] for x in group_select]

    true_labels = []
    for i in base_list:
        if i in blic_dict:
            true_labels.append(blic_dict[i])

    # cats_perc = round(counter_animals.get('🐈') / all_animals * 100, 3)
    # dogs_perc = round(counter_animals.get('🐕\u200d🦺') / all_animals * 100, 3)
    # animal_q = (f'Любители шерстянкых товарищей на месте? Результаты честных выборов\n'
    #             f'🐈Партия любителей кошек - *{cats_perc}%*🐈\n'
    #             f'🐕\u200d🦺Партия любителей собак - *{dogs_perc}%*🐕\u200d🦺')

    mychet = pd.Series(true_labels)
    my_fig = mychet.value_counts().reset_index()
    true_labels = [my_fig['index'][0], my_fig['index'][1]]
    plot_rand = random.randint(1, 6)

    title = f'Контрольная выборка {len(base_list)}'
    if plot_rand == 1:
        mystable = mychet.value_counts().plot.pie(autopct='%1.0f%%',  labels=['',''])
        plt.legend(true_labels)
        plt.title(title)
        plt.savefig('foo.png')
        plt.close()
        with io.open('foo.png', 'rb') as image:
            await bot.send_photo(GROUP_DS_55_ID, photo=image)
    elif plot_rand ==2:
        mystable = mychet.value_counts()
        fig, ax = plt.subplots()
        ax.bar(true_labels, mystable,  width=0.8, edgecolor="black", linewidth=0.7, color=['red', 'blue'])
        plt.title(title)
        plt.savefig('foo.png')
        plt.close()
        with io.open('foo.png', 'rb') as image:
            await bot.send_photo(GROUP_DS_55_ID, photo=image)
    elif plot_rand ==3:
        mystable = mychet.value_counts()
        fig, ax = plt.subplots()
        ax.stackplot(true_labels, mystable, color='cyan')
        plt.title(title)
        plt.savefig('foo.png')
        plt.close()
        with io.open('foo.png', 'rb') as image:
            await bot.send_photo(GROUP_DS_55_ID, photo=image)
    elif plot_rand ==4:
        mystable = mychet.value_counts()
        fig, ax = plt.subplots()
        ax.plot(true_labels, mystable, linewidth=2.0)
        plt.title(title)
        plt.savefig('foo.png')
        plt.close()
        with io.open('foo.png', 'rb') as image:
            await bot.send_photo(GROUP_DS_55_ID, photo=image)
    elif plot_rand ==5:
        mystable = mychet.value_counts()
        fig, ax = plt.subplots()
        ax.scatter(true_labels, mystable, color=['green', 'purple'], marker="X", s=999)
        plt.title(title)
        plt.savefig('foo.png')
        plt.close()
        with io.open('foo.png', 'rb') as image:
            await bot.send_photo(GROUP_DS_55_ID, photo=image)
    elif plot_rand ==6:
        mystable = mychet.value_counts()
        fig, ax = plt.subplots()
        ax.stem(true_labels, mystable)
        plt.title(title)
        plt.savefig('foo.png')
        plt.close()
        with io.open('foo.png', 'rb') as image:
            await bot.send_photo(GROUP_DS_55_ID, photo=image)

    true_labels=[]
    bd.commit()
    # #
    #
    #
    #
    # base_list_ps = [x[0] for x in all_e]
    # counter_eat = Counter(base_list_ps)
    # all_eat = len(base_list_ps)
    # pizza_perc = round(counter_eat.get('🍕') / all_eat * 100, 3)
    # suchi_perc = round(counter_eat.get('🍣') / all_eat * 100, 3)
    # eat_q = (f'Любители пощекотать вкусовые рецепторы на месте? Результаты честных выборов\n'
    #             f'🍣Партия любителей есть палочками - *{pizza_perc}%🍣*\n'
    #             f'🍕Партия любителей есть руками - *{suchi_perc}%🍕*')
    #
    #
    # base_list_sm = [x[0] for x in all_seamou]
    # counter_sm = Counter(base_list_sm)
    # all_seamount = len(base_list_sm)
    # sea_perc = round(counter_sm.get('🏖') / all_seamount * 100, 3)
    # mount_perc = round(counter_sm.get('🏔') / all_seamount * 100, 3)
    # seam_q = (f'Любители хорошо отдохнуть? Результаты честных выборов\n'
    #             f'🏖Партия любителей морского воздуха - *{sea_perc}%*🏖\n'
    #             f'🏔Партия любителей горного воздуха - *{mount_perc}%*🏔')
    #
    #
    # base_list_fh = [x[0] for x in all_flh]
    # counter_fh = Counter(base_list_fh)
    # all_flathouse = len(base_list_fh)
    # home_perc = round(counter_fh.get('🏡') / all_flathouse * 100, 3)
    # flat_perc = round(counter_fh.get('🏢') / all_flathouse * 100, 3)
    # flath_q = (f'Любители крыши дома своего на месте? Результаты честных выборов\n'
    #             f'🏢Партия многоквартирной суеты - *{flat_perc}%🏢*\n'
    #             f'🏡Партия загородного домашнего уюта - *{home_perc}%*🏡')
    #
    #
    # base_list_tp = [x[0] for x in all_tp]
    # counter_tp = Counter(base_list_tp)
    # all_trainplain = len(base_list_tp)
    # plain_perc = round(counter_tp.get('✈️') / all_trainplain * 100, 3)
    # train_perc = round(counter_tp.get('🚂') / all_trainplain * 100, 3)
    # train_q = (f'Любители путешествовать на месте? Результаты честных выборов\n'
    #             f'️🚂Партия поездной романтики - *{train_perc}%*🚂\n'
    #             f'✈️Партия рыбы или мяса - *{plain_perc}%*✈️')
    #
    #
    # base_list_tc = [x[0] for x in all_tc]
    # counter_tc = Counter(base_list_tc)
    # all_tea_coffe = len(base_list_tc)
    # tea_perc = round(counter_tc.get('🫖') / all_tea_coffe * 100, 3)
    # coffe_perc = round((all_tea_coffe - counter_tc.get('🫖')) / all_tea_coffe * 100, 3)
    # tea_q = (f'Любители теплых напитков на месте? Результаты честных выборов\n'
    #             f'🫖Партия чайного спокойствия - *{tea_perc}%*🫖\n'
    #             f'☕️Партия кофейной суеты - *{coffe_perc}%*☕️')
    #
    #'
    #
    # base_list_tt = [x[0] for x in all_tt]
    # counter_tt = Counter(base_list_tt)
    # all_tv_tube = len(base_list_tt)
    # tube_perc = round((all_tv_tube-counter_tt['📺']) / all_tv_tube * 100, 3)
    # tv_perc = round(counter_tt['📺'] / all_tv_tube * 100, 3)
    # tv_q = (f'Любители повтыкать в экран на месте? Результаты честных выборов\n'
    #             f'📺Партия ТВ - староверов  - *{tv_perc}%*📺\n'
    #             f'🖥️Партия блогеров и подписок - *{tube_perc}%*🖥️')
    #
    #
    #
    # base_list_ai = [x[0] for x in all_ai]
    # counter_ai = Counter(base_list_ai)
    # all_andr = len(base_list_ai)
    # aios_perc = round(counter_ai['📱ios'] / all_andr * 100, 3)
    # andr_perc = round((all_andr - counter_ai['📱ios']) / all_andr * 100, 3)
    # tel_q = (f'Любители потыкать в экран на месте? Результаты честных выборов\n'
    #             f'Партия яблочников - *{aios_perc}%*📱ios\n'
    #             f'Партия андроидов - *{andr_perc}%*📵android')
    #
    #
    # base_list_tat = [x[0] for x in all_tat]
    # counter_tat = Counter(base_list_tat)
    # all_tatoo = len(base_list_tat)
    # yest_perc = round(counter_tat.get('✅') / all_tatoo * 100, 3)
    # not_perc = round(counter_tat.get('⛔️') / all_tatoo * 100, 3)
    # tatoo_q = (f'Любите живопись по телу? Результаты честных выборов\n'
    #             f'🎨Партия яркой внешности - *{yest_perc}%🎨*\n'
    #             f'🧽Партия чистого тела - *{not_perc}%🧽*')
    #
    #
    # base_list_dr = [x[0] for x in all_dr]
    # counter_dr = Counter(base_list_dr)
    # all_drive = len(base_list_dr)
    # yesdr_perc = round(counter_dr.get('✅') / all_drive * 100, 3)
    # notdr_perc = round(counter_dr.get('⛔️') / all_drive * 100, 3)
    # drive_q = (f'Водитель или пешеход? Результаты честных выборов\n'
    #             f'🛻Партия водителей - *{yesdr_perc}%*🚗\n'
    #             f'🚶‍♀️Партия исключительно пешеходов - *{notdr_perc}%*🚶‍♂️')
    #
    #
    # base_list_pk = [x[0] for x in all_pk]
    # counter_pk = Counter(base_list_pk)
    # all_parentkid = len(base_list_pk)
    # yest_kid = round(counter_pk.get('✅') / all_drive* 100, 3)
    # not_kid = round(counter_pk.get('⛔️') / all_drive * 100, 3)
    # pk_q = (f'Имеешь родительские обязанности или рановато? Результаты честных выборов\n'
    #             f'👶🏻Партия пока еще детей - *{yest_kid}%*👧🏻\n'
    #             f'👩🏻‍🦰Партия уже родителей - *{not_kid}%*🧔🏻‍♂️')
    # list_q = [pk_q, drive_q, tatoo_q, tel_q, tea_q, train_q, flath_q, seam_q, eat_q, animal_q, tv_q]
    # analyst = random.choice(list_q)
    # await bot.edit_message_text(chat_id=call.message.chat.id, message_id=kingmes[-1], text=list_q, parse_mode="MarkDown")
    # mykings.clear()

@dp.callback_query_handler(text='mycom')
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
    base_min_m = cur.execute('SELECT MIN(age) FROM Users WHERE sex="man"').fetchone()
    base_min_w = cur.execute('SELECT MIN(age) FROM Users WHERE sex="woman"').fetchone()
    base_max_m = cur.execute('SELECT MAX(age) FROM Users WHERE sex="man"').fetchone()
    base_max_w = cur.execute('SELECT MAX(age) FROM Users WHERE sex="woman"').fetchone()
    mess = (f'С вашего позволения, я поделюсь *аналитикой* по чату:\n'
            f'На текущую секундочку в чате {len(base_list)} *настоящих мастеров DS*.\n'
            f'Средний возраст *элиты чата {round(user_age_avg, 2)}*\n'
            f'*🗿 - {round(user_age_avg_m, 2)}         👩🏻‍🦰 - {round(user_age_avg_w, 2)}*\n'
             f'Медианый возраст *золотого фонда чата {user_age_med}*\n'
            f'*🗿 - {user_age_med_m}         👩🏻‍🦰 - {user_age_med_w}*\n'
            f'*Диапазон возрастов чата {base_min[0]} - {base_max[0]}*\n'
            f'*🗿 {base_min_m[0]}-{base_max_m[0]}  👩🏻‍🦰 - {base_min_w[0]}-{base_max_w[0]}*\n'
            f'Внимание! Я вижу в чате еще *{len(base_count)-len(base_list)} живых юзеров*.\n'
            f'*Напишите* /start в отдельном чате со мной и заполните свои профили. Давайте еще лучше узнаем друг друга.\n'
            f'*А еще всего {len(blic_count)} прошли блиц.* Поторопитесь, на вершине еще остались места.')
    await bot.edit_message_text(chat_id=GROUP_DS_55_ID, message_id=kingmes[-1], text=mess, parse_mode="MarkDown")
    sleep(3)
    if len(base_list_w) > len(base_list_m):
        dolya = round(len(base_list_w)/len(base_list)*100, 3)
        await bot.send_message(
            chat_id=GROUP_DS_55_ID,
            text=f'Гинекократия наметилась.\nПринцессы чата владеют девичьим ридикюлем чата в размере *{dolya}%*', parse_mode="MarkDown")
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

    age_pd = pd.Series(base_list)
    age_pd.hist(bins=25, figsize=(15,10), grid=False, color='skyblue', ec="red", zorder=2, rwidth=1)
    plt.title('Распределение по возрасту')
    plt.ylabel('Количество ДСеров')
    plt.savefig('foo.png')
    plt.close()
    with io.open('foo.png', 'rb') as image:
        await bot.send_photo(GROUP_DS_55_ID, photo=image)

@dp.callback_query_handler(text='myreput')
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
        f'*Генеральный директор уважения* - {mention1}.\n'
        f'Баллы уважения {top_of_rate[0][1]}🦄🦄🦄\n'
        f'*Зам. генерального директора по престижу* - {mention2}.\n'
        f'Уровень престижа {top_of_rate[1][1]}👑👑\n'
        f'*Зам. генерального директора по авторитету* - {mention3}.\n'
        f'Очки авторитета {top_of_rate[2][1]}🐗🐗\n'
        f'*Зам. генерального директора по репутации* - {mention4}.\n' 
        f'Репутационный итог {top_of_rate[3][1]}🌈🌈\n'
        f'*Тамада - баянист* - {mention5}.\n'
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
            chat_id=GROUP_DS_55_ID,
            text=f'Репутация {mention}, на текущий момент составляет - {user_rate_cur[0]} ⭐️\n', parse_mode="MarkDown")
    mykings.clear()

@dp.callback_query_handler(text='mytrue')
async def myrrueds_func(call):
   base_whyds = cur.execute('SELECT id, chat_name, whyds FROM Users WHERE whyds NOT NULL').fetchall()
   one_ds = random.choice(base_whyds)
   rand_emo = ['🤌', '✊🏻', '💪🏻', '🫡']
   mention = "[" + one_ds[1] + "](tg://user?id=" + str(one_ds[0]) + ")"
   mess = (f'Перед тем как прийти сюда, многие задавались вопросом:\n'
                f'Что такое этот *DataSciene?*{random.choice(rand_emo)}'
                f'Когда дедлайн был близок и времени уже не оставалось, я дал слабину.\n'
                f'Подумал, что это не моё, хотел вернуться на домашний диван.\n'
                f'{mention} перубедил(а) всего несколькими словами.\n'
                f'Когда я услышал: *{one_ds[2]}* {random.choice(rand_emo)} я сразу всё понял')
   await bot.edit_message_text(chat_id=GROUP_DS_55_ID, message_id=kingmes[-1],
        text=mess, parse_mode="MarkDown")
   mykings.clear()
@dp.callback_query_handler(text='mybooks')
async def mybooks_func(call):
    book_r = cur.execute('SELECT knigas FROM Blic WHERE knigas NOT NULL').fetchall()
    one_ds = random.choice(book_r)
    mess = (f'Рубрика *уютные рекомендации - книги*\n'
            f'📌{one_ds[0]}📌\n'
            f'Это *явно стоит* прочесть🙊!')
    await bot.edit_message_text(chat_id=GROUP_DS_55_ID, message_id=kingmes[-1],
        text=mess, parse_mode="MarkDown")
    mykings.clear()
@dp.callback_query_handler(text='myfilms')
async def myfilms_func(call):
    fil_r = cur.execute('SELECT films FROM Blic WHERE films NOT NULL').fetchall()
    one_ds = random.choice(fil_r)
    mess = (f'Рубрика *приятные рекомендации - фильмы/сериалы*\n'
            f'📌{one_ds[0]}📌\n'
            f'Это *явно стоит* посмотреть🙈!')
    await bot.edit_message_text(chat_id=GROUP_DS_55_ID, message_id=kingmes[-1],
        text=mess, parse_mode="MarkDown")
    mykings.clear()
@dp.callback_query_handler(text='mymusic')
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
    message_lower = message.text.lower()
    if message_lower.find('старос') > -1:
        sleep(3)
        stick_list = ['CAACAgIAAxkBAAEGv75jk0wFqJ_a9NTkXSSsw0WSPw_zCAACwAADKJcGAAFhjyrXKl5tTisE',
                      'CAACAgIAAxkBAAEGv8Bjk0wN6EqK64c4XQ-SvWM4nuBQVQACjgADKJcGAAEjKuNEWg7P0isE',
                      'CAACAgIAAxkBAAEGv8Jjk0wa-ZW_kOIoH35cRoqwqHlt9QACxwADKJcGAAH4yvn60cNpHCsE',
                      'CAACAgIAAxkBAAEGv8xjk0xdy4-b-KDZMNtpTGcgFPZNlwACswADKJcGAAFx6TKsPKKF-isE']
        forfun = random.choice(stick_list)
        await bot.send_sticker(
            chat_id=GROUP_DS_55_ID,
            sticker=forfun)
    elif message_lower.find('пасиб') > -1:
        await message.answer(
                text=f'Еще бы понять кого ты благодаришь😞')
    elif message_lower.find('календар') > -1:
            file1 = open('study_plan.jpg', 'rb')
            await bot.send_document(message.chat.id, file1)
    elif message_lower.find('цп') > -1:
            mus_rss = cur.execute('SELECT type_educ FROM Users WHERE type_educ NOT NULL').fetchall()
            base_list = [x[0] for x in mus_rss]
            mychet = pd.Series(base_list)
            mystable = mychet.value_counts().plot.bar(color=['pink', 'black'])
            # fig, ax = plt.subplots()
            # ax.bar(mystable, height=1, width=0.8, edgecolor="black", linewidth=0.7, color=['red', 'blue'])
            plt.title('Срез по ЦП')
            plt.savefig('foo.png')
            plt.close()
            with io.open('foo.png', 'rb') as image:
                await bot.send_photo(GROUP_DS_55_ID, photo=image)
    elif message_lower.find('поток') > -1:
            mus_rss = cur.execute('SELECT flow_num FROM Users WHERE flow_num NOT NULL').fetchall()
            base_list = [x[0] for x in mus_rss]
            mychet = pd.Series(base_list)
            mystable = mychet.value_counts().plot.bar(color=['black', 'red', 'green', 'blue', 'cyan'])
            # fig, ax = plt.subplots()
            # ax.bar(mystable, height=1, width=0.8, edgecolor="black", linewidth=0.7, color=['red', 'blue'])
            plt.title('Наши первоначальные когорты')
            plt.savefig('foo.png')
            plt.close()
            with io.open('foo.png', 'rb') as image:
                await bot.send_photo(GROUP_DS_55_ID, photo=image)
    elif message_lower.find('наши города') > -1:
         mus_rss = cur.execute('SELECT city FROM Users WHERE city NOT NULL').fetchall()
         base_list = [x[0] for x in mus_rss]
         mychet = pd.Series(base_list)

         mychet.value_counts().plot.pie(figsize=(15,10), autopct='%.2f', fontsize=8, pctdistance=1.25, radius=1.2)

         plt.title('Наша география')
         plt.savefig('foo.png')
         plt.close()
         with io.open('foo.png', 'rb') as image:
             await bot.send_photo(message.from_user.id, photo=image)

# Техническая часть, чтобы бот работал не уходил в игнор от большого количества запросов.
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
