from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """Create a single-row keyboard for Telegram with specified items.

    Args:
        items (list[str]): A list of strings, each representing the label for a button on the keyboard.

    Returns:
        ReplyKeyboardMarkup: A Telegram bot reply keyboard markup with a single row of buttons.
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)
