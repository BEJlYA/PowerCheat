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

sett = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='⚔Бой'
        ),
        KeyboardButton(
            text='⛑Лечение'
        ),
        KeyboardButton(
            text='🎲Дроп'
        )
    ],
    [
        KeyboardButton(
            text='📥Ловля'
        ),
        KeyboardButton(
            text='📋Шайни'
        ),
        KeyboardButton(
            text='◀Вернуться'
        )
    ],
    [
        KeyboardButton(
            text='♻Oчистить всё'
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

onoff = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='✅Да'
        ),
        KeyboardButton(
            text='❌Нет'
        )
    ]
], resize_keyboard=True)

genders = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Мужской'
        ),
        KeyboardButton(
            text='Бесполый'
        ),
        KeyboardButton(
            text='Женский'
        )
    ],
    [
        KeyboardButton(
            text='♻Очистить'
        ),
        KeyboardButton(
            text='Любой'
        ),
        KeyboardButton(
            text='◀Вернуться'
        )
    ]
], resize_keyboard=True)

pokebols = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Покебол'
        ),
        KeyboardButton(
            text='Гритбол'
        ),
        KeyboardButton(
            text='Ультрабол'
        )
    ],
    [
        KeyboardButton(
            text='Дистанцбол'
        ),
        KeyboardButton(
            text='Генебол'
        ),
        KeyboardButton(
            text='Мастербол'
        )
    ],
    [
        KeyboardButton(
            text='Шайнибол'
        ),
        KeyboardButton(
            text='В.Шайнибол'
        ),
        KeyboardButton(
            text='Сафарибол'
        )
    ]
], resize_keyboard=True)
