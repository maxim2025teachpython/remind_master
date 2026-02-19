
from datetime import timedelta


def get_next_time(now, repeat_type, repeat_value):
    if repeat_type == "daily":
        return now + timedelta(days=1)

    if repeat_type == "hourly":
        return now + timedelta(hours=1)

    if repeat_type == "weekly":
        return now + timedelta(days=7)

    if repeat_type == "every_n_days":
        return now + timedelta(days=repeat_value)

    return None
