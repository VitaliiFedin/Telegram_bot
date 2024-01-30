from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    """_summary_

    Args:
        StatesGroup (_type_): _description_
    """

    location = State()
    checklist_item = State()
    comment = State()
    photo = State()
