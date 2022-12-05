
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
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import IsReplyFilter
from aiogram.dispatcher.filters.state import StatesGroup, State



# Базовые настройки для соединения с созданным ботом
API_TOKEN = 'Token'
bot = Bot(token=API_TOKEN)
dp  = Dispatcher(bot, storage=MemoryStorage())
# Подключаемся/создаем базу данных
bd = sqlite3.connect('datasciense.db')
cur = bd.cursor()

# Создаем таблицу(если её еще не существет) всех пользователей чатика. Столбцы: id, имя в чате, пол, возраст, город, репутация, библиотека-роль, о себе, почему ДС)
bd.execute('CREATE TABLE IF NOT EXISTS Users (id int NOT NULL, chat_name NULL, sex NULL, age int NULL, city NULL, rep int, libstate NULL, aself NULL, whyds NULL, PRIMARY KEY(id))')
# НЕ ПРИОРИТЕТНАЯ ЗАДАЧА Создаем таблицу данных блица, ответы будем визуализировать графиками:
bd.execute('CREATE TABLE IF NOT EXISTS Blic (id int NOT NULL, cat_dog NULL, pizza_suchi NULL, sea_mount NULL, flat_house NULL, train_plain NULL, tea_coffe NULL, tv_tube NULL, andr_ios NULL,  tatoo NULL, drive NULL, parent_kid NULL, PRIMARY KEY(id))')
# Создаем таблицу по функциям:
bd.execute('CREATE TABLE IF NOT EXISTS Base (id NOT NULL, name NULL, desc NULL, fullv NULL, args NULL, example NULL, dopinfo NULL, erors NULL, meth_args NULL, cat1 NULL, cat2 NULL, cat3 NULL, file NULL, PRIMARY KEY(id))')
# команда подтверждающая изменения в БД
bd.commit()

# инлайн  кнопки для основного меню и реакцию на старт
button1 = InlineKeyboardButton(text='ПРОФИЛЬ🧐', callback_data='profile')
button2 = InlineKeyboardButton(text='БЛИЦ🧾', callback_data='blic')
button3 = InlineKeyboardButton(text='СКЛАД ДС💌', callback_data='base')
button4 = InlineKeyboardButton(text='ОСНОВНОЕ МЕНЮ', callback_data='menu')

