from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

febck = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='◀Вернуться'
        ),
    ]
], resize_keyboard=True)

answ = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='📡Ответить'
        ),
        KeyboardButton(
            text='◀Вернуться'
        ),
    ]
], resize_keyboard=True)

ansfd = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='‼Удалить'
        ),
        KeyboardButton(
          text='◀Вернуться'
        ),
    ]
], resize_keyboard=True)
