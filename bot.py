import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from database import init_db
from scheduler import scheduler, restore_jobs
from handlers import register_all_handlers


async def main():
    bot = Bot(TOKEN)
    dp = Dispatcher()

    # Инициализация базы
    init_db()

    # Восстановление задач APScheduler
    restore_jobs(bot)
    scheduler.start()

    # Регистрация всех хендлеров
    register_all_handlers(dp)

    print("Бот запущен и готов работать.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