# реакция на команду /start
@dp.message_handler(CommandStart())
# назначим функцию, которая принимает текстовое сообщение от пользователя
async def first_step(message: types.Message):
    # переменная с id пользователя ТГ
    user_id = message.from_user.id
    # высосываем из базы инфу по тем, кто уже есть в базе
    fellows = cur.execute('SELECT id FROM Users').fetchall()
    # так как инфа высасывается в виде кортежей (значения в скобках) распакуем кортежи, чтобы значение выводилось без лишних символов
    fellows_list = [x[0] for x in fellows]
    # создадим клавиуатуру, которую покажем пользователю
    MainMenu = InlineKeyboardMarkup(row_width=2)
    # добавим в неё три кнопки
    MainMenu.insert(button1)
    #MainMenu.insert(button2)
    #MainMenu.insert(button3)
    # пишем саму реакцию: бот отправляет в личную беседу с юзером стикер-приветствие
    await bot.send_sticker(chat_id=user_id, sticker="CAACAgIAAxkBAAEGFaxjSSZR18Rg3M4DobRVMNWUcDoEeQACwwIAAqKK8QdgnyDY1-DSlioE")
    welcome = 'Я знаю только то, что я староста. Приходи потом, возможно инфы появится больше'
    # напишем сценарий для случаев, если юзер уже в базе
    if user_id in fellows_list:
        # получим ник, который он указал при заполнении профиля
        # переменная с текстовым сообщением приветствием
        fellow_message = f'Рад снова тебя видеть, {message.from_user.first_name}. Нас уже {len(fellows_list)}'
        # сама реакция, бот отвечает приветственным сообщением
        await bot.send_message(chat_id=user_id,text=fellow_message, parse_mode="MarkDown", reply_markup=MainMenu)
        # получим информацию участвовал ли этот юзер в блице
        victory_id = cur.execute('SELECT id FROM Blic').fetchall()
        victory_id_list = [x[0] for x in victory_id]
        # сценарий если участвовал
        if user_id in victory_id_list:
            good_person = f'Твой профиль заполнен. Твоя викторина пройдена.'
            await bot.send_message(chat_id=user_id, text=welcome, parse_mode="MarkDown")
        # сценарий если не участвовал
        elif user_id not in victory_id_list:
            vitctorina_user = f'Твой профиль заполнен, но ты не прошёл викторину. Пройди, когда будет время. Мне нужны данные для настоящего Дата Саенс'
            await bot.send_message(chat_id=user_id, text=welcome, parse_mode="MarkDown")
        # ловим ошибку
        else:
            await message.answer(text='Ошибка, напиши моим авторам')
    # напишем сценарий для случаев, если юзер не в базе
    elif user_id not in fellows_list:
        #welcome = (f'Привяу, я Арсений, но друзья зовут меня про Сеня. Я тоже учился на Яндекс Практикуме, но так и не смог завершить \n'
         #           f'Я много учился раньше, а сейчас помогаю тем, кто учиться прямо сейчас. Кстати благодаря курсу я нашёл {len(fellows_list)} друзей. Нажми кнопку "ПРОФИЛЬ" чтобы посмотреть профили товарищей и рассказать чуть больше о себе\n'
          #          f'Еще я провожу мини-исследования. Нажми кнопку "БЛИЦ", чтобы ответить на небольшой блиц и поделиться рекомендациями по фильмам, книгам, музыке\n'
           #         f'А еще я собираю полезную информацию по инструментам Python инструментом для ДС. Нажми кнопку "СКЛАД ДС", чтобы просветиться или добавить просветительского контента\n')

        cur.execute('INSERT INTO Users(id, rep) VALUES(?, ?)', (user_id, 0))
        bd.commit()
        await bot.send_message(chat_id=user_id, text=welcome, parse_mode="MarkDown")

# Заготовка для работы непосредственно с библиотекой. Недоработана
@dp.callback_query_handler(text='base')
async def myfunc(call):
    funcs = cur.execute('SELECT func FROM Base WHERE func NOT NULL').fetchall()
    funcs_list = [x[0] for x in funcs]
    buttonb1 = InlineKeyboardButton(text='СПИСОК', callback_data='funlis')
    buttonb2 = InlineKeyboardButton(text='ДОБАВИТЬ', callback_data='addfun')
    BaseMenu = InlineKeyboardMarkup(row_width=2)
    BaseMenu.insert(buttonb1)
    BaseMenu.insert(buttonb2)
    base_mes = f'Это библиотека полезных функций. Сейчас в библиотеке {len(funcs_list)} функций. Нажми "СПИСОК" чтобы посмотреть библиотеку. Нажми "ДОБАВИТЬ" чтобы добавить информацию по новой функции'
    await bot.send_message(chat_id=call.from_user.id, text=base_mes, parse_mode="MarkDown")

# Заготовка для реакции на кнопку СПИСОК
@dp.callback_query_handler(text='funlis')
async def funlist(call):
    funcs = cur.execute('SELECT func FROM Base WHERE func NOT NULL').fetchall()
    funcs_list = [x[0] for x in funcs]
    await bot.send_message(chat_id=call.from_user.id, text=funcs_list, parse_mode="MarkDown", reply_markup=BaseMenu)




# Заготовка для реакции на кнопку ДОБАВИТЬ
@dp.callback_query_handler(text='addfun')
async def addfun(call):
    funcs = cur.execute('SELECT func FROM Base WHERE func NOT NULL').fetchall()
    funcs_list = [x[0] for x in funcs]
    await bot.send_message(chat_id=call.from_user.id, text=funcs_list, parse_mode="MarkDown", reply_markup=BaseMenu)


