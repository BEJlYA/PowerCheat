from aiogram.fsm.state import StatesGroup, State


class DataSteps(StatesGroup):
    START = State()  # Basic bot state
    ACCOUNT = State()  # Account states:
    LOGIN = State()
    PASSWORD = State()
    HELP = State()  # Helping states:
    FEEDBACK = State()
    ANSW_MENU = State()
    ANSW = State()
    SETTING = State()  # Settings states:
    FIGHT = State()
    ITEM = State()
    POK = State()
    GENDER = State()
    BOL = State()
    SHINE = State()
    LAUNCH = State()  # Playwright state
