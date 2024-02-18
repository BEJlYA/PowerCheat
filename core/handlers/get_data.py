import sqlite3
import requests
from aiogram import Bot
from aiogram.types import Message
from core.settings import settings
from core.keyboards.reply_fb import *
from core.keyboards.reply_sett import *
from core.keyboards.reply_menu import *
from core.keyboards.reply_acc import accou
from aiogram.fsm.context import FSMContext
from core.utils.data_states import DataSteps
from core.handlers.basic_def import account, setting


async def login(message: Message, state: FSMContext):
    await message.answer('Укажите ваш логин:', reply_markup=inputs)
    await state.set_state(DataSteps.LOGIN)


async def get_login(message: Message, state: FSMContext):
    if message.text == '◀Назад':
        await state.set_state(None)
        await account(message)
    elif message.text == '♻Очистить':
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        cursor.execute("""UPDATE profiles SET login = 'Отсутствует' WHERE chat_id = ?""", (message.chat.id,))
        connection.commit()
        await state.set_state(None)
        await account(message)
    else:
        await message.answer('Логин принят для обработки!', reply_markup=accou)
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        cursor.execute("""UPDATE profiles SET login = ? WHERE chat_id = ?""", (message.text, message.chat.id,))
        connection.commit()
        await state.set_state(None)


async def password(message: Message, state: FSMContext):
    await message.answer('Укажите ваш пароль:', reply_markup=inputs)
    await state.set_state(DataSteps.PASSWORD)


async def get_password(message: Message, state: FSMContext):
    if message.text == '◀Назад':
        await state.set_state(None)
        await account(message)
    elif message.text == '♻Очистить':
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        cursor.execute("""UPDATE profiles SET password = 'Отсутствует' WHERE chat_id = ?""", (message.chat.id,))
        connection.commit()
        await state.set_state(None)
        await account(message)
    else:
        await message.answer('Пароль принят для обработки!', reply_markup=accou)
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        cursor.execute("""UPDATE profiles SET password = ? WHERE chat_id = ?""", (message.text, message.chat.id,))
        connection.commit()
        await state.set_state(None)


async def proxy(message: Message, state: FSMContext):
    await message.answer('Укажите HTTP/HTTPS прокси <i>(прим. 012.34.567.890:1111)</i>:', reply_markup=inputs)
    await state.set_state(DataSteps.PROXY)


async def get_proxy(message: Message, state: FSMContext):
    if message.text == '◀Назад':
        await state.set_state(None)
        await account(message)
    elif message.text == '♻Очистить':
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        cursor.execute("""UPDATE profiles SET proxy = 'Отсутствуют' WHERE chat_id = ?""", (message.chat.id,))
        connection.commit()
        await state.set_state(None)
        await account(message)
    else:
        try:
            await message.answer('Выполняется проверка ваших прокси. <i>(Максимальное время ожидания - 5 сек.)</i>')
            r = requests.get(url='https://www.httpbin.org/ip',
                             proxies={'http': f'{message.text}', 'https': f'{message.text}'},
                             timeout=5)
            ip = message.text.split(':')
            if ip[0] in r.text:
                await message.answer('Прокси приняты!', reply_markup=accou)
                connection = sqlite3.connect('data/users.db')
                cursor = connection.cursor()
                cursor.execute("""UPDATE profiles SET proxy = ? WHERE chat_id = ?""", (message.text, message.chat.id,))
                connection.commit()
                await state.set_state(None)
        except requests.exceptions.ConnectionError:
            await message.answer('Укажите другие прокси, введенные не работают...', reply_markup=inputs)


