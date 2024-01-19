from aiogram.fsm.state import State, StatesGroup

class Task(StatesGroup):
    desc = State()