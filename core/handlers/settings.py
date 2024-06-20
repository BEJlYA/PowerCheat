import aiosqlite
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.handlers import menu
from core.keyboards import reply_menu, reply_settings
from core.utils.data_states import DataSteps


async def setting_menu(message: Message, state: FSMContext):
    if message.text == '⚔Бой':
        await fight(message, state)
    elif message.text == '🎲Дроп':
        await drop(message, state)
    elif message.text == '📥Ловля':
        await catch(message, state)
    elif message.text == '📋Шайни':
        await shines(message, state)
    elif message.text == '♻Oчистить всё':
        await clear_st(message)
    elif message.text == '◀Вернуться':
        await message.answer('Вы вернулись в Меню.', reply_markup=reply_menu.menus)
        await state.set_state(DataSteps.START)
    else:
        await message.answer('Такая команда у меня отсутствует...', reply_markup=reply_settings.sett)


async def fight(message: Message, state: FSMContext):
    await message.answer('Введите кол-во проводимых боёв (в диапазоне от 1 до 1500):', reply_markup=reply_menu.inputs)
    await state.set_state(DataSteps.FIGHT)


async def get_fight(message: Message, state: FSMContext):
    if message.text == '◀Вернуться':
        await state.set_state(DataSteps.SETTING)
        await menu.settings(message, state)
    elif message.text == '♻Очистить':
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET fight = '1500' WHERE chat_id = ?""", (message.chat.id,))
            await db.commit()
        await state.set_state(DataSteps.SETTING)
        await menu.settings(message, state)
    else:
        if message.text.isdigit():
            if 1500 >= int(message.text) >= 1:
                await message.answer('Параметр принят!', reply_markup=reply_settings.sett)
                async with aiosqlite.connect('data/users.db') as db:
                    await db.execute("""UPDATE profiles SET fight = ? WHERE chat_id = ?""",
                                     (message.text, message.chat.id,))
                    await db.commit()
                await state.set_state(DataSteps.SETTING)
            else:
                await message.answer('Вы ввели число вне допустимого диапазона!\n\nПопробуйте заново:')
        else:
            await message.answer('Требуется ввести числовое значение!\n\nПопробуйте заново:', reply_markup=reply_menu.inputs)


async def drop(message: Message, state: FSMContext):
    await message.answer('Введите "Предмет:Количество" <i>(через запятую для выбора нескольких предметов)</i>:',
                         reply_markup=reply_menu.inputs)
    await state.set_state(DataSteps.ITEM)


async def get_item(message: Message, state: FSMContext):
    if message.text == '◀Вернуться':
        await state.set_state(DataSteps.SETTING)
        await menu.settings(message, state)
    elif message.text == '♻Очистить':
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET items = 'Отсутствует' WHERE chat_id = ?""", (message.chat.id,))
            await db.commit()
        await state.set_state(DataSteps.SETTING)
        await menu.settings(message, state)
    else:
        await message.answer('Значение принято!', reply_markup=reply_settings.sett)
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET items = ? WHERE chat_id = ?""", (message.text, message.chat.id,))
            await db.commit()
        await state.set_state(DataSteps.SETTING)


async def catch(message: Message, state: FSMContext):
    await message.answer('Введите "Имя покемона:Количество" <i>(через запятую для выбора нескольких покемонов)</i>:',
                         reply_markup=reply_menu.inputs)
    await state.set_state(DataSteps.POK)


async def get_pok(message: Message, state: FSMContext):
    if message.text == '◀Вернуться':
        await state.set_state(DataSteps.SETTING)
        await menu.settings(message, state)
    elif message.text == '♻Очистить':
        await state.set_state(DataSteps.SETTING)
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute(
                """UPDATE profiles SET catch = 'Отсутствует', gender = 'Отсутствует', pokebol = 'Отсутствует' WHERE chat_id = ?""",
                (message.chat.id,))
            await db.commit()
        await menu.settings(message, state)
    else:
        await message.answer('Покемон принят!\n\n'
                             'Выберите желаемый гендер:', reply_markup=reply_settings.genders)
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET catch = ? WHERE chat_id = ?""", (message.text, message.chat.id,))
            await db.commit()
        await state.set_state(DataSteps.GENDER)


async def get_gender(message: Message, state: FSMContext):
    if message.text == '◀Вернуться':
        await state.set_state(DataSteps.SETTING)
        await menu.settings(message, state)
    elif message.text == '♻Очистить':
        await state.set_state(DataSteps.SETTING)
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute(
                """UPDATE profiles SET catch = 'Отсутствует', gender = 'Отсутствует', pokebol = 'Отсутствует' WHERE chat_id = ?""",
                (message.chat.id,))
            await db.commit()
        await menu.settings(message, state)
    else:
        await message.answer('Гендер принят!\n\n'
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
    await state.set_state(DataSteps.SETTING)


async def shines(message: Message, state: FSMContext):
    await message.answer('Ловить шайни-покемонов?', reply_markup=reply_settings.onoff)
    await state.set_state(DataSteps.SHINE)


async def get_shines(message: Message, state: FSMContext):
    if message.text == '✅Да':
        await message.answer('Ловля включена!', reply_markup=reply_settings.sett)
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET shine = ? WHERE chat_id = ?""", ('Включено', message.chat.id,))
            await db.commit()
        await state.set_state(DataSteps.SETTING)
    elif message.text == '❌Нет':
        await message.answer('Ловля отключена!', reply_markup=reply_settings.sett)
        async with aiosqlite.connect('data/users.db') as db:
            await db.execute("""UPDATE profiles SET shine = ? WHERE chat_id = ?""", ('Отключено', message.chat.id,))
            await db.commit()
        await state.set_state(DataSteps.SETTING)
    else:
        await message.answer('Такая команда у меня отсутствует...', reply_markup=reply_settings.onoff)


async def clear_st(message: Message):
    async with aiosqlite.connect('data/users.db') as db:
        await db.execute(
            """UPDATE profiles SET fight = '1500', items = 'Отсутствует', catch = 'Отсутствует', gender = 'Отсутствует', pokebol = 'Отсутствует', shine = 'Отключено' WHERE chat_id = ?""",
            (message.chat.id,))
        await db.commit()
    await message.answer('Все параметры очищенны!', reply_markup=reply_settings.sett)
