from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menus = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='👤Аккаунт'
        )
    ],
    [
        KeyboardButton(
            text='📘Обратная связь'
        ),
        KeyboardButton(
            text='⚙Настройки'
        ),
        KeyboardButton(
            text='🏳️Помощь'
        )
    ],
    [
        KeyboardButton(
            text='🕹Запуск'
        )
    ]
], resize_keyboard=True)

inputs = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='♻Очистить'
        ),
        KeyboardButton(
            text='◀Назад'
        )
    ]
], resize_keyboard=True)

stop = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='⛔Остановить'
        )
    ]
], resize_keyboard=True)