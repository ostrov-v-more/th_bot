import asyncio

from aiogram import types

from calculate_result import calculate_result
from constants import RESULT


async def finish_quiz(message, state, data):
    s1 = data["total_score_1"]
    s2 = data["total_score_2"]

    result = calculate_result(s1, s2)
    messages = RESULT.get(result, ["Ошибка: результат не найден"])

    await message.answer(
        "📊 *Тест завершен\! Подсчитываем результаты\.\.\.*",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await asyncio.sleep(1)

    await message.answer(
        f"*РЕЗУЛЬТАТЫ:*\n"
        f"*Гиперактивность:* {s1}\n"
        f"*Внимание:* {s2}\n"
        f"*Итого:* {s1 + s2}"
    )

    for text in messages:
        await message.answer(text)
        await asyncio.sleep(2)

    await state.clear()
