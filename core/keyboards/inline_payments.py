from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

choose_term = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='1️⃣',
            callback_data='one_mounth'
        ),
        InlineKeyboardButton(
            text='2️⃣',
            callback_data='two_mounth'
        ),
        InlineKeyboardButton(
            text='3️⃣',
            callback_data='three_mounth'
        )
    ],
    [
        InlineKeyboardButton(
            text='Вернуться',
            callback_data='return'
        )
    ]
])

choose_payment = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Оплатить XTR',
            pay=True
        )
    ],
    [
        InlineKeyboardButton(
            text='Отменить оплату',
            callback_data='back'
        )
    ]
])