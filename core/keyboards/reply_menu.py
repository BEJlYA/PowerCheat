from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo

menus = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='🏳️Помощь'
        ),
    ],
    [
        KeyboardButton(
            text='👤Аккаунт'
        ),
        KeyboardButton(
            text='⚙Настройки'
        ),
        KeyboardButton(
            text='🎮Игра',
            web_app=WebAppInfo(
                url='https://pokepower.ru'
            )
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
            text='◀Вернуться'
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