from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def main_menu():
    kb = ReplyKeyboardBuilder()
    kb.button(text="📝 Создать напоминание")
    kb.button(text="📋 Мои напоминания")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

def back_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.button(text="⬅️ Назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

def quick_times_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.button(text="1 минута")
    kb.button(text="5 минут")
    kb.button(text="10 минут")
    kb.button(text="30 минут")
    kb.button(text="1 час")
    kb.button(text="⏰ Выбрать точное время")
    kb.adjust(2, 2, 2)
    return kb.as_markup(resize_keyboard=True)

quick_mapping = {
    "1 минута": 1,
    "5 минут": 5,
    "10 минут": 10,
    "30 минут": 30,
    "1 час": 60
}

def repeat_menu():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Не повторять")
    kb.button(text="Каждый день")
    kb.button(text="Каждый час")
    kb.button(text="Каждую неделю")
    kb.button(text="Каждые N дней")
    kb.button(text="⬅️ Назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

def hour_keyboard():
    kb = InlineKeyboardBuilder()
    for h in range(24):
        kb.button(text=f"{h:02d}", callback_data=f"hour_{h}")
    kb.adjust(6)
    return kb.as_markup()

def minute_keyboard(hour: int):
    kb = InlineKeyboardBuilder()
    for m in range(0, 60, 5):
        kb.button(text=f"{m:02d}", callback_data=f"minute_{hour}_{m}")
    kb.adjust(6)
    return kb.as_markup()

def weekday_keyboard():
    kb = InlineKeyboardBuilder()
    days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    for i, d in enumerate(days):
        kb.button(text=d, callback_data=f"weekday_{i}")
    kb.adjust(7)
    return kb.as_markup()
