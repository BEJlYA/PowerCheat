from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.keyboards import reply_menu
from core.utils.settings import setting


async def start_bot(bot: Bot):
    await bot.send_message(setting.bots.admin_id, text='Бот запущен!')


async def stop_bot(bot: Bot):
    await bot.send_message(setting.bots.admin_id, text='Бот остановлен!')


async def menu(message: Message, state: FSMContext):
    await message.answer('Вы вернулись в Меню.', reply_markup=reply_menu.menus)
    await state.set_state(None)


async def none_msg(message: Message):
    await message.answer('Такая команда у меня отсутствует...', reply_markup=reply_menu.menus)
