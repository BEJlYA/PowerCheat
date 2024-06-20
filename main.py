import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage

from core.handlers import commands, menu, account, settings, payments, helping
from core.utils.data_states import DataSteps
from core.utils.settings import setting


async def start():
    bot = Bot(token=setting.bots.token_bot, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    #  Registration handlers command
    dp.message.register(commands.start_msg, CommandStart())
    #  Registration handlers menu
    dp.message.register(menu.start_menu, DataSteps.START)
    dp.message.register(menu.stop_browser, DataSteps.LAUNCH)
    #  Registration handlers menu account
    dp.message.register(account.account_menu, DataSteps.ACCOUNT)
    dp.message.register(account.get_login, DataSteps.LOGIN)
    dp.message.register(account.get_password, DataSteps.PASSWORD)
    #  Registration handlers helping menu
    dp.message.register(helping.help_menu, DataSteps.HELP)
    dp.message.register(helping.get_feedback, DataSteps.FEEDBACK)
    dp.message.register(helping.answer_menu, DataSteps.ANSW_MENU)
    dp.message.register(helping.answer, DataSteps.ANSW)
    #  Registration handlers menu setting
    dp.message.register(settings.setting_menu, DataSteps.SETTING)
    dp.message.register(settings.get_fight, DataSteps.FIGHT)
    dp.message.register(settings.get_item, DataSteps.ITEM)
    dp.message.register(settings.get_pok, DataSteps.POK)
    dp.message.register(settings.get_gender, DataSteps.GENDER)
    dp.message.register(settings.get_bol, DataSteps.BOL)
    dp.message.register(settings.get_shines, DataSteps.SHINE)
    #  Registration payment handlers
    dp.pre_checkout_query.register(payments.on_pre_checkout_query)
    dp.message.register(payments.successful_payments, F.successful_payment)
    #  Registration handlers callback query
    dp.callback_query.register(payments.one_mounth_pay, F.data == 'one_mounth')
    dp.callback_query.register(payments.two_mounth_pay, F.data == 'two_mounth')
    dp.callback_query.register(payments.three_mounth_pay, F.data == 'three_mounth')
    dp.callback_query.register(payments.return_to_menu, F.data == 'return')
    dp.callback_query.register(payments.back_to_choose, F.data == 'back')
    # Registration handler if state is None
    dp.message.register(menu.none_state)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


async def start_bot(bot: Bot):
    await bot.send_message(setting.bots.admin_id, text='Бот запущен!')


async def stop_bot(bot: Bot):
    await bot.send_message(setting.bots.admin_id, text='Бот остановлен!')

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