async def feedback(message: Message, state: FSMContext):
    connection = sqlite3.connect('data/users.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT Count(*) FROM feedback""")
    val_fb = cursor.fetchone()
    connection.commit()
    if message.chat.id == settings.bots.admin_id:
        await message.answer(f'Количество обращений к разработчику: <b>{val_fb[0]}</b>\n'
                             f'Что желаете делать?', reply_markup=answ)
        await state.set_state(DataSteps.ANSW_M)
    else:
        await message.answer('Напишите ваше обращение к разработчику бота:', reply_markup=febck)
        await state.set_state(DataSteps.FEEDBACK)


async def answer_menu(message: Message, state: FSMContext, bot=Bot(token=settings.bots.bot_token)):
    if message.text == '📡Ответить':
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        cursor.execute("""SELECT * from feedback""")
        if cursor.fetchone() is None:
            connection.commit()
            await state.set_state(None)
            await message.answer('Обращения отсутствуют!', reply_markup=menus)
        else:
            cursor.execute("""SELECT message, user from feedback""")
            message_fb, user = cursor.fetchone()
            connection.commit()
            await message.answer('Обращение от пользователя:', reply_markup=ansfd)
            await bot.forward_message(settings.bots.admin_id, user, message_fb)
            await state.set_state(DataSteps.ANSW)
    elif message.text == '◀Вернуться':
        await state.set_state(None)
        await message.answer('Вы вернулись в Меню.', reply_markup=menus)
    else:
        await message.answer('Такая команда у меня отсутствует...', reply_markup=answ)


async def answer(message: Message, state: FSMContext, bot=Bot(token=settings.bots.bot_token)):
    if message.text == '‼Удалить':
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM feedback WHERE rowid = (SELECT rowid FROM feedback LIMIT 1);""")
        connection.commit()
        await message.answer('Обращение удалено из очереди!', reply_markup=ansfd)
    elif message.text == '◀Вернуться':
        await state.set_state(None)
        await message.answer('Вы вернулись в Меню.', reply_markup=menus)
    else:
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        cursor.execute("""SELECT message, user from feedback""")
        message_fb, user = cursor.fetchone()
        connection.commit()
        await bot.send_message(user, message.text, reply_to_message_id=message_fb)
        await message.answer('Ответ отправлен пользователю!', reply_markup=ansfd)
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM feedback WHERE rowid = (SELECT rowid FROM feedback LIMIT 1);""")
        cursor.execute("""SELECT * FROM feedback""")
        if cursor.fetchone() is None:
            connection.commit()
            await state.set_state(None)
            await message.answer('Обращения от пользователей закончились!', reply_markup=menus)
        else:
            cursor.execute("""SELECT message, user from feedback""")
            message_fb, user = cursor.fetchone()
            connection.commit()
            await bot.forward_message(settings.bots.admin_id, user, message_fb)


