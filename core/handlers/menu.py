import logging
from datetime import datetime

import aiosqlite
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from playwright._impl._errors import TargetClosedError

from browser.cheat import ExCheat, main
from core.keyboards import reply_menu, reply_help, reply_accounts, reply_settings, inline_payments
from core.utils.data_states import DataSteps
from core.utils.settings import setting


async def start_menu(message: Message, state: FSMContext):
    if message.text == '🏳️Помощь':
        await help(message, state)
    elif message.text == '👤Аккаунт':
        await account(message, state)
    elif message.text == '⚙Настройки':
        await settings(message, state)
    elif message.text == '🕹Запуск':
        await check_payments(message, state)
    else:
        await message.answer('Такая команда у меня отсутствует...', reply_markup=reply_menu.menus)


async def help(message: Message, state: FSMContext):
    await state.set_state(DataSteps.HELP)
    await message.answer('Выберите нужный раздел:', reply_markup=reply_help.help)


async def account(message: Message, state: FSMContext):
    async with aiosqlite.connect('data/users.db') as db:
        cursor = await db.execute("""SELECT login, password FROM profiles WHERE chat_id = ?""",
                                  (message.chat.id,))
        login, password = await cursor.fetchone()
        await db.commit()
    if not password == 'Отсутствует':
        hid_pass = password[3:][:-3].replace(password[3:][:-3],
                                             password[:3] + '*' * len(password[3:][:-3]) + password[3:][-3:])
    else:
        hid_pass = 'Отсутствует'
    await message.answer(f'<u>👤Аккаунт:</u>\n\n'
                         f'✏Логин: <i><b>{login}</b></i>\n'
                         f'🔐Пароль: <i><b>{hid_pass}</b></i>\n',
                         reply_markup=reply_accounts.accou)
    await state.set_state(DataSteps.ACCOUNT)


async def settings(message: Message, state: FSMContext):
    async with aiosqlite.connect('data/users.db') as db:
        cursor = await db.execute(
            """SELECT fight, items, catch, gender, pokebol, shine FROM profiles WHERE chat_id = ?""",
            (message.chat.id,))
        fight, items, catch, gender, pokebol, shine = await cursor.fetchone()
        await db.commit()
    await message.answer(f'<u>⚙Настройки:</u>\n\n'
                         f'⚔Бой: <i><b>{fight}</b></i>\n'
                         f'🎲Дроп: <i><b>{items}</b></i>\n'
                         f'📥Ловля: <i><b>{catch}</b></i>\n'
                         f'      🔻Гендер: <i><b>{gender}</b></i>\n'
                         f'      🔻Бол: <i><b>{pokebol}</b></i>\n'
                         f'📋Шайни: <i><b>{shine}</b></i>',
                         reply_markup=reply_settings.sett)
    await state.set_state(DataSteps.SETTING)


async def check_payments(message: Message, state: FSMContext):
    async with aiosqlite.connect('data/users.db') as db:
        cursor = await db.execute("""SELECT chat_id FROM payments WHERE chat_id = ?""", (message.chat.id,))
        if await cursor.fetchone() is None:
            await db.execute("""INSERT INTO payments (chat_id) VALUES (?)""", (message.chat.id,))
        cursor = await db.execute(
            """SELECT time_end FROM payments WHERE chat_id = ?""",
            (message.chat.id,))
        time_end = (await cursor.fetchone())[0]
        await db.commit()
    if time_end is None or int(datetime.now().timestamp()) >= int(time_end):
        await message.answer('❌<b>У вас не оплачена подписка на бота</b>❌\n\n'
                             'Выберите пожалуйста на сколько <b>месяцев</b> вы хотите приобрести подписку:',
                             reply_markup=inline_payments.choose_term)
    else:
        await start_pw_bot(message, state)


async def start_pw_bot(message: Message, state: FSMContext):
    if message.chat.id == setting.bots.admin_id or True:  # "False" for to Technicals works
        async with aiosqlite.connect('data/users.db') as db:
            cursor = await db.execute(
                """SELECT login, password, fight, items, catch, gender, pokebol, shine FROM profiles WHERE chat_id = ?""",
                (message.chat.id,))
            login, password, fight, items, catch, gender, pokebol, shine = await cursor.fetchone()
            cursor = await db.execute(
                """SELECT proxy, user, pass FROM payments WHERE chat_id = ?""",
                (message.chat.id,))
            proxy, user, pass_proxy = await cursor.fetchone()
            await db.commit()
            try:
                await message.answer('Бот запущен с выбранными настройками, ожидайте результатов!',
                                     reply_markup=reply_menu.stop)
                await state.set_state(DataSteps.LAUNCH)
                await main(login, password, proxy, user, pass_proxy, fight, items, catch, gender, pokebol, shine, state)
            except ExCheat as dc:
                await message.answer(f'{dc}', reply_markup=reply_menu.menus)
                await state.set_state(DataSteps.START)
            except TargetClosedError:
                await message.answer('Бот остановлен!', reply_markup=reply_menu.menus)
                await state.set_state(DataSteps.START)
            except Exception as er:
                if len(str(er)) > 3500:
                    logging.error(str(er))
                    await message.answer(f'Бот был остановлена из за ошибки: \n ``` {er[:3500]} ```',
                                         reply_markup=reply_menu.menus,
                                         parse_mode='MarkdownV2')
                elif 'net::ERR_ABORTED; maybe frame was detached?' in str(er):
                    await message.answer('Бот остановлен!', reply_markup=reply_menu.menus)
                    await state.set_state(DataSteps.START)
                else:
                    logging.error(str(er))
                    await message.answer(f'Бот был остановлена из за ошибки: \n ``` {er} ```',
                                         reply_markup=reply_menu.menus,
                                         parse_mode='MarkdownV2')
                await state.set_state(DataSteps.START)
    else:
        await message.answer('В данный момент проводятся Технические Работы, ожидайте пожалуйста новостей!')


async def stop_browser(message: Message, state: FSMContext):
    if message.text == '⛔Остановить':
        date = await state.get_data()
        if not date.get('p_browser') is None:
            browser = date['p_browser']
            await browser.close()
    else:
        await message.answer('Такая команда у меня отсутствует...', reply_markup=reply_menu.stop)


async def none_state(message: Message, state: FSMContext):
    await message.answer('Извините, бот только что проснулся после Технических работ! 😉\n\nПожалуйста повторите заново', reply_markup=reply_menu.menus)
    await state.set_state(DataSteps.START)
