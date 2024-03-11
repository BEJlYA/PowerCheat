from aiogram import Dispatcher, F
from core.handlers.datas import *
from core.handlers.basics import *
from aiogram.filters import CommandStart
from core.utils.data_states import DataSteps
from aiogram.fsm.storage.memory import MemoryStorage


async def start():
    logging.basicConfig(level=logging.INFO,
                        format='[%(levelname)s] [%(asctime)s] [%(name)s] '
                               '[%(filename)s]-[%(funcName)s]-[%(lineno)d]: %(message)s',
                        handlers=[
                            logging.FileHandler('logs/project.log'),
                            logging.StreamHandler()
                        ])
    storage = MemoryStorage()
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(start_msg, CommandStart())
    dp.message.register(account, F.text == '👤Аккаунт')
    dp.message.register(login, F.text == '✏Логин')
    dp.message.register(get_login, DataSteps.LOGIN)
    dp.message.register(password, F.text == '🔐Пароль')
    dp.message.register(get_password, DataSteps.PASSWORD)
    dp.message.register(proxy, F.text == '🤖Прокси')
    dp.message.register(get_proxy, DataSteps.PROXY)
    dp.message.register(clear_ac, F.text == '♻Очистить Аккаунт')
    dp.message.register(menu, F.text == '◀Вернуться')
    dp.message.register(feedback, F.text == '📘Обратная связь')
    dp.message.register(get_feedback, DataSteps.FEEDBACK)
    dp.message.register(answer_menu, DataSteps.ANSW_M)
    dp.message.register(answer, DataSteps.ANSW)
    dp.message.register(help, F.text == '🏳️Помощь')
    dp.message.register(start_cheat, F.text == '🕹Запуск')
    dp.message.register(stop_browser, DataSteps.START)
    dp.message.register(setting, F.text == '⚙Настройки')
    dp.message.register(fight, F.text == '⚔Бой')
    dp.message.register(get_fight, DataSteps.FIGHT)
    dp.message.register(heal, F.text == '⛑Лечение')
    dp.message.register(get_heal, DataSteps.HEAL)
    dp.message.register(drop, F.text == '🎲Дроп')
    dp.message.register(get_item, DataSteps.ITEM)
    dp.message.register(catch, F.text == '📥Ловля')
    dp.message.register(get_pok, DataSteps.POK)
    dp.message.register(get_gender, DataSteps.GENDER)
    dp.message.register(get_bol, DataSteps.BOL)
    dp.message.register(shines, F.text == '📋Шайни')
    dp.message.register(get_shines, DataSteps.SHINE)
    dp.message.register(clear_st, F.text == '♻Oчистить всё')
    dp.message.register(none_msg)
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
    asyncio.run(start())