async def get_feedback(message: Message, state: FSMContext):
    if message.text == '◀Вернуться':
        await state.set_state(None)
        await message.answer('Вы вернулись в Меню.', reply_markup=menus)
    else:
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO feedback  (message, user) VALUES (?, ?)""", (message.message_id, message.chat.id,))
        connection.commit()
        await message.answer('Ваше сообщение отправлено, ожидайте пожалуйста.', reply_markup=menus)
        await state.set_state(None)


async def fight(message: Message, state: FSMContext):
    await message.answer('Введите кол-во проводимых боёв:', reply_markup=inputs)
    await state.set_state(DataSteps.FIGHT)


async def get_fight(message: Message, state: FSMContext):
    if message.text == '◀Назад':
        await state.set_state(None)
        await setting(message)
    elif message.text == '♻Очистить':
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        cursor.execute("""UPDATE profiles SET fight = 'Отсутствует' WHERE chat_id = ?""", (message.chat.id,))
        connection.commit()
        await state.set_state(None)
        await setting(message)
    else:
        if message.text.isdigit():
            await message.answer('Параметр принят!', reply_markup=sett)
            connection = sqlite3.connect('data/users.db')
            cursor = connection.cursor()
            cursor.execute("""UPDATE profiles SET fight = ? WHERE chat_id = ?""", (message.text, message.chat.id,))
            connection.commit()
            await state.set_state(None)
        else:
            await message.answer('Требуется ввести числовое значение!', reply_markup=inputs)


async def heal(message: Message, state: FSMContext):
    await message.answer('Функция отключена...', reply_markup=sett)
    # await message.answer('Включить авто-лечение?', reply_markup=onoff)
    # await state.set_state(DataSteps.HEAL)


async def get_heal(message: Message, state: FSMContext):
    if message.text == '✅Включить':
        await message.answer('Авто-лечение включено!', reply_markup=sett)
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        cursor.execute("""UPDATE profiles SET heal = ? WHERE chat_id = ?""", ('Включено', message.chat.id,))
        connection.commit()
        await state.set_state(None)
    elif message.text == '❌Отключить':
        await message.answer('Авто-лечение отключено!', reply_markup=sett)
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        cursor.execute("""UPDATE profiles SET heal = ? WHERE chat_id = ?""", ('Отключено', message.chat.id,))
        connection.commit()
        await state.set_state(None)


async def drop(message: Message, state: FSMContext):
    await message.answer('Введите предмет/ы из покемона:', reply_markup=inputs)
    await state.set_state(DataSteps.ITEM)


async def get_item(message: Message, state: FSMContext):
    if message.text == '◀Назад':
        await state.set_state(None)
        await setting(message)
    elif message.text == '♻Очистить':
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        cursor.execute("""UPDATE profiles SET items = 'Отсутствует' WHERE chat_id = ?""", (message.chat.id,))
        connection.commit()
        await state.set_state(None)
        await setting(message)
    else:
        await message.answer('Значение принято!', reply_markup=sett)
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        cursor.execute("""UPDATE profiles SET items = ? WHERE chat_id = ?""", (message.text, message.chat.id,))
        connection.commit()
        await state.set_state(None)


async def catch(message: Message, state: FSMContext):
    await message.answer('Введите "Имя покемона" <i>(через пробел для выбора нескольких покемонов)</i>:', reply_markup=inputs)
    await state.set_state(DataSteps.POK)


async def get_pok(message: Message, state: FSMContext):
    if message.text == '◀Назад':
        await state.set_state(None)
        await setting(message)
    elif message.text == '♻Очистить':
        await state.set_state(None)
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        cursor.execute(
            """UPDATE profiles SET catch = 'Отсутствует', gender = 'Отсутствует', pokebol = 'Отсутствует' WHERE chat_id = ?""", (message.chat.id,))
        connection.commit()
        await setting(message)
    else:
        await message.answer('Покемон принят!\n'
                             'Выберите желаемый гендер:', reply_markup=genders)
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        cursor.execute("""UPDATE profiles SET catch = ? WHERE chat_id = ?""", (message.text, message.chat.id,))
        connection.commit()
        await state.set_state(DataSteps.GENDER)


async def get_gender(message: Message, state: FSMContext):
    if message.text == '◀Назад':
        await state.set_state(None)
        await setting(message)
    elif message.text == '♻Очистить':
        await state.set_state(None)
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        cursor.execute(
            """UPDATE profiles SET catch = 'Отсутствует', gender = 'Отсутствует', pokebol = 'Отсутствует' WHERE chat_id = ?""", (message.chat.id,))
        connection.commit()
        await setting(message)
    else:
        await message.answer('Гендер принят!\n'
                             'Выберите используемый бол:', reply_markup=pokebols)
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        cursor.execute("""UPDATE profiles SET gender = ? WHERE chat_id = ?""", (message.text, message.chat.id,))
        connection.commit()
        await state.set_state(DataSteps.BOL)


async def get_bol(message: Message, state: FSMContext):
    await message.answer('Покебол принят!', reply_markup=sett)
    connection = sqlite3.connect('data/users.db')
    cursor = connection.cursor()
    cursor.execute("""UPDATE profiles SET pokebol = ? WHERE chat_id = ?""", (message.text, message.chat.id,))
    connection.commit()
    await state.set_state(None)


async def shines(message: Message, state: FSMContext):
    await message.answer('Ловить шайни-покемонов?', reply_markup=onoff)
    await state.set_state(DataSteps.SHINE)


async def get_shines(message: Message, state: FSMContext):
    if message.text == '✅Да':
        await message.answer('Ловля включена!', reply_markup=sett)
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        cursor.execute("""UPDATE profiles SET shine = ? WHERE chat_id = ?""", ('Включено', message.chat.id,))
        connection.commit()
        await state.set_state(None)
    elif message.text == '❌Нет':
        await message.answer('Ловля отключена!', reply_markup=sett)
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        cursor.execute("""UPDATE profiles SET shine = ? WHERE chat_id = ?""", ('Отключено', message.chat.id,))
        connection.commit()
        await state.set_state(None)
    else:
        await message.answer('Такая команда у меня отсутствует...', reply_markup=onoff)


async def stop_browser(message: Message, state: FSMContext):
    if message.text == '⛔Остановить':
        date = await state.get_data()
        browser = date['p_browser']
        await browser.close()
    else:
        await message.answer('Такая команда у меня отсутствует...', reply_markup=stop)