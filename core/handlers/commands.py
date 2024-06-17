import aiosqlite
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hide_link

from core.keyboards import reply_menu


async def start_msg(message: Message, state: FSMContext):
    if await state.get_state() is None:
        await message.answer('👋')
        await message.answer(
            f'Я помогу тебе с облегчением рутинных действий в браузерной игре про Покемонов "<b>PokePower</b>". {hide_link("https://t.me/+7J3a6UokLodhMWYy")}\n\n⬇<b>Новостной канал:</b>⬇',
            reply_markup=reply_menu.menus)
        await sqlbase(message)
    else:
        await message.answer('В данный момент выполнение данной команды невозможно!')


async def sqlbase(message: Message):
    async with aiosqlite.connect('data/users.db') as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS profiles(chat_id  INTEGER NOT NULL CONSTRAINT data_pk PRIMARY KEY,
                                            login    TEXT    DEFAULT 'Отсутствует', password TEXT    DEFAULT 'Отсутствует',
                                            fight    integer DEFAULT 'Отсутствует', items    TEXT    DEFAULT 'Отсутствует',
                                            catch    TEXT    DEFAULT 'Отсутствует', shine    TEXT    DEFAULT 'Отключено',
                                            gender   TEXT    DEFAULT 'Отсутствует', pokebol  TEXT    DEFAULT 'Отсутствует')""")
        await db.execute("""CREATE TABLE IF NOT EXISTS feedback(message INTEGER, chat_id INTEGER)""")
        await db.execute(
            """CREATE TABLE IF NOT EXISTS payments(chat_id INTEGER PRIMARY KEY, proxy_id INTEGER, time_end TEXT,
            proxy TEXT, user TEXT, pass TEXT, transaction_id TEXT)""")
        await db.commit()
        cursor = await db.execute("""SELECT chat_id FROM profiles WHERE chat_id = ?""", (message.chat.id,))
        if await cursor.fetchone() is None:
            await db.execute("""INSERT INTO profiles (chat_id) VALUES (?)""", (message.chat.id,))
        await db.commit()
