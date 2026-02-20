import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import load_all_reminders, update_reminder_time
from utils.time_calc import get_next_time
from aiogram import Bot

scheduler = AsyncIOScheduler()


async def send_reminder(bot: Bot, chat_id, text, reminder_id, repeat_type, repeat_value):
    await bot.send_message(chat_id, f"🔔 Напоминание: {text}")

    if repeat_type == "none":
        from database import delete_reminder
        delete_reminder(reminder_id)
        return

    now = datetime.now()
    new_time = get_next_time(now, repeat_type, repeat_value)

    update_reminder_time(reminder_id, new_time.isoformat())

    scheduler.add_job(
        send_reminder,
        trigger="date",
        run_date=new_time,
        args=[bot, chat_id, text, reminder_id, repeat_type, repeat_value]
    )


def restore_jobs(bot: Bot):
    rows = load_all_reminders()
    now = datetime.now()

    for reminder_id, chat_id, text, run_date, repeat_type, repeat_value in rows:

        # 1. Пустая дата
        if not run_date or run_date.strip() == "":
            print(f"[!] Пропускаю напоминание {reminder_id}: пустая дата")
            continue

        # 2. Попытка распарсить дату
        try:
            run_dt = datetime.fromisoformat(run_date)
        except Exception:
            print(f"[!] Пропускаю напоминание {reminder_id}: неверный формат даты ({run_date})")
            continue

        # 3. Дополнительная защита — если всё равно None
        if run_dt is None:
            print(f"[!] Пропускаю напоминание {reminder_id}: run_dt = None")
            continue

        # 4. Обработка пропущенных напоминаний
        if run_dt <= now:
            while run_dt <= now:
                asyncio.create_task(
                    bot.send_message(chat_id, f"🔔 (пропущено) {text}")
                )
                run_dt = get_next_time(run_dt, repeat_type, repeat_value)

            update_reminder_time(reminder_id, run_dt.isoformat())

        # 5. Планирование следующего напоминания
        scheduler.add_job(
            send_reminder,
            trigger="date",
            run_date=run_dt,
            args=[bot, chat_id, text, reminder_id, repeat_type, repeat_value]
        )
