from constants import QUESTIONS
from keyboard_cache import get_keyboard


async def send_question(message, index):
    q = QUESTIONS[index]
    await message.answer(
        f"*{index + 1} из {len(QUESTIONS)}\.*: {q['text']}",
        reply_markup=get_keyboard(q["answers"].keys())
    )
