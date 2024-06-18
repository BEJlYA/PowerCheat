from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from core.keyboards import reply_menu
from aiogram.utils.markdown import hide_link


async def help_menu(message: Message, state: FSMContext):
    if message.text == '📄Пользовательское соглашение':
        await state.set_state(None)
        await message.answer(f'Внимательно прочитайте данное соглашение:{hide_link("https://telegra.ph/Polzovatelskoe-soglashenie-dlya-telegram-bota-PowerCheat-06-18")}', reply_markup=reply_menu.menus)
    elif message.text == '📖Гайд по использованию':
        await state.set_state(None)
        await message.answer(f'Внимательно прочитайте данный гайд:{hide_link("https://telegra.ph/Gajd-po-ispolzovaniyu-telegramm-bota-PowerCheat-06-18")}', reply_markup=reply_menu.menus)
    elif message.text == '◀Вернуться':
        await message.answer('Вы вернулись в Меню.', reply_markup=reply_menu.menus)
        await state.set_state(None)

