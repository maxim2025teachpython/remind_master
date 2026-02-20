from .create import register_create_handlers
from .repeat import register_repeat_handlers
from .back import register_back_handlers
from .list_delete import register_list_delete_handlers


def register_all_handlers(dp):
    register_create_handlers(dp)
    register_repeat_handlers(dp)
    register_back_handlers(dp)
    register_list_delete_handlers(dp)
