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
            text='♻Очистить Аккаунт'
        ),
        KeyboardButton(
            text='◀Вернуться'
        )
    ]
], resize_keyboard=True)
