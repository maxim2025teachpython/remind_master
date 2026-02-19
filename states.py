from aiogram.fsm.state import State, StatesGroup

class ReminderState(StatesGroup):
    waiting_for_time = State()
    waiting_for_text = State()
    waiting_for_repeat = State()
    waiting_for_weekday = State()
    waiting_for_every_n_days = State()
