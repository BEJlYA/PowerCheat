from aiogram.fsm.state import StatesGroup, State


class DataSteps(StatesGroup):
    LOGIN = State()
    PASSWORD = State()
    FEEDBACK = State()
    ANSW_M = State()
    ANSW = State()
    FIGHT = State()
    ITEM = State()
    POK = State()
    GENDER = State()
    BOL = State()
    SHINE = State()
    START = State()