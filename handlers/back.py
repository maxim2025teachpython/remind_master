
from aiogram import types
from aiogram.fsm.context import FSMContext
from keyboards import main_menu


def register_back_handlers(dp):
    @dp.message(lambda m: m.text == "⬅️ Назад")
    async def go_back(message: types.Message, state: FSMContext):
        await state.clear()
        await message.answer("Главное меню:", reply_markup=main_menu())