class Profile(StatesGroup):
    ProfileSex = State()
    ProfileAge = State()
    ProfileCity = State()
    ProfileAself = State()
    ProfileWhyDs = State()

@dp.callback_query_handler(text='profile')
async def pro_file(call):
    user_id = call.from_user.id
    myprofile  = cur.execute('SELECT sex FROM Users WHERE id=' + str(user_id)).fetchone()
    mycheck = cur.execute('SELECT * FROM Users WHERE id=' + str(user_id)).fetchone()
    button11 = InlineKeyboardButton(text='Заполнить профиль', callback_data='addprofile')
    #button22 = InlineKeyboardButton(text='Посмотреть профили', callback_data='lookprofile')
    if myprofile is not None:
        myinfo = (f'*Карточка начинающего ДСера*\n'
                    f'*Позывной*: {mycheck[1]}\n'
                    f'*Пол*: {mycheck[2]}\n'
                    f'*Возраст*: {mycheck[3]}\n'
                    f'*Город*: {mycheck[4]}\n'
                    f'*Репутация*: {mycheck[5]}\n'
                    f'*О себе*:{mycheck[7]}\n'
                    f'*Почему DS*: {mycheck[8]}\n')
        ProfileMenu = InlineKeyboardMarkup(row_width=2)
        ProfileMenu.insert(button11)
        #ProfileMenu.insert(button22)
        ProfileMenu.insert(button4)
        await bot.send_message(chat_id=user_id, text=myinfo, parse_mode="MarkDown", reply_markup=ProfileMenu)
    elif myprofile is None:
        ProfileMenu1 = InlineKeyboardMarkup(row_width=2)
        ProfileMenu1.insert(button11)
        #ProfileMenu1.insert(button22)
        ProfileMenu1.insert(button4)
        await bot.send_message(chat_id=call.from_user.id, text='Сделай доброе DS-дело, хороший человек, заполни профиль!', parse_mode="MarkDown", reply_markup=ProfileMenu1)
