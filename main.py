import asyncio
import logging
from core.handlers import datas
from core.handlers import basics
from core.settings import settings
from aiogram.enums import ParseMode
from aiogram import Dispatcher, F, Bot
from aiogram.filters import CommandStart
from core.utils.data_states import DataSteps
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties


async def start():
    storage = MemoryStorage()
    bot = Bot(token=settings.bots.token_bot, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(basics.start_msg, CommandStart())
    dp.message.register(basics.account, F.text == '👤Аккаунт')
    dp.message.register(datas.login, F.text == '✏Логин')
    dp.message.register(datas.get_login, DataSteps.LOGIN)
    dp.message.register(datas.password, F.text == '🔐Пароль')
    dp.message.register(datas.get_password, DataSteps.PASSWORD)
    dp.message.register(datas.proxy, F.text == '🤖Прокси')
    dp.message.register(datas.get_proxy, DataSteps.PROXY)
    dp.message.register(basics.clear_ac, F.text == '♻Очистить Аккаунт')
    dp.message.register(basics.menu, F.text == '◀Вернуться')
    dp.message.register(datas.feedback, F.text == '📘Обратная связь')
    dp.message.register(datas.get_feedback, DataSteps.FEEDBACK)
    dp.message.register(datas.answer_menu, DataSteps.ANSW_M)
    dp.message.register(datas.answer, DataSteps.ANSW)
    dp.message.register(basics.help, F.text == '🏳️Помощь')
    dp.message.register(basics.start_cheat, F.text == '🕹Запуск')
    dp.message.register(datas.stop_browser, DataSteps.START)
    dp.message.register(basics.setting, F.text == '⚙Настройки')
    dp.message.register(datas.fight, F.text == '⚔Бой')
    dp.message.register(datas.get_fight, DataSteps.FIGHT)
    dp.message.register(datas.heal, F.text == '⛑Лечение')
    dp.message.register(datas.get_heal, DataSteps.HEAL)
    dp.message.register(datas.drop, F.text == '🎲Дроп')
    dp.message.register(datas.get_item, DataSteps.ITEM)
    dp.message.register(datas.catch, F.text == '📥Ловля')
    dp.message.register(datas.get_pok, DataSteps.POK)
    dp.message.register(datas.get_gender, DataSteps.GENDER)
    dp.message.register(datas.get_bol, DataSteps.BOL)
    dp.message.register(datas.shines, F.text == '📋Шайни')
    dp.message.register(datas.get_shines, DataSteps.SHINE)
    dp.message.register(basics.clear_st, F.text == '♻Oчистить всё')
    dp.message.register(basics.none_msg)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.send_message(settings.bots.admin_id, text='Бот остановлен по ошибке!')
        await bot.session.close()


async def start_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот запущен!')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен!')


if __name__ in '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='[%(levelname)s] [%(asctime)s] '
                               '[%(filename)s]-[%(funcName)s]-[Line: %(lineno)d]: %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S',
                        handlers=[
                            logging.FileHandler('logs/info.log'),
                            logging.StreamHandler()
                        ])
    asyncio.run(start())
