import sqlite3
import logging
from aiogram.types import Message
from core.keyboards.reply_acc import accou
from core.keyboards.reply_sett import sett
from aiogram.fsm.context import FSMContext
from core.keyboards.reply_menu import menus, stop
from core.utils.data_states import DataSteps
from core.utils.pp_cheat import DoneCheat, main


async def sqlbase(message: Message):
    connection = sqlite3.connect('data/users.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT chat_id FROM profiles WHERE chat_id = ?""", (message.chat.id,))
    if cursor.fetchone() is None:
        cursor.execute("""INSERT INTO profiles (chat_id) VALUES (?)""", (message.chat.id,))
    connection.commit()


async def start_msg(message: Message):
    await message.answer('Привет, я помогу с облегчением рутинных действий в браузерной игре про Покемонов "PokePower". <b><a href="https://t.me/+7J3a6UokLodhMWYy">Канал</a></b> с различной информацией!', reply_markup=menus)
    await sqlbase(message)


async def help(message: Message):
    await message.answer('Ссылка на гайд по боту, скоро появится!')


async def clear_ac(message: Message):
    connection = sqlite3.connect('data/users.db')
    cursor = connection.cursor()
    cursor.execute("""UPDATE profiles SET login = 'Отсутствует', password = 'Отсутствует', proxy = 'Отсутствуют' WHERE chat_id = ?""",
                   (message.chat.id,))
    connection.commit()
    await message.answer('Все параметры очищенны!', reply_markup=accou)


async def clear_st(message: Message):
    connection = sqlite3.connect('data/users.db')
    cursor = connection.cursor()
    cursor.execute(
        """UPDATE profiles SET fight = 'Отсутствует', heal = 'Отключено', items = 'Отсутствует', catch = 'Отсутствует', gender = 'Отсутствует', pokebol = 'Отсутствует', shine = 'Отключено' WHERE chat_id = ?""",
        (message.chat.id,))
    connection.commit()
    await message.answer('Все параметры очищенны!', reply_markup=sett)


async def account(message: Message):
    connection = sqlite3.connect('data/users.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT login, password, proxy FROM profiles WHERE chat_id = ?""",
                   (message.chat.id,))
    login, password, proxy = cursor.fetchone()
    if not password == 'Отсутствует':
        hid_pass = password[3:][:-3].replace(password[3:][:-3],
                                             password[:3] + '*' * len(password[3:][:-3]) + password[3:][-3:])
    else:
        hid_pass = 'Отсутствуют'
    await message.answer(f'<u>👤Аккаунт:</u>\n\n'
                         f'✏Логин: <i><b>{login}</b></i>\n'
                         f'🔐Пароль: <i><b>{hid_pass}</b></i>\n'
                         f'🤖Прокси: <i><b>{proxy}</b></i>',
                         reply_markup=accou)


async def setting(message: Message):
    connection = sqlite3.connect('data/users.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT fight, heal, items, catch, gender, pokebol, shine FROM profiles WHERE chat_id = ?""",
                   (message.chat.id,))
    fight, heal, items, catch, gender, pokebol, shine = cursor.fetchone()
    await message.answer(f'<u>⚙Настройки:</u>\n\n'
                         f'⚔Бой: <i><b>{fight}</b></i>\n'
                         f'⛑Лечение: <i><b>{heal}</b></i>\n'
                         f'🎲Дроп: <i><b>{items}</b></i>\n'
                         f'📥Ловля: <i><b>{catch}</b></i>\n'
                         f'      🔻Гендер: <i><b>{gender}</b></i>\n'
                         f'      🔻Бол: <i><b>{pokebol}</b></i>\n'
                         f'📋Шайни: <i><b>{shine}</b></i>',
                         reply_markup=sett)


async def start_cheat(message: Message, state: FSMContext):
    connection = sqlite3.connect('data/users.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT login, password, proxy, fight, heal, items, catch, gender, pokebol, shine FROM profiles WHERE chat_id = ?""",
                   (message.chat.id,))
    login, password, proxy, fight, heal, item, item_val, catch, gender, pokebol, shine = cursor.fetchone()
    if proxy == 'Отсутствуют' or proxy is None:
        await message.answer(
            'Вернитесь и укажите <b>прокси</b>, без них ваш аккаунт <b>рискует быть заблокированным.</b>')
    else:
        try:
            await message.answer('Программа запущена с выбранными настройками, ожидайте результатов!', reply_markup=stop)
            await state.set_state(DataSteps.START)
            await main(login, password, proxy, fight, item, item_val, catch, gender, pokebol, shine, state)
        except DoneCheat as dc:
            await message.answer(f'{dc}', reply_markup=menus)
            await state.set_state(None)
        except Exception as er:
            logging.error(str(er))
            if len(str(er)) > 3500:
                await message.answer(f'Программа была остановлена по ошибке: \n ``` {er[:3500]} ```', reply_markup=menus, parse_mode='MarkdownV2')
            else:
                await message.answer(f'Программа была остановлена по ошибке: \n ``` {er} ```', reply_markup=menus, parse_mode='MarkdownV2')
            await state.set_state(None)


async def menu(message: Message):
    await message.answer('Вы вернулись в Меню.', reply_markup=menus)


async def none_msg(message: Message):
    await message.answer('Такая команда у меня отсутствует...', reply_markup=menus)
