from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

help = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='📠Обратная связь'
        )
    ],
    [
        KeyboardButton(
            text='📄Пользовательское соглашение'
        ),
        KeyboardButton(
            text='📖Гайд по использованию'
        )
    ],
    [
        KeyboardButton(
            text='◀Вернуться'
        )
    ]
], resize_keyboard=True)
