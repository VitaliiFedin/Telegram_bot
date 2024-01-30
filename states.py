from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    """Represents the states used in the Telegram bot conversation."""

    location = State()
    checklist_item = State()
    comment = State()
    photo = State()
