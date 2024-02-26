from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

accou = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='✏Логин'
        ),
        KeyboardButton(
            text='🔐Пароль'
        )
    ],
    [
        KeyboardButton(
            text='🤖Прокси'
        ),
        KeyboardButton(
            text='◀Вернуться'
        )
    ],
    [
        KeyboardButton(
            text='♻Очистить Аккаунт'
        )
    ]
], resize_keyboard=True)
