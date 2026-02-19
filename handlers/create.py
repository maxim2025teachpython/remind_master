from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime, timedelta

from states import ReminderState
from keyboards import (
    quick_times_keyboard,
    quick_mapping,
    hour_keyboard,
    minute_keyboard,
    repeat_menu,
)
from keyboards import back_keyboard


def register_create_handlers(dp):
    @dp.message(lambda m: m.text == "📝 Создать напоминание")
    async def create_reminder(message: types.Message, state: FSMContext):
        await message.answer(
            "Выберите быстрый интервал или точное время:",
            reply_markup=quick_times_keyboard()
        )

    @dp.message(lambda m: m.text in quick_mapping)
    async def quick_reminder(message: types.Message, state: FSMContext):
        minutes = quick_mapping[message.text]
        remind_time = datetime.now() + timedelta(minutes=minutes)

        await state.update_data(remind_time=remind_time)
        await message.answer("Как часто повторять?", reply_markup=repeat_menu())
        await state.set_state(ReminderState.waiting_for_repeat)

    @dp.message(lambda m: m.text == "⏰ Выбрать точное время")
    async def choose_exact_time(message: types.Message, state: FSMContext):
        await message.answer("Выберите час:", reply_markup=hour_keyboard())
        await state.set_state(ReminderState.waiting_for_time)

    @dp.callback_query(lambda c: c.data.startswith("hour_"))
    async def select_hour(callback: types.CallbackQuery, state: FSMContext):
        hour = int(callback.data.split("_")[1])
        await state.update_data(hour=hour)

        await callback.message.edit_text(
            f"Вы выбрали час: {hour:02d}\nТеперь выберите минуты:",
            reply_markup=minute_keyboard(hour)
        )

    @dp.callback_query(lambda c: c.data.startswith("minute_"))
    async def select_minute(callback: types.CallbackQuery, state: FSMContext):
        _, hour, minute = callback.data.split("_")
        hour = int(hour)
        minute = int(minute)

        now = datetime.now()
        remind_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

        if remind_time <= now:
            remind_time += timedelta(days=1)

        await state.update_data(remind_time=remind_time)

        await callback.message.edit_text("Как часто повторять?")
        await callback.message.answer("Выберите:", reply_markup=repeat_menu())

        await state.set_state(ReminderState.waiting_for_repeat)
