from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

sett = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='⚔Бой'
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
            text='◀Назад'
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
