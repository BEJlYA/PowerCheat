import aiohttp
import aiosqlite
from aiogram import Bot
import asyncio.exceptions
from aiogram.types import Message
from core.settings import settings
from aiogram.fsm.context import FSMContext
from core.utils.data_states import DataSteps
from core.handlers.basics import account, setting
from core.keyboards import reply_feedbacks, reply_settings, reply_menu, reply_accounts


async def login(message: Message, state: FSMContext):
    await message.answer('Укажите ваш логин:', reply_markup=reply_menu.inputs)
    await state.set_state(DataSteps.LOGIN)


async def get_login(message: Message, state: FSMContext):
    if message.text == '◀Назад':
        await state.set_state(None)
        await account(message)
    elif message.text == '♻Очистить':
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET login = 'Отсутствует' WHERE chat_id = ?""", (message.chat.id,))
            await db.commit()
        await state.set_state(None)
        await account(message)
    else:
        await message.answer('Логин принят для обработки!', reply_markup=reply_accounts.accou)
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET login = ? WHERE chat_id = ?""", (message.text, message.chat.id,))
            await db.commit()
        await state.set_state(None)


async def password(message: Message, state: FSMContext):
    await message.answer('Укажите ваш пароль:', reply_markup=reply_menu.inputs)
    await state.set_state(DataSteps.PASSWORD)


async def get_password(message: Message, state: FSMContext):
    if message.text == '◀Назад':
        await state.set_state(None)
        await account(message)
    elif message.text == '♻Очистить':
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET password = 'Отсутствует' WHERE chat_id = ?""", (message.chat.id,))
            await db.commit()
        await state.set_state(None)
        await account(message)
    else:
        await message.answer('Пароль принят для обработки!', reply_markup=reply_accounts.accou)
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET password = ? WHERE chat_id = ?""", (message.text, message.chat.id,))
            await db.commit()
        await state.set_state(None)


async def proxy(message: Message, state: FSMContext):
    await message.answer('Укажите HTTP/HTTPS прокси <i>(прим. 012.34.567.890:1111)</i>:', reply_markup=reply_menu.inputs)
    await state.set_state(DataSteps.PROXY)


