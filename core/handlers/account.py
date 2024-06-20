import aiosqlite
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.handlers.menu import account
from core.keyboards import reply_accounts, reply_menu
from core.utils.data_states import DataSteps


async def account_menu(message: Message, state: FSMContext):
    if message.text == '✏Логин':
        await login(message, state)
    elif message.text == '🔐Пароль':
        await password(message, state)
    elif message.text == '♻Очистить Аккаунт':
        await clear_ac(message)
    elif message.text == '◀Вернуться':
        await message.answer('Вы вернулись в Меню.', reply_markup=reply_menu.menus)
        await state.set_state(DataSteps.START)
    else:
        await message.answer('Такая команда у меня отсутствует...', reply_markup=reply_accounts.accou)


async def login(message: Message, state: FSMContext):
    await message.answer('Укажите ваш логин:', reply_markup=reply_menu.inputs)
    await state.set_state(DataSteps.LOGIN)


async def get_login(message: Message, state: FSMContext):
    if message.text == '◀Вернуться':
        await state.set_state(DataSteps.ACCOUNT)
        await account(message, state)
    elif message.text == '♻Очистить':
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET login = 'Отсутствует' WHERE chat_id = ?""", (message.chat.id,))
            await db.commit()
        await state.set_state(DataSteps.ACCOUNT)
        await account(message, state)
    else:
        await message.answer('Логин принят для обработки!', reply_markup=reply_accounts.accou)
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET login = ? WHERE chat_id = ?""", (message.text, message.chat.id,))
            await db.commit()
        await state.set_state(DataSteps.ACCOUNT)


async def password(message: Message, state: FSMContext):
    await message.answer('Укажите ваш пароль:', reply_markup=reply_menu.inputs)
    await state.set_state(DataSteps.PASSWORD)


async def get_password(message: Message, state: FSMContext):
    if message.text == '◀Вернуться':
        await state.set_state(DataSteps.ACCOUNT)
        await account(message, state)
    elif message.text == '♻Очистить':
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET password = 'Отсутствует' WHERE chat_id = ?""", (message.chat.id,))
            await db.commit()
        await state.set_state(DataSteps.ACCOUNT)
        await account(message, state)
    else:
        await message.answer('Пароль принят для обработки!', reply_markup=reply_accounts.accou)
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET password = ? WHERE chat_id = ?""", (message.text, message.chat.id,))
            await db.commit()
        await state.set_state(DataSteps.ACCOUNT)


async def clear_ac(message: Message):
    async with aiosqlite.connect('data/users.db') as db:
        await db.execute(
            """UPDATE profiles SET login = 'Отсутствует', password = 'Отсутствует' WHERE chat_id = ?""",
            (message.chat.id,))
        await db.commit()
    await message.answer('Все параметры очищенны!', reply_markup=reply_accounts.accou)
