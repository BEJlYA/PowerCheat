import aiosqlite
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.handlers.menu import account
from core.keyboards import reply_accounts, reply_menu
from core.utils.data_states import DataSteps


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


async def clear_ac(message: Message):
    async with aiosqlite.connect('data/users.db') as db:
        await db.execute(
            """UPDATE profiles SET login = 'Отсутствует', password = 'Отсутствует' WHERE chat_id = ?""",
            (message.chat.id,))
        await db.commit()
    await message.answer('Все параметры очищенны!', reply_markup=reply_accounts.accou)
