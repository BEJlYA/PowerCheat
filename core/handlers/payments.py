from datetime import datetime

import aiohttp
import aiosqlite
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, CallbackQuery

from core.keyboards import inline_payments
from core.utils.settings import setting


async def one_mounth_pay(call: CallbackQuery):
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer_invoice(title="💎Подписка 1 Месяц💎",
                                      description="Скидка: Не действительна",
                                      photo_url='https://i.getgems.io/md0QVCY3Sp7flUeVHAzPF4fTUmxIm6H0liM4U8FtiuU/rs:fill:512:512:1/g:ce/czM6Ly9nZXRnZW1zLXMzL3VzZXItbWVkaWEvMDYtMTEtMjAyMi82MzY2YTc3N2ViZjE1MDIxYWM3NjlkMWIvNjM2NzNlNTBlYmYxNTAyMWFjNzZhZDY3LmpwZw',
                                      photo_size=512,
                                      photo_width=512,
                                      photo_height=512,
                                      prices=[LabeledPrice(
                                          label="XTR",
                                          amount=369)],
                                      provider_token='',
                                      payload="30",
                                      currency="XTR",
                                      reply_markup=inline_payments.choose_payment)


async def two_mounth_pay(call: CallbackQuery):
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer_invoice(title="💎Подписка 2 Месяца💎",
                                      description="Скидка: 6%",
                                      photo_url='https://i.getgems.io/md0QVCY3Sp7flUeVHAzPF4fTUmxIm6H0liM4U8FtiuU/rs:fill:512:512:1/g:ce/czM6Ly9nZXRnZW1zLXMzL3VzZXItbWVkaWEvMDYtMTEtMjAyMi82MzY2YTc3N2ViZjE1MDIxYWM3NjlkMWIvNjM2NzNlNTBlYmYxNTAyMWFjNzZhZDY3LmpwZw',
                                      photo_size=512,
                                      photo_width=512,
                                      photo_height=512,
                                      prices=[LabeledPrice(
                                          label="XTR",
                                          amount=694)],
                                      provider_token='',
                                      payload="60",
                                      currency="XTR",
                                      reply_markup=inline_payments.choose_payment)


async def three_mounth_pay(call: CallbackQuery):
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer_invoice(title="💎Подписка 3 Месяца💎",
                                      description="Скидка: 10%",
                                      photo_url='https://i.getgems.io/md0QVCY3Sp7flUeVHAzPF4fTUmxIm6H0liM4U8FtiuU/rs:fill:512:512:1/g:ce/czM6Ly9nZXRnZW1zLXMzL3VzZXItbWVkaWEvMDYtMTEtMjAyMi82MzY2YTc3N2ViZjE1MDIxYWM3NjlkMWIvNjM2NzNlNTBlYmYxNTAyMWFjNzZhZDY3LmpwZw',
                                      photo_size=512,
                                      photo_width=512,
                                      photo_height=512,
                                      prices=[LabeledPrice(
                                          label="XTR",
                                          amount=996)],
                                      provider_token='',
                                      payload="90",
                                      currency="XTR",
                                      reply_markup=inline_payments.choose_payment)


async def on_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


async def successful_payments(message: Message):
    async with aiosqlite.connect('data/users.db') as db:
        cursor = await db.execute("""SELECT proxy_id FROM payments WHERE chat_id = ?""",
                                  (message.chat.id,))
        async with aiohttp.ClientSession() as session:
            if (await cursor.fetchone())[0] is None:
                async with session.get(
                        f'https://proxy6.net/api/{setting.bots.api_proxy}/buy?count=1&period={message.successful_payment.invoice_payload}&country=ru&version=4&type=http') as response:
                    cursor = await db.execute("""SELECT proxy_id FROM payments""")
                    proxy_ids = await cursor.fetchall()
                    response = eval(await response.text()).get('list')
                    for element in response.values():
                        if element['id'] not in str(proxy_ids).strip('(),'):
                            await db.execute(
                                """UPDATE payments SET proxy_id = ?, time_end = ?, proxy = ?, user = ?, pass = ?, transaction_id = ? WHERE chat_id = ?""",
                                (element['id'], element['unixtime_end'], element['host'] + ':' + element['port'],
                                 element['user'], element['pass'],
                                 message.successful_payment.telegram_payment_charge_id, message.chat.id))
                            await db.commit()
            else:
                cursor = await db.execute("""SELECT proxy_id FROM payments WHERE chat_id = ?""",
                                          (message.chat.id,))
                proxy_id = (await cursor.fetchone())[0]
                async with session.get(
                        f'https://proxy6.net/api/{setting.bots.api_proxy}/prolong?period={message.successful_payment.invoice_payload}&ids={proxy_id}') as response:
                    response = eval(await response.text())
                await db.execute("""UPDATE payments SET time_end = ?, transaction_id = ? WHERE chat_id = ?""",
                                 (response['list'][f'{proxy_id}']['unixtime_end'],
                                  message.successful_payment.telegram_payment_charge_id, message.chat.id))
                await db.commit()
        cursor = await db.execute("""SELECT time_end FROM payments WHERE chat_id = ?""",
                                  (message.chat.id,))
        time_end = str(await cursor.fetchone()).strip("'(,)'")
        await message.answer('🎉Оплата успешно произведена!🎉\n\n'
                             f'Ваша подписка закончится: <b>{datetime.fromtimestamp(int(time_end))}</b>')


async def back_to_choose(call: CallbackQuery):
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('❌<b>У вас не оплачена подписка на бота</b>❌\n\n'
                              'Выберите пожалуйста на сколько <b>месяцев</b> вы хотите приобрести подписку:',
                              reply_markup=inline_payments.choose_term)


async def return_to_menu(call: CallbackQuery):
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
