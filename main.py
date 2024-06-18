import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage

from core.handlers import basics, commands, menu, account, settings, payments, helping
from core.utils.settings import setting
from core.utils.data_states import DataSteps


async def start():
    bot = Bot(token=setting.bots.token_bot, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.startup.register(basics.start_bot)
    dp.shutdown.register(basics.stop_bot)
    #  Registration handlers command
    dp.message.register(commands.start_msg, CommandStart())
    #  Registration handlers menu
    dp.message.register(menu.account, F.text == '👤Аккаунт')
    dp.message.register(menu.feedback, F.text == '📠Обратная связь')
    dp.message.register(menu.get_feedback, DataSteps.FEEDBACK)
    dp.message.register(menu.answer_menu, DataSteps.ANSW_M)
    dp.message.register(menu.answer, DataSteps.ANSW)
    dp.message.register(menu.help, F.text == '🏳️Помощь')
    dp.message.register(menu.check_payments, F.text == '🕹Запуск')
    dp.message.register(menu.stop_browser, DataSteps.START)
    #  Registration handlers menu account
    dp.message.register(account.login, F.text == '✏Логин')
    dp.message.register(account.get_login, DataSteps.LOGIN)
    dp.message.register(account.password, F.text == '🔐Пароль')
    dp.message.register(account.get_password, DataSteps.PASSWORD)
    dp.message.register(account.clear_ac, F.text == '♻Очистить Аккаунт')
    #  Registration handlers helping menu
    dp.message.register(helping.help_menu, DataSteps.HELP)
    #  Registration handlers menu setting
    dp.message.register(settings.setting, F.text == '⚙Настройки')
    dp.message.register(settings.fight, F.text == '⚔Бой')
    dp.message.register(settings.get_fight, DataSteps.FIGHT)
    dp.message.register(settings.drop, F.text == '🎲Дроп')
    dp.message.register(settings.get_item, DataSteps.ITEM)
    dp.message.register(settings.catch, F.text == '📥Ловля')
    dp.message.register(settings.get_pok, DataSteps.POK)
    dp.message.register(settings.get_gender, DataSteps.GENDER)
    dp.message.register(settings.get_bol, DataSteps.BOL)
    dp.message.register(settings.shines, F.text == '📋Шайни')
    dp.message.register(settings.get_shines, DataSteps.SHINE)
    dp.message.register(settings.clear_st, F.text == '♻Oчистить всё')
    #  Registration payment handlers
    dp.pre_checkout_query.register(payments.on_pre_checkout_query)
    dp.message.register(payments.successful_payments, F.successful_payment)
    #  Registration hadlers callback query
    dp.callback_query.register(payments.one_mounth_pay, F.data == 'one_mounth')
    dp.callback_query.register(payments.two_mounth_pay, F.data == 'two_mounth')
    dp.callback_query.register(payments.three_mounth_pay, F.data == 'three_mounth')
    dp.callback_query.register(payments.return_to_menu, F.data == 'return')
    dp.callback_query.register(payments.back_to_choose, F.data == 'back')
    #  Registration handlers other
    dp.message.register(basics.menu, F.text == '◀Вернуться')
    dp.message.register(basics.none_msg)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


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
