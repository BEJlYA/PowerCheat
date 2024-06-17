import logging
from datetime import datetime

import aiohttp
import aiosqlite
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hide_link
from playwright._impl._errors import TargetClosedError

from browser.cheat import ExCheat, main
from core.keyboards import reply_accounts, reply_feedbacks, reply_menu, inline_payments
from core.utils.settings import setting
from core.utils.data_states import DataSteps


async def account(message: Message):
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


async def feedback(message: Message, state: FSMContext):
    async with aiosqlite.connect('data/users.db') as db:
        cursor = await db.execute("""SELECT Count(*) FROM feedback""")
        val_fb = await cursor.fetchone()
        await db.commit()
    if message.chat.id == setting.bots.admin_id:
        await message.answer(f'Количество обращений к разработчику: <b>{val_fb[0]}</b>\n'
                             f'Что желаете делать?', reply_markup=reply_feedbacks.answ)
        await state.set_state(DataSteps.ANSW_M)
    else:
        await message.answer('Напишите ваше обращение к разработчику бота:', reply_markup=reply_feedbacks.febck)
        await state.set_state(DataSteps.FEEDBACK)


async def get_feedback(message: Message, state: FSMContext):
    if message.text == '◀Вернуться':
        await message.answer('Вы вернулись в Меню.', reply_markup=reply_menu.menus)
        await state.set_state(None)
    else:
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""INSERT INTO feedback  (message, chat_id) VALUES (?, ?)""",
                             (message.message_id, message.chat.id,))
            await db.commit()
        await message.answer('Ваше сообщение отправлено, ожидайте пожалуйста.', reply_markup=reply_menu.menus)
        await state.set_state(None)


async def answer_menu(message: Message, state: FSMContext):
    if message.text == '📡Ответить':
        async with aiosqlite.connect('data/users.db') as db:
            cursor = await db.execute("""SELECT * from feedback""")
            if await cursor.fetchone() is None:
                await db.commit()
                await state.set_state(None)
                await message.answer('Обращения отсутствуют!', reply_markup=reply_menu.menus)
            else:
                cursor = await db.execute("""SELECT message, chat_id from feedback""")
                message_fb, chat_id = await cursor.fetchone()
                await db.commit()
                await message.answer('Обращение от пользователя:', reply_markup=reply_feedbacks.ansfd)
                await message.bot.forward_message(setting.bots.admin_id, chat_id, message_fb)
                await state.set_state(DataSteps.ANSW)
    elif message.text == '◀Вернуться':
        await message.answer('Вы вернулись в Меню.', reply_markup=reply_menu.menus)
        await state.set_state(None)
    else:
        await message.answer('Такая команда у меня отсутствует...', reply_markup=reply_feedbacks.answ)


async def answer(message: Message, state: FSMContext):
    if message.text == '‼Удалить':
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""DELETE FROM feedback WHERE rowid = (SELECT rowid FROM feedback LIMIT 1);""")
            await db.commit()
        await message.answer('Обращение удалено из очереди!', reply_markup=reply_feedbacks.ansfd)
    elif message.text == '◀Вернуться':
        await message.answer('Вы вернулись в Меню.', reply_markup=reply_menu.menus)
        await state.set_state(None)
    else:
        async with aiosqlite.connect('data/users.db') as db:
            cursor = await db.execute("""SELECT message, chat_id from feedback""")
            message_fb, chat_id = await cursor.fetchone()
            await db.commit()
        await message.bot.send_message(chat_id, message.text, reply_to_message_id=message_fb)
        await message.answer('Ответ отправлен пользователю!', reply_markup=reply_feedbacks.ansfd)
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""DELETE FROM feedback WHERE rowid = (SELECT rowid FROM feedback LIMIT 1);""")
            cursor = await db.execute("""SELECT * FROM feedback""")
            if await cursor.fetchone() is None:
                await db.commit()
                await state.set_state(None)
                await message.answer('Обращения от пользователей закончились!', reply_markup=reply_menu.menus)
            else:
                await message.answer('Следущее обращение:', reply_markup=reply_feedbacks.ansfd)
                cursor = await db.execute("""SELECT message, chat_id from feedback""")
                message_fb, chat_id = await cursor.fetchone()
                await db.commit()
                await message.bot.forward_message(setting.bots.admin_id, chat_id, message_fb)


async def help(message: Message):
    await message.answer('Ссылка на гайд по боту, скоро появится!')


async def check_payments(message: Message, state: FSMContext):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://proxy6.net/api/{setting.bots.api_proxy}') as response:
            response = eval(await response.text())
    if 99 <= int(float(response['balance'])):
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
    else:
        await message.answer('😭Извините, в данный момент это <b>невозможно</b>!\n\nПопробуйте немного позже')
        await message.bot.send_message(setting.bots.admin_id, f'💎На балансе {hide_link("https://proxy6.net/user/balance")}закончились деньги!💎\n\nПожалуйста пополните баланс!')


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
                await state.set_state(DataSteps.START)
                await main(login, password, proxy, user, pass_proxy, fight, items, catch, gender, pokebol, shine, state)
            except ExCheat as dc:
                await message.answer(f'{dc}', reply_markup=reply_menu.menus)
                await state.set_state(None)
            except TargetClosedError:
                await message.answer('Бот остановлен!', reply_markup=reply_menu.menus)
                await state.set_state(None)
            except Exception as er:
                logging.error(str(er))
                if len(str(er)) > 3500:
                    await message.answer(f'Бот был остановлена из за ошибки: \n ``` {er[:3500]} ```',
                                         reply_markup=reply_menu.menus,
                                         parse_mode='MarkdownV2')
                else:
                    await message.answer(f'Бот был остановлена из за ошибки: \n ``` {er} ```',
                                         reply_markup=reply_menu.menus,
                                         parse_mode='MarkdownV2')
                await state.set_state(None)
    else:
        await message.answer('В данный момент проводятся Технические Работы, ожидайте пожалуйста новостей!')


async def stop_browser(message: Message, state: FSMContext):
    if message.text == '⛔Остановить':
        date = await state.get_data()
        browser = date['p_browser']
        await browser.close()
    else:
        await message.answer('Такая команда у меня отсутствует...', reply_markup=reply_menu.stop)
