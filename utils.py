import openai
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from items import answers_items, checklist_items, flag_to_country
from states import Form


def create_keyboard(items: list[str]):
    """Create a Telegram keyboard with buttons for each item in a list.

    Args:
        items (list[str]): A list of strings where each string is the label for a keyboard button.

    Returns:
        ReplyKeyboardMarkup: A Telegram bot reply keyboard with buttons for each provided item.
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for item in items:
        keyboard.add(KeyboardButton(item))
    return keyboard


async def send_data_to_openai(data: dict):
    """Send the provided data to OpenAI for analysis.

    Args:
        data (dict): A dictionary containing various pieces of information to be sent to OpenAI.
                     Expected to have keys like 'location' and checklist responses.

    Returns:
        str: The analysis result from OpenAI or an error message.
    """
    # Prepare the data for OpenAI
    location_emoji = data.get("location", "Unknown location")
    location = flag_to_country.get(location_emoji)
    checklist_qa = "\n".join(
        [
            f"Q: {checklist_items[i]} A: {data.get(f'checklist_item_{i + 1}', 'No response')}"
            for i in range(len(checklist_items))
        ]
    )

    # Combine everything into one string for analysis
    full_text = f"Location: {location}\n\nChecklist Q&A:\n{checklist_qa}\n"

    # Sending the data to OpenAI
    try:
        stream = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Analyze the following comments from a checklist:",
                },
                {"role": "user", "content": full_text},
            ],
            stream=True,
        )
        analysis_result = ""
        for chunk in stream:
            if chunk.choices[0].delta and chunk.choices[0].delta.content:
                analysis_result += chunk.choices[0].delta.content
        return analysis_result
    except Exception as e:
        print("Error with OpenAI request:", e)
        return "Error in processing the request."


async def advance_to_next_checklist_item(
    message: types.Message, state: FSMContext, data: dict
):
    """Advance the user to the next item in the checklist.

    Args:
        message (Message): The message object from aiogram.
        state (FSMContext): The finite state machine context for tracking user state.
        data (dict): The user's data dictionary, including the current index in the checklist.
    """
    index = data["checklist_index"]
    if index < len(checklist_items) - 1:
        data["checklist_index"] += 1
        await Form.checklist_item.set()
        await message.answer(
            f"{checklist_items[data['checklist_index']]} (No/Comment)",
            reply_markup=create_keyboard(answers_items),
        )
    else:
        # Here we send the data to OpenAI when the checklist is complete
        analysis = await send_data_to_openai(data)
        await state.finish()
        await message.answer(
            "Checklist completed! Your report will be generated and analyzed."
        )
        await message.answer(f"OpenAI Analysis: {analysis}")
        await message.answer(
            "Click /start to begin again.", reply_markup=create_keyboard(["/start"])
        )