@dp.callback_query_handler(text='addprofile')
async def addprofile_new(call):
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    ProfileSex = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text='Мужской🧔🏻‍♂️', callback_data='iman')
    button2 = InlineKeyboardButton(text='Женский👩🏻‍🦰', callback_data='iwomen')
    button3 = InlineKeyboardButton(text='Другой🧌', callback_data='inone')
    ProfileSex.insert(button1)
    ProfileSex.insert(button2)
    ProfileSex.insert(button3)
    await bot.send_message(chat_id=user_id, text='Чудесно, актуальная информация - клад для молодого DS-ера. Сейчас я задам тебе несколько вопросов. Сначала укажи свой пол', parse_mode="MarkDown",  reply_markup=ProfileSex)
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
        if int(mes) > 18 and int(mes) < 88:
            cur.execute('UPDATE Users SET age == ? WHERE id == ?', (mes, user_id))
            bd.commit()
            await bot.send_message(chat_id=user_id,
                               text='Хорошо, теперь напиши из какого ты города')
            await  Profile.ProfileCity.set()
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
    if len(mes) > 3 and len(mes) < 25:
        cur.execute('UPDATE Users SET city == ? WHERE id == ?', (mes, user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text='Пару слов о себе')
        await  Profile.ProfileAself.set()
    else:
        await bot.send_message(chat_id=user_id,
                               text = 'Что за город такой? Выдуманный чтоли?')
@dp.message_handler(state= Profile.ProfileAself)
async def aself_ds(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    mes = message.text
    if len(mes) > 5 and len(mes) < 188:
        cur.execute('UPDATE Users SET aself == ? WHERE id == ?', (mes, user_id))
        bd.commit()
        await bot.send_message(chat_id=user_id,
                               text='Ну и финалочка. Почему выбрал/выбрала DS?')
        await  Profile.ProfileWhyDs.set()
    else:
        await bot.send_message(chat_id=user_id,
                               text='Надо написать хоть то-то дельное')
@dp.message_handler(state=Profile.ProfileWhyDs)
async def my_ds(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    mes = message.text
    if len(mes) > 5 and len(mes) < 188:
        cur.execute('UPDATE Users SET whyds == ? WHERE id == ?', (mes, user_id))
        bd.commit()
        await state.reset_state()
        mycheck = cur.execute('SELECT * FROM Users WHERE id=' + str(user_id)).fetchone()
        myinfo = (f'*Карточка начинающего ДСера*\n'
                    f'*Позывной*: {mycheck[1]}\n'
                    f'*Пол*: {mycheck[2]}\n'
                    f'*Возраст*: {mycheck[3]}\n'
                    f'*Город*: {mycheck[4]}\n'
                    f'*Репутация*: {mycheck[5]}\n'
                    f'*О себе*:{mycheck[7]}\n'
                    f'*Почему DS*: {mycheck[8]}\n')
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
        maga_phrase = ['Ну что сказать, ну что сказать, человек мой дорогой?',
                       'Магомед - мой знакомец, мы с ним любить поюморить',
                       'Да ты мне не рассказывай, ты им рассказывай',
                       'Да тут и так всё понятно, вопросов -1',
                       'Ты пойми, эти роботы, это все к не добру',
                       'Ты меня уважаешь???',
                       'Потому что есть Алёшка у тебя',
                       'По статистике каждый ДСер еще тот аналитик',
                       'Как-то раз заснул и сниться мне p-value',
                       'Ну вот скажи, мне студент, в чем сила?'
                       'Моё уважение = твоё уважение',
                       'Ты тут кого-нибудь знаешь? Им можно доверять?',
                       'Я импортозамещеный искуственный интеллект. Прекол?']
        forfun = random.choice(maga_phrase)
        await message.answer(
            text=forfun, parse_mode="MarkDown")
    elif message_lower.find('пасиб')> -1 or message_lower.find('лагодар')> -1:
        if user_id == rep_id:
            await message.answer(
                text=f'{mention_rep} ты так-то человечек хороший. Все это уже поняли. Может про DS что нить накидаешь?',
                parse_mode="MarkDown")
        elif user_id != rep_id:
            user_rate_cur = cur.execute('SELECT rep FROM Users WHERE id=' + str(rep_id)).fetchone()
            if user_rate_cur == None:
                await message.answer(
                    text=f'{rep_name}, к сожалению, я тебя знаю и не могу повысить твою репутацию. Напиши /start, чтобы это исправить',
                    parse_mode="MarkDown")
            elif user_rate_cur[0] >= 0:
                user_rate_fin = user_rate_cur[0] + 1
                funfact = ['приятный человек и мудрый собеседник.',
                           'всегда сумеет найти нужные слова.',
                           'человек с большой Буквы.',
                           'ты просто наиприятнейшая личность в контексте DS',
                           'цветок добра',
                           'расшарил(а) мудрость',
                           'авторитетен и ТОЧКА',
                           'задаёт хороший тон',
                           'умеет делать красиво',
                           'от души душевно в душу - часто слышишь?']
                forfun = random.choice(funfact)
                await message.answer(text=f' {mention_rep} {forfun}.\n+1 в твою личную коллекцию благодарностей.\nУровень коллективной благодарности: {user_rate_fin} ⭐️', parse_mode="MarkDown")
                cur.execute('UPDATE Users SET rep == ? WHERE id == ?', (user_rate_fin, rep_id))
                bd.commit()
    elif message_lower.find('профил') > -1:
        mycheck = cur.execute('SELECT * FROM Users WHERE id=' + str(rep_id)).fetchone()
        if mycheck[4] == None:
            await bot.send_message(chat_id=message.chat.id, text=f'{rep_name} пока еще не чувствует себя ДСером, у него нет профиля и ему нечего рассказывать о себе', parse_mode="MarkDown")


        elif len(mycheck[7]) >= 3:
            myinfo = (f'*Профиль {rep_name}*\n'
                    f'*Позывной*: {mycheck[1]}\n'
                    f'*Пол*: {mycheck[2]}\n'
                    f'*Возраст*: {mycheck[3]}\n'
                    f'*Город*: {mycheck[4]}\n'
                    f'*Репутация*: {mycheck[5]}\n'
                    f'*О себе*:{mycheck[7]}\n'
                    f'*Почему DS*: {mycheck[8]}\n')
            await bot.send_message(chat_id=message.from_user.id, text=myinfo, parse_mode="MarkDown")


@dp.message_handler(commands=['info'])
async def bd_info(message: types.Message):
    user_id = message.from_user.id
    base_count = cur.execute('SELECT id FROM Users').fetchall()
    base_info = cur.execute('SELECT age FROM Users WHERE age > 0').fetchall()
    base_info_m = cur.execute('SELECT age FROM Users WHERE age > 0 AND sex == "man"').fetchall()
    base_info_w = cur.execute('SELECT age FROM Users WHERE age > 0 AND sex == "woman"').fetchall()
    base_list = [x[0] for x in base_info]
    base_list_m = [x[0] for x in base_info_m]
    base_list_w = [x[0] for x in base_info_w]
    user_age_avg = sum(base_list) / len(base_list)
    user_age_avg_m = sum(base_list_m) / len(base_list_m)
    user_age_avg_w = sum(base_list_w) / len(base_list_w)
    mess = (f'С вашего позволения, я поделюсь *аналитикой по чату*:\n'
            f'На текущую секундочку в чате {len(base_list)} *настоящих и идентифицированных ДСеров*.\n'
            f'Средний возраст *элиты* чата *{round(user_age_avg, 2)}. 🗿 - {round(user_age_avg_m, 2)} 👩🏻‍🦰 - {round(user_age_avg_w, 2)}*\n'
            f'Они люди уважаемые, поэтому для них *двойной* почёт.\n'
            f'Остальным {len(base_count)-len(base_list)} невидимкам рекомендую не стыдиться себя и заполнить свой *true профиль* начинающего ДСера')
    await message.answer(text=mess, parse_mode="MarkDown")
    sleep(3)
    if len(base_list_w) > len(base_list_m):
        await message.answer(text=f'Наши барышни заседают на царстве большинства.\n Их доля - *{round(len(base_list_w)/len(base_list), 2)} Мужички на подхвате*', parse_mode="MarkDown")
    elif len(base_list_w) > len(base_list_m):
        await message.answer(text=f'Неужели мужички на царстве? *Доля образцов DS-мужственности🗿🗿🗿 - {round(len(base_list_m)/len(base_list), 2)} Это что гараж?*', parse_mode="MarkDown")
    elif len(base_list_w) == len(base_list_m):
        await message.answer(
            text=f'Я люблю когда так бывает. Объявляю половое равенство в чате', parse_mode="MarkDown")
@dp.message_handler(commands=['whyds'])
async def why_ds(message: types.Message):
    user_id = message.from_user.id
    base_whyds = cur.execute('SELECT chat_name, whyds FROM Users WHERE whyds NOT NULL').fetchall()
    one_ds = random.choice(base_whyds)
    rand_emo = ['🤌', '✊🏻', '💪🏻', '🫡']
    mess = (f'Меня часто спрашивают "**Чем же так хорош этот ваш датасенс🥸???**"\n'
            f'В такие моменты я сразу вспоминаю *слова {one_ds[0]}* 🫶\n'
            f'Мы в тот день засиделись в библиотеке: таблицы, графики, усы, p-value. Когда силы начали покидать😵, я спросил в отчаянии для чего всё это???\n'
            f'Ответ был: *{one_ds[1]}*{random.choice(rand_emo)}')
    await message.answer(
        text=mess, parse_mode="MarkDown")


@dp.message_handler(commands=['myrep'])
async def my_rep(message: types.Message):
    user_id = message.from_user.id
    user_rate_cur = cur.execute('SELECT rep FROM Users WHERE id=' + str(user_id)).fetchone()
    user_name = message.from_user.first_name
    mention = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    if user_rate_cur == None:
        await message.answer(
            text=f'EERRORR>>> USER NOT FOUND!!!! {mention}, твой авторитет мне неизвестен\nВозможно пришло время дать /start нашему знакомству?',
            parse_mode="MarkDown")
    else:
        await message.answer(
            text=(f'Авторитетность {mention}, на текущий момент составляет: {user_rate_cur[0]} ⭐️\n'
                 f'Достаточно авторитетно, как считаете?'),
            parse_mode="MarkDown")

@dp.message_handler(commands=['toprep'])
async def top_rep(message: types.Message):
    top_of_rate = cur.execute('SELECT id, rep FROM Users ORDER BY rep DESC').fetchall()
    chat_member1 = await bot.get_chat_member(chat_id=message.chat.id, user_id=top_of_rate[0][0])
    first_name1 = chat_member1.user.first_name
    mention1= "[" + first_name1 + "](tg://user?id=" + str(top_of_rate[0][0]) + ")"
    chat_member2 = await bot.get_chat_member(chat_id=message.chat.id, user_id=top_of_rate[1][0])
    first_name2 = chat_member2.user.first_name
    mention2 = "[" + first_name2 + "](tg://user?id=" + str(top_of_rate[1][0]) + ")"
    chat_member3 = await bot.get_chat_member(chat_id=message.chat.id, user_id=top_of_rate[2][0])
    first_name3 = chat_member3.user.first_name
    mention3 = "[" + first_name3 + "](tg://user?id=" + str(top_of_rate[2][0]) + ")"
    chat_member4 = await bot.get_chat_member(chat_id=message.chat.id, user_id=top_of_rate[3][0])
    first_name4 = chat_member4.user.first_name
    mention4 = "[" + first_name4 + "](tg://user?id=" + str(top_of_rate[3][0]) + ")"
    chat_member5 = await bot.get_chat_member(chat_id=message.chat.id, user_id=top_of_rate[4][0])
    first_name5 = chat_member5.user.first_name
    mention5 = "[" + first_name5 + "](tg://user?id=" + str(top_of_rate[4][0]) + ")"
    fin_mes = (f'Извольте ознакомиться с самыми приятными собеседниками:\n'
              f'Генеральный директор уважения - {mention1}.\n'
                f'Баллы уважения {top_of_rate[0][1]}🦄🦄🦄\n'
              f'Зам. генерального директора по престижу - {mention2}.\n'
               f'Уровень престижа {top_of_rate[1][1]}👑👑\n'
            f'Зам. генерального директора по авторитету - {mention3}.\n'
               f'Очки авторитета {top_of_rate[2][1]}🐗🐗\n'
              f'Зам. генерального директора по репутации - {mention4}.\n' 
               f'Репутационный итог {top_of_rate[3][1]}🌈🌈\n'
              f'Тамада - баянист - {mention5}.\n'
               f'Удачных мероприятий {top_of_rate[4][1]}🕺💃\n')
    await message.answer(text=fin_mes, parse_mode="MarkDown")
    await bot.send_sticker(chat_id=message.chat.id, sticker='CAACAgIAAxkBAAEGrxhjjPPBUTZ153IUAAG661RGhtPvM54AArEKAAKVi-FJbx85rlVi_BQrBA')



# Новичок в группе
@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def New_member(message):
    await message.answer(f"У нас пополнение - {message.new_chat_members[0].get_mention(as_html=True)}. Вкратце расскажи про свой путь DSeра, нам реально интересно", parse_mode='HTML')
    await bot.send_sticker(chat_id=message.chat.id, sticker='CAACAgIAAxkBAAEGl9tjhNncRF99x78OPh02Wk6byzBeEgACXgwAApS4UEtOn6EuKYdYXisE')


@dp.message_handler(content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def Del_member(message):
    await message.answer(f"Фиксирую убытие - {message.new_chat_members[0].get_mention(as_html=True)}. Это как понимать, дорогие ребята?", parse_mode='HTML')
    await bot.send_sticker(chat_id=message.chat.id, sticker='CAACAgIAAxkBAAEGqChjinr2MwuV2m87-mQYTz1PQAb5mwACFAEAA5rPDQJgUE8KmjDVKwQ')
# Заготовка для реакции на кнопку БЛИЦ
@dp.callback_query_handler(text='blic')
async def blic(call):
    user_id = call.from_user.id
    mypvic = cur.execute('SELECT id FROM Blic').fetchall()
    mypvic_list = [x[0] for x in  mypvic]
    button11 = InlineKeyboardButton(text='Пройти викторину', callback_data='addvictory')
    if user_id in mypvic_list:
        mypvic = cur.execute('SELECT * FROM Victorina WHERE id=' + str(user_id)).fetchone()
        myansw = (f'Мои ответы на викторину:\n'
                  f'Кошки/собаки: {mypvic[1]}\n'
                  f'Пицца/суши: {mypvic[2]}\n'
                  f'Море/горы: {mypvic[3]}\n'
                  f'Квартира/дом: {mypvic[4]}\n'
                  f'Самолет/поезд:{mypvic[5]}\n'
                  f'Чай/кофе: {mypvic[6]}\n'
                  f'ТВ/Youtube: {mypvic[7]}\n'
                  f'Татуировки: {mypvic[8]}\n'
                  f'Водительство: {mypvic[9]}\n'
                  f'Моя музыка: {mypvic[10]}\n'
                  f'Мои фильмы: {mypvic[11]}\n'
                  f'Мои книги: {mypvic[12]}\n')
        VictorinaMenu = InlineKeyboardMarkup(row_width=2)
        VictorinaMenu.insert(button11)
        VictorinaMenu.insert(button4)
        await bot.send_message(chat_id=call.from_user.id, text=myansw, parse_mode="MarkDown", reply_markup=VictorinaMenu)
    elif user_id in mypvic_list:
        VictorinaMenu1 = InlineKeyboardMarkup(row_width=2)
        VictorinaMenu1.insert(button11)
        VictorinaMenu1.insert(button4)
        await bot.send_message(chat_id=call.from_user.id, text='Ты еще не прошёл викторину. Сейчас готов?', parse_mode="MarkDown", reply_markup=VictorinaMenu1)

# Реакция на кнопку возврата в основное меню(клавиатура)
@dp.callback_query_handler(text='menu')
async def menu(call):
    MainMenu = InlineKeyboardMarkup(row_width=2)
    MainMenu.insert(button1)
    #MainMenu.insert(button2)
    #MainMenu.insert(button3)
    await bot.send_message(chat_id=call.from_user.id, text='ОСНОВНОЕ МЕНЮ', parse_mode="MarkDown", reply_markup=MainMenu)

# Заготовка для реакции на кнопку ЗАПОЛНЕНИЯ ПРОФИЛЯ
#@dp.callback_query_handler(text='addprofile')
#async def addprofile(call):

@dp.message_handler()
async def check_user(message: types.Message):
    chat_name = message.from_user.first_name
    user_id = message.from_user.id
    fellows = cur.execute('SELECT id FROM Users').fetchall()
    fellows_list = [x[0] for x in fellows]
    if user_id not in fellows_list:
        cur.execute('INSERT INTO Users(id, rep) VALUES(?, ?)', (user_id, 0))
        bd.commit()

# Техническая часть, чтобы бот работал не уходил в игнор от большого количества запросов.
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)