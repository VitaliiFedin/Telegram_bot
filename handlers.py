from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from config import config
from items import answers_items, checklist_items, locations_items
from states import Form
from utils import advance_to_next_checklist_item, create_keyboard


async def send_welcome(message: types.Message, state: FSMContext):
    """Send a welcome message and initiate the checklist process.
    This function sends a greeting to the user and sets the initial state for the checklist
    process in the bot's conversation.

    Args:
        message (types.Message): The message object from the user.
        state (FSMContext): The current state context of the conversation.
    """
    await state.finish()
    await message.answer("Hello. \U0001F44B Let's get started.")
    await Form.location.set()

    await message.answer(
        "Choose a location:", reply_markup=create_keyboard(locations_items)
    )


async def process_location(message: types.Message, state: FSMContext):
    """Process the user's location response and advance to the checklist.

    This function stores the user's provided location and starts the checklist process by
    setting the appropriate state and prompting the first checklist question.

    Args:
        message (types.Message): The message object containing the user's location response.
        state (FSMContext): The current state context of the conversation.
    """
    async with state.proxy() as data:
        data["location"] = message.text
        data["checklist_index"] = 0  # Initialize checklist index
    await Form.checklist_item.set()

    await message.answer(
        f"{checklist_items[0]} (No/Comment)",
        reply_markup=create_keyboard(answers_items),
    )


async def invalid_checklist_response(message: types.Message):
    """Handle invalid responses in the checklist process.
    This function is triggered when the user provides an invalid response (not 'No' or 'Comment')
    during the checklist process. It prompts the user to provide a valid response.

    Args:
        message (types.Message): The message object containing the user's response.
    """
    await message.answer(
        "Please answer with 'No' or 'Comment'.",
        reply_markup=create_keyboard(answers_items),
    )


async def handle_checklist_item(message: types.Message, state: FSMContext):
    """Handle user responses for each checklist item.

    This function processes the user's response for the current checklist item, either storing
    the response or prompting for a comment, and then advances to the next item or phase as appropriate.

    Args:
        message (types.Message): The message object containing the user's response.
        state (FSMContext): The current state context of the conversation.
    """
    response = message.text.lower()
    async with state.proxy() as data:
        index = data["checklist_index"]
        if response == "comment":
            await Form.comment.set()
            await message.answer(
                f"Please leave your comment for '{checklist_items[index]}'.",
                reply_markup=types.ReplyKeyboardRemove(),
            )
        elif response == "no":
            # Store 'No' as response
            data[f"checklist_item_{index + 1}"] = "No"
            await advance_to_next_checklist_item(message, state, data)
        else:
            await message.answer(
                "Please answer with 'No' or 'Comment'.",
                reply_markup=create_keyboard(answers_items),
            )


async def process_comment(message: types.Message, state: FSMContext):
    """Process and store the user's comment for a checklist item.

    This function captures and stores the user's comment for a specific checklist item and
    then advances the conversation to the next phase, typically requesting a photo.

    Args:
        message (types.Message): The message object containing the user's comment.
        state (FSMContext): The current state context of the conversation.
    """
    comment = message.text
    async with state.proxy() as data:
        index = data["checklist_index"]
        data[f"checklist_item_{index + 1}"] = comment  # Store comment as response

    await Form.photo.set()  # Set the state to photo
    await message.answer("Please upload a photo:")


async def process_photo(message: types.Message, state: FSMContext):
    """Process and store the user's photo submission.

    This function captures and stores the photo submitted by the user, generating a link to the
    photo and displaying it, then advancing to the next checklist item or phase.

    Args:
        message (types.Message): The message object containing the user's photo.
        state (FSMContext): The current state context of the conversation.
    """
    if message.photo:
        bot = message.bot
        photo_id = message.photo[-1].file_id
        file_info = await bot.get_file(photo_id)
        file_path = file_info.file_path
        telegram_file_url = (
            f"https://api.telegram.org/file/bot"
            f"{config.bot_token.get_secret_value()}/{file_path}"
        )

        async with state.proxy() as data:
            data["photo"] = telegram_file_url
            photo_link = f"[Your Photo]({telegram_file_url})"
            await message.answer(
                f"Here is the link to {photo_link}", parse_mode="Markdown"
            )
            await advance_to_next_checklist_item(message, state, data)
    else:
        await message.answer("Please upload a photo.")


async def process_non_photo(message: types.Message):
    """Prompt the user to upload a photo.

    This function is invoked when the user fails to upload a photo, prompting them to do so.

    Args:
        message (types.Message): The message object from the user.
    """
    await message.answer("Please upload a photo.")


def setup_handlers(dp: Dispatcher):
    """Register handlers for different message types and states.

    This function sets up the various message handlers for the bot, linking specific functions
    to different commands, message types, and conversation states.


    Args:
        dp (Dispatcher): The Dispatcher object used for registering handlers.
    """
    dp.register_message_handler(send_welcome, commands=["start"])
    dp.register_message_handler(process_location, state=Form.location)
    dp.register_message_handler(
        invalid_checklist_response,
        lambda message: message.text.lower() not in ["no", "comment"],
        state=Form.checklist_item,
    )
    dp.register_message_handler(handle_checklist_item, state=Form.checklist_item)
    dp.register_message_handler(process_comment, state=Form.comment)
    dp.register_message_handler(
        process_photo, content_types=["photo"], state=Form.photo
    )
    dp.register_message_handler(
        process_non_photo, lambda message: not message.photo, state=Form.photo
    )