async def get_proxy(message: Message, state: FSMContext):
    if message.text == '◀Назад':
        await state.set_state(None)
        await account(message)
    elif message.text == '♻Очистить':
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET proxy = 'Отсутствуют' WHERE chat_id = ?""", (message.chat.id,))
            await db.commit()
        await state.set_state(None)
        await account(message)
    else:
        try:
            await message.answer('Выполняется проверка ваших прокси. <i>(Максимальное время ожидания - 5 сек.)</i>')
            async with aiohttp.ClientSession() as session:
                async with session.get(url='https://www.httpbin.org/ip',
                                       proxy=f'http://{message.text}',
                                       timeout=5) as response:
                    ip = message.text.split(':')
                    if ip[0] in await response.text():
                        await message.answer('Прокси приняты!', reply_markup=reply_accounts.accou)
                        async with aiosqlite.connect('data/users.db') as db:
                            await db.execute("""UPDATE profiles SET proxy = ? WHERE chat_id = ?""",
                                             (message.text, message.chat.id,))
                            await db.commit()
                        await state.set_state(None)
        except aiohttp.ClientConnectionError:
            await message.answer('Укажите другие прокси, введенные не работают...', reply_markup=reply_menu.inputs)
        except asyncio.exceptions.TimeoutError:
            await message.answer('Укажите другие прокси, введенные не работают...', reply_markup=reply_menu.inputs)
        except aiohttp.ClientHttpProxyError:
            await message.answer('Проверьте правильность введенных прокси или укажите другие...')


async def feedback(message: Message, state: FSMContext):
    async with aiosqlite.connect('data/users.db') as db:
        cursor = await db.execute("""SELECT Count(*) FROM feedback""")
        val_fb = await cursor.fetchone()
        await db.commit()
    if message.chat.id == settings.bots.admin_id:
        await message.answer(f'Количество обращений к разработчику: <b>{val_fb[0]}</b>\n'
                             f'Что желаете делать?', reply_markup=reply_feedbacks.answ)
        await state.set_state(DataSteps.ANSW_M)
    else:
        await message.answer('Напишите ваше обращение к разработчику бота:', reply_markup=reply_feedbacks.febck)
        await state.set_state(DataSteps.FEEDBACK)


async def answer_menu(message: Message, state: FSMContext, bot=Bot(token=settings.bots.token_bot)):
    if message.text == '📡Ответить':
        async with aiosqlite.connect('data/users.db') as db:
            cursor = await db.execute("""SELECT * from feedback""")
            if await cursor.fetchone() is None:
                await db.commit()
                await state.set_state(None)
                await message.answer('Обращения отсутствуют!', reply_markup=reply_menu.menus)
            else:
                cursor = await db.execute("""SELECT message, user from feedback""")
                message_fb, user = await cursor.fetchone()
                await db.commit()
                await message.answer('Обращение от пользователя:', reply_markup=reply_feedbacks.ansfd)
                await bot.forward_message(settings.bots.admin_id, user, message_fb)
                await state.set_state(DataSteps.ANSW)
    else:
        await message.answer('Такая команда у меня отсутствует...', reply_markup=reply_feedbacks.answ)


async def answer(message: Message, state: FSMContext, bot=Bot(token=settings.bots.token_bot)):
    if message.text == '‼Удалить':
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""DELETE FROM feedback WHERE rowid = (SELECT rowid FROM feedback LIMIT 1);""")
            await db.commit()
        await message.answer('Обращение удалено из очереди!', reply_markup=reply_feedbacks.ansfd)
    else:
        async with aiosqlite.connect('data/users.db') as db:
            cursor = await db.execute("""SELECT message, user from feedback""")
            message_fb, user = await cursor.fetchone()
            await db.commit()
        await bot.send_message(user, message.text, reply_to_message_id=message_fb)
        await message.answer('Ответ отправлен пользователю!', reply_markup=reply_feedbacks.ansfd)
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""DELETE FROM feedback WHERE rowid = (SELECT rowid FROM feedback LIMIT 1);""")
            cursor = await db.execute("""SELECT * FROM feedback""")
            if await cursor.fetchone() is None:
                await db.commit()
                await state.set_state(None)
                await message.answer('Обращения от пользователей закончились!', reply_markup=reply_menu.menus)
            else:
                cursor = await db.execute("""SELECT message, user from feedback""")
                message_fb, user = await cursor.fetchone()
                await db.commit()
                await bot.forward_message(settings.bots.admin_id, user, message_fb)


async def get_feedback(message: Message, state: FSMContext):
    async with aiosqlite.connect('data/users.db') as db:
        await db.execute("""INSERT INTO feedback  (message, user) VALUES (?, ?)""",
                         (message.message_id, message.chat.id,))
        await db.commit()
    await message.answer('Ваше сообщение отправлено, ожидайте пожалуйста.', reply_markup=reply_menu.menus)
    await state.set_state(None)


async def fight(message: Message, state: FSMContext):
    await message.answer('Введите кол-во проводимых боёв:', reply_markup=reply_menu.inputs)
    await state.set_state(DataSteps.FIGHT)


async def get_fight(message: Message, state: FSMContext):
    if message.text == '◀Назад':
        await state.set_state(None)
        await setting(message)
    elif message.text == '♻Очистить':
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET fight = 'Отсутствует' WHERE chat_id = ?""", (message.chat.id,))
            await db.commit()
        await state.set_state(None)
        await setting(message)
    else:
        if message.text.isdigit():
            await message.answer('Параметр принят!', reply_markup=reply_settings.sett)
            async with aiosqlite.connect('data/users.db') as db:
                await db.execute("""UPDATE profiles SET fight = ? WHERE chat_id = ?""", (message.text, message.chat.id,))
                await db.commit()
            await state.set_state(None)
        else:
            await message.answer('Требуется ввести числовое значение!', reply_markup=reply_menu.inputs)


async def heal(message: Message):
    await message.answer('Функция отключена...', reply_markup=reply_settings.sett)
    # await message.answer('Включить авто-лечение?', reply_markup=onoff)
    # await state.set_state(DataSteps.HEAL)


async def get_heal(message: Message, state: FSMContext):
    if message.text == '✅Включить':
        await message.answer('Авто-лечение включено!', reply_markup=reply_settings.sett)
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET heal = ? WHERE chat_id = ?""", ('Включено', message.chat.id,))
            await db.commit()
        await state.set_state(None)
    elif message.text == '❌Отключить':
        await message.answer('Авто-лечение отключено!', reply_markup=reply_settings.sett)
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET heal = ? WHERE chat_id = ?""", ('Отключено', message.chat.id,))
            await db.commit()
        await state.set_state(None)


