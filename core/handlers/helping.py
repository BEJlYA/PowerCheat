import aiosqlite
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hide_link

from core.keyboards import reply_feedbacks, reply_menu, reply_help
from core.utils.data_states import DataSteps
from core.utils.settings import setting


async def help_menu(message: Message, state: FSMContext):
    if message.text == '📄Пользовательское соглашение':
        await message.answer(f'Внимательно прочитайте данное соглашение:{hide_link("https://telegra.ph/Polzovatelskoe-soglashenie-dlya-telegram-bota-PowerCheat-06-18")}', reply_markup=reply_help.help)
    elif message.text == '📖Гайд по использованию':
        await message.answer(f'Внимательно прочитайте данный гайд:{hide_link("https://telegra.ph/Gajd-po-ispolzovaniyu-telegramm-bota-PowerCheat-06-18")}', reply_markup=reply_help.help)
    elif message.text == '📠Обратная связь':
        await feedback(message, state)
    elif message.text == '◀Вернуться':
        await message.answer('Вы вернулись в Меню.', reply_markup=reply_menu.menus)
        await state.set_state(DataSteps.START)
    else:
        await message.answer('Такая команда у меня отсутствует...', reply_markup=reply_feedbacks.answ)


async def feedback(message: Message, state: FSMContext):
    async with aiosqlite.connect('data/users.db') as db:
        cursor = await db.execute("""SELECT Count(*) FROM feedback""")
        val_fb = await cursor.fetchone()
        await db.commit()
    if message.chat.id == setting.bots.admin_id:
        await message.answer(f'Количество обращений к разработчику: <b>{val_fb[0]}</b>\n'
                             f'Что желаете делать?', reply_markup=reply_feedbacks.answ)
        await state.set_state(DataSteps.ANSW_MENU)
    else:
        await message.answer('Напишите ваше обращение к разработчику бота:', reply_markup=reply_feedbacks.febck)
        await state.set_state(DataSteps.FEEDBACK)


async def get_feedback(message: Message, state: FSMContext):
    if message.text == '◀Вернуться':
        await state.set_state(DataSteps.HELP)
        await message.answer('⬇Выберите нужный раздел:', reply_markup=reply_help.help)
    else:
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""INSERT INTO feedback  (message, chat_id) VALUES (?, ?)""",
                             (message.message_id, message.chat.id,))
            await db.commit()
        await message.answer('Ваше сообщение отправлено, ожидайте пожалуйста.', reply_markup=reply_help.help)
        await state.set_state(DataSteps.HELP)


async def answer_menu(message: Message, state: FSMContext):
    if message.text == '📡Ответить':
        async with aiosqlite.connect('data/users.db') as db:
            cursor = await db.execute("""SELECT * from feedback""")
            if await cursor.fetchone() is None:
                await db.commit()
                await state.set_state(DataSteps.HELP)
                await message.answer('Выберите нужный раздел:', reply_markup=reply_help.help)
            else:
                cursor = await db.execute("""SELECT message, chat_id from feedback""")
                message_fb, chat_id = await cursor.fetchone()
                await db.commit()
                await message.answer('Обращение от пользователя:', reply_markup=reply_feedbacks.ansfd)
                await message.bot.forward_message(setting.bots.admin_id, chat_id, message_fb)
                await state.set_state(DataSteps.ANSW)
    elif message.text == '◀Вернуться':
        await state.set_state(DataSteps.HELP)
        await message.answer('Выберите нужный раздел:', reply_markup=reply_help.help)
    else:
        await message.answer('Такая команда у меня отсутствует...', reply_markup=reply_feedbacks.answ)


async def answer(message: Message, state: FSMContext):
    if message.text == '‼Удалить':
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""DELETE FROM feedback WHERE rowid = (SELECT rowid FROM feedback LIMIT 1);""")
            await db.commit()
        await message.answer('Обращение удалено из очереди!', reply_markup=reply_feedbacks.ansfd)
    elif message.text == '◀Вернуться':
        await state.set_state(DataSteps.HELP)
        await message.answer('Выберите нужный раздел:', reply_markup=reply_help.help)
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
                await state.set_state(DataSteps.START)
                await message.answer('Обращения от пользователей закончились!', reply_markup=reply_menu.menus)
            else:
                await message.answer('Следущее обращение:', reply_markup=reply_feedbacks.ansfd)
                cursor = await db.execute("""SELECT message, chat_id from feedback""")
                message_fb, chat_id = await cursor.fetchone()
                await db.commit()
                await message.bot.forward_message(setting.bots.admin_id, chat_id, message_fb)
