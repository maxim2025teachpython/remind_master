from aiogram import types
from database import get_user_reminders, delete_reminder
from keyboards import main_menu
from aiogram.utils.keyboard import InlineKeyboardBuilder


def register_list_delete_handlers(dp):
    @dp.message(lambda m: m.text == "📋 Мои напоминания")
    async def list_reminders(message: types.Message):
        reminders = get_user_reminders(message.chat.id)

        if not reminders:
            await message.answer("У вас нет напоминаний.", reply_markup=main_menu())
            return

        text = "Ваши напоминания:\n\n"
        kb = InlineKeyboardBuilder()

        for idx, (rem_id, rem_text, run_date, repeat_type, repeat_value) in enumerate(reminders, start=1):
            dt = run_date.replace("T", " ")
            text += f"{idx}) {dt} — {rem_text} ({repeat_type})\n"
            kb.button(text=f"Удалить {idx}", callback_data=f"del_{rem_id}")

        kb.adjust(1)

        await message.answer(text, reply_markup=kb.as_markup())

    @dp.callback_query(lambda c: c.data.startswith("del_"))
    async def delete_reminder_handler(callback: types.CallbackQuery):
        rem_id = int(callback.data.split("_")[1])
        delete_reminder(rem_id)

        await callback.message.edit_text("Напоминание удалено.")
        await callback.message.answer("📋 Мои напоминания обновлены.", reply_markup=main_menu())
