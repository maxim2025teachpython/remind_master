from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from states import ReminderState
from keyboards import weekday_keyboard, back_keyboard
from database import add_reminder, get_user_reminders
from scheduler import scheduler, send_reminder


def register_repeat_handlers(dp):
    @dp.message(StateFilter(ReminderState.waiting_for_repeat))
    async def choose_repeat(message: types.Message, state: FSMContext):
        txt = message.text

        if txt == "Не повторять":
            await state.update_data(repeat_type="none", repeat_value=None)
            await message.answer("Введите текст напоминания:", reply_markup=back_keyboard())
            await state.set_state(ReminderState.waiting_for_text)
            return

        if txt == "Каждый день":
            await state.update_data(repeat_type="daily", repeat_value=None)
            await message.answer("Введите текст напоминания:", reply_markup=back_keyboard())
            await state.set_state(ReminderState.waiting_for_text)
            return

        if txt == "Каждый час":
            await state.update_data(repeat_type="hourly", repeat_value=None)
            await message.answer("Введите текст напоминания:", reply_markup=back_keyboard())
            await state.set_state(ReminderState.waiting_for_text)
            return

        if txt == "Каждую неделю":
            await message.answer("Выберите день недели:", reply_markup=weekday_keyboard())
            await state.set_state(ReminderState.waiting_for_weekday)
            return

        if txt == "Каждые N дней":
            await message.answer("Введите число N:", reply_markup=back_keyboard())
            await state.set_state(ReminderState.waiting_for_every_n_days)
            return

    @dp.callback_query(StateFilter(ReminderState.waiting_for_weekday))
    async def choose_weekday(callback: types.CallbackQuery, state: FSMContext):
        weekday = int(callback.data.split("_")[1])
        await state.update_data(repeat_type="weekly", repeat_value=weekday)

        await callback.message.answer("Введите текст напоминания:", reply_markup=back_keyboard())
        await state.set_state(ReminderState.waiting_for_text)

    @dp.message(StateFilter(ReminderState.waiting_for_every_n_days))
    async def choose_every_n_days(message: types.Message, state: FSMContext):
        try:
            n = int(message.text)
        except:
            await message.answer("Введите только число:", reply_markup=back_keyboard())
            return

        await state.update_data(repeat_type="every_n_days", repeat_value=n)
        await message.answer("Введите текст напоминания:", reply_markup=back_keyboard())
        await state.set_state(ReminderState.waiting_for_text)

    @dp.message(StateFilter(ReminderState.waiting_for_text))
    async def get_text(message: types.Message, state: FSMContext):
        data = await state.get_data()

        remind_time = data["remind_time"]
        repeat_type = data["repeat_type"]
        repeat_value = data.get("repeat_value")
        text = message.text

        add_reminder(message.chat.id, text, remind_time.isoformat(), repeat_type, repeat_value)

        reminders = get_user_reminders(message.chat.id)
        reminder_id = reminders[-1][0]

        scheduler.add_job(
            send_reminder,
            trigger="date",
            run_date=remind_time,
            args=[message.bot, message.chat.id, text, reminder_id, repeat_type, repeat_value]
        )

        await message.answer(
            f"Напоминание создано!\n"
            f"⏰ Время: {remind_time.strftime('%H:%M')}\n"
            f"🔁 Повтор: {repeat_type}\n"
            f"📝 Текст: {text}"
        )

        await state.clear()