async def drop(message: Message, state: FSMContext):
    await message.answer('Введите "Предмет:Количество" <i>(через запятую для выбора нескольких предметов)</i>:',
                         reply_markup=reply_menu.inputs)
    await state.set_state(DataSteps.ITEM)


async def get_item(message: Message, state: FSMContext):
    if message.text == '◀Назад':
        await state.set_state(None)
        await setting(message)
    elif message.text == '♻Очистить':
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET items = 'Отсутствует' WHERE chat_id = ?""", (message.chat.id,))
            await db.commit()
        await state.set_state(None)
        await setting(message)
    else:
        await message.answer('Значение принято!', reply_markup=reply_settings.sett)
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET items = ? WHERE chat_id = ?""", (message.text, message.chat.id,))
            await db.commit()
        await state.set_state(None)


async def catch(message: Message, state: FSMContext):
    await message.answer('Введите "Имя покемона:Количество" <i>(через запятую для выбора нескольких покемонов)</i>:',
                         reply_markup=reply_menu.inputs)
    await state.set_state(DataSteps.POK)


async def get_pok(message: Message, state: FSMContext):
    if message.text == '◀Назад':
        await state.set_state(None)
        await setting(message)
    elif message.text == '♻Очистить':
        await state.set_state(None)
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute(
                """UPDATE profiles SET catch = 'Отсутствует', gender = 'Отсутствует', pokebol = 'Отсутствует' WHERE chat_id = ?""",
                (message.chat.id,))
            await db.commit()
        await setting(message)
    else:
        await message.answer('Покемон принят!\n'
                             'Выберите желаемый гендер:', reply_markup=reply_settings.genders)
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET catch = ? WHERE chat_id = ?""", (message.text, message.chat.id,))
            await db.commit()
        await state.set_state(DataSteps.GENDER)


async def get_gender(message: Message, state: FSMContext):
    if message.text == '◀Назад':
        await state.set_state(None)
        await setting(message)
    elif message.text == '♻Очистить':
        await state.set_state(None)
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute(
                """UPDATE profiles SET catch = 'Отсутствует', gender = 'Отсутствует', pokebol = 'Отсутствует' WHERE chat_id = ?""",
                (message.chat.id,))
            await db.commit()
        await setting(message)
    else:
        await message.answer('Гендер принят!\n'
                             'Выберите используемый бол:', reply_markup=reply_settings.pokebols)
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET gender = ? WHERE chat_id = ?""", (message.text, message.chat.id,))
            await db.commit()
        await state.set_state(DataSteps.BOL)


async def get_bol(message: Message, state: FSMContext):
    await message.answer('Покебол принят!', reply_markup=reply_settings.sett)
    async with aiosqlite.connect('data/users.db') as db:
        await db.execute("""UPDATE profiles SET pokebol = ? WHERE chat_id = ?""", (message.text, message.chat.id,))
        await db.commit()
    await state.set_state(None)


async def shines(message: Message, state: FSMContext):
    await message.answer('Ловить шайни-покемонов?', reply_markup=reply_settings.onoff)
    await state.set_state(DataSteps.SHINE)


async def get_shines(message: Message, state: FSMContext):
    if message.text == '✅Да':
        await message.answer('Ловля включена!', reply_markup=reply_settings.sett)
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET shine = ? WHERE chat_id = ?""", ('Включено', message.chat.id,))
            await db.commit()
        await state.set_state(None)
    elif message.text == '❌Нет':
        await message.answer('Ловля отключена!', reply_markup=reply_settings.sett)
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET shine = ? WHERE chat_id = ?""", ('Отключено', message.chat.id,))
            await db.commit()
        await state.set_state(None)
    else:
        await message.answer('Такая команда у меня отсутствует...', reply_markup=reply_settings.onoff)


async def stop_browser(message: Message, state: FSMContext):
    if message.text == '⛔Остановить':
        date = await state.get_data()
        browser = date['p_browser']
        await browser.close()
    else:
        await message.answer('Такая команда у меня отсутствует...', reply_markup=reply_menu.stop)
