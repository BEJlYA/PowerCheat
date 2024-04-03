import logging
import aiosqlite
from aiogram.types import Message
from core.settings import settings
from browser.cheat import main, ExCheat
from aiogram.fsm.context import FSMContext
from core.utils.data_states import DataSteps
from core.keyboards import reply_settings, reply_accounts, reply_menu
from playwright._impl._errors import TargetClosedError


async def sqlbase(message: Message):
    async with aiosqlite.connect('data/users.db') as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS profiles(chat_id  integer not null constraint data_pk primary key,
                                            login    TEXT    default 'Отсутствует', password TEXT    default 'Отсутствует',
                                            proxy    TEXT    default 'Отсутствуют', fight    integer default 'Отсутствует',
                                            heal     TEXT    default 'Отключено', items    TEXT    default 'Отсутствует',
                                            catch    TEXT    default 'Отсутствует', shine    TEXT    default 'Отключено',
                                            gender   TEXT    default 'Отсутствует', pokebol  TEXT    default 'Отсутствует')""")
        await db.execute("""CREATE TABLE IF NOT EXISTS feedback(message INTEGER, user INTEGER);""")
        await db.commit()
        cursor = await db.execute("""SELECT chat_id FROM profiles WHERE chat_id = ?""", (message.chat.id,))
        if await cursor.fetchone() is None:
            await db.execute("""INSERT INTO profiles (chat_id) VALUES (?)""", (message.chat.id,))
        await db.commit()


async def start_msg(message: Message, state: FSMContext):
    if await state.get_state() is None:
        await message.answer(
            'Привет, я помогу с облегчением рутинных действий в браузерной игре про Покемонов "PokePower". <b><a href="https://t.me/+7J3a6UokLodhMWYy">Канал</a></b> с различной информацией!',
            reply_markup=reply_menu.menus)
        await sqlbase(message)
    else:
        await message.answer('В данный момент выполнение данной команды невозможно!')


async def help(message: Message):
    await message.answer('Ссылка на гайд по боту, скоро появится!')


async def clear_ac(message: Message):
    async with aiosqlite.connect('data/users.db') as db:
        await db.execute(
            """UPDATE profiles SET login = 'Отсутствует', password = 'Отсутствует', proxy = 'Отсутствуют' WHERE chat_id = ?""",
            (message.chat.id,))
        await db.commit()
    await message.answer('Все параметры очищенны!', reply_markup=reply_accounts.accou)


async def clear_st(message: Message):
    async with aiosqlite.connect('data/users.db') as db:
        await db.execute(
            """UPDATE profiles SET fight = 'Отсутствует', heal = 'Отключено', items = 'Отсутствует', catch = 'Отсутствует', gender = 'Отсутствует', pokebol = 'Отсутствует', shine = 'Отключено' WHERE chat_id = ?""",
            (message.chat.id,))
        await db.commit()
    await message.answer('Все параметры очищенны!', reply_markup=reply_settings.sett)


async def account(message: Message):
    async with aiosqlite.connect('data/users.db') as db:
        cursor = await db.execute("""SELECT login, password, proxy FROM profiles WHERE chat_id = ?""",
                                  (message.chat.id,))
        login, password, proxy = await cursor.fetchone()
        await db.commit()
    if not password == 'Отсутствует':
        hid_pass = password[3:][:-3].replace(password[3:][:-3],
                                             password[:3] + '*' * len(password[3:][:-3]) + password[3:][-3:])
    else:
        hid_pass = 'Отсутствует'
    await message.answer(f'<u>👤Аккаунт:</u>\n\n'
                         f'✏Логин: <i><b>{login}</b></i>\n'
                         f'🔐Пароль: <i><b>{hid_pass}</b></i>\n'
                         f'🤖Прокси: <i><b>{proxy}</b></i>',
                         reply_markup=reply_accounts.accou)


async def setting(message: Message):
    async with aiosqlite.connect('data/users.db') as db:
        cursor = await db.execute(
            """SELECT fight, heal, items, catch, gender, pokebol, shine FROM profiles WHERE chat_id = ?""",
            (message.chat.id,))
        fight, heal, items, catch, gender, pokebol, shine = await cursor.fetchone()
        await db.commit()
    await message.answer(f'<u>⚙Настройки:</u>\n\n'
                         f'⚔Бой: <i><b>{fight}</b></i>\n'
                         f'⛑Лечение: <i><b>{heal}</b></i>\n'
                         f'🎲Дроп: <i><b>{items}</b></i>\n'
                         f'📥Ловля: <i><b>{catch}</b></i>\n'
                         f'      🔻Гендер: <i><b>{gender}</b></i>\n'
                         f'      🔻Бол: <i><b>{pokebol}</b></i>\n'
                         f'📋Шайни: <i><b>{shine}</b></i>',
                         reply_markup=reply_settings.sett)


async def start_cheat(message: Message, state: FSMContext):
    if message.chat.id == settings.bots.admin_id or True:  # "False" to Technical work
        async with aiosqlite.connect('data/users.db') as db:
            cursor = await db.execute(
                """SELECT login, password, proxy, fight, heal, items, catch, gender, pokebol, shine FROM profiles WHERE chat_id = ?""",
                (message.chat.id,))
            login, password, proxy, fight, heal, items, catch, gender, pokebol, shine = await cursor.fetchone()
            await db.commit()
        if proxy == 'Отсутствуют' or proxy is None:
            await message.answer(
                'Вернитесь и укажите <b>прокси</b>, без них ваш аккаунт <b>рискует быть заблокированным.</b>')
        else:
            try:
                await message.answer('Бот запущен с выбранными настройками, ожидайте результатов!', reply_markup=reply_menu.stop)
                await state.set_state(DataSteps.START)
                await main(login, password, proxy, fight, items, catch, gender, pokebol, shine, state)
            except ExCheat as dc:
                await message.answer(f'{dc}', reply_markup=reply_menu.menus)
                await state.set_state(None)
            except TargetClosedError:
                await message.answer('Бот остановлен!', reply_markup=reply_menu.menus)
                await state.set_state(None)
            except Exception as er:
                logging.error(str(er))
                if len(str(er)) > 3500:
                    await message.answer(f'Бот был остановлена из за ошибки: \n ``` {er[:3500]} ```', reply_markup=reply_menu.menus,
                                         parse_mode='MarkdownV2')
                else:
                    await message.answer(f'Бот был остановлена из за ошибки: \n ``` {er} ```', reply_markup=reply_menu.menus,
                                         parse_mode='MarkdownV2')
                await state.set_state(None)
    else:
        await message.answer('В данный момент проводятся Технические Работы, ожидайте пожалуйста новостей!')


async def menu(message: Message, state: FSMContext):
    await message.answer('Вы вернулись в Меню.', reply_markup=reply_menu.menus)
    await state.set_state(None)


async def none_msg(message: Message):
    await message.answer('Такая команда у меня отсутствует...', reply_markup=reply_menu.menus)
