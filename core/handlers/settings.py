import aiosqlite
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.keyboards import reply_menu, reply_settings
from core.utils.data_states import DataSteps


async def setting(message: Message):
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
                await db.execute("""UPDATE profiles SET fight = ? WHERE chat_id = ?""",
                                 (message.text, message.chat.id,))
                await db.commit()
            await state.set_state(None)
        else:
            await message.answer('Требуется ввести числовое значение!', reply_markup=reply_menu.inputs)


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


async def clear_st(message: Message):
    async with aiosqlite.connect('data/users.db') as db:
        await db.execute(
            """UPDATE profiles SET fight = 'Отсутствует', items = 'Отсутствует', catch = 'Отсутствует', gender = 'Отсутствует', pokebol = 'Отсутствует', shine = 'Отключено' WHERE chat_id = ?""",
            (message.chat.id,))
        await db.commit()
    await message.answer('Все параметры очищенны!', reply_markup=reply_settings.sett)
