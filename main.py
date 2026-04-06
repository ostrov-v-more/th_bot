import os
from dotenv import load_dotenv
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from constants import DISCLAIMERS, QUESTIONS
from finish_quiz import finish_quiz
from keyboard_cache import get_keyboard
from send_question import send_question

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")


class Quiz(StatesGroup):
    waiting_for_disclaimer = State()  # Новое состояние для чтения предупреждений
    answering = State()


dp = Dispatcher()


# Хендлер СТАРТА - теперь показывает первое предупреждение
@dp.message(Command("start"))
async def start_quiz(message: types.Message, state: FSMContext):
    # Сбрасываем данные и ставим индекс дисклеймерса на 0
    await state.update_data(
        disclaimer_index=0,
        current_question=0,
        total_score_1=0,
        total_score_2=0,
    )
    await state.set_state(Quiz.waiting_for_disclaimer)

    await message.answer(
        DISCLAIMERS[0],
        reply_markup=get_keyboard(["Продолжить ➡️"])
    )


# Хендлер перелистывания предупреждений
@dp.message(Quiz.waiting_for_disclaimer)
async def disclaimers(message: types.Message, state: FSMContext):
    data = await state.get_data()
    idx = data["disclaimer_index"]

    idx += 1

    if idx >= len(DISCLAIMERS):
        await state.set_state(Quiz.answering)
        await send_question(message, 0)
        return

    data["disclaimer_index"] = idx
    await state.set_data(data)

    btn = "Начать 🚀" if idx == len(DISCLAIMERS) - 1 else "Продолжить ➡️"

    await message.answer(
        DISCLAIMERS[idx],
        reply_markup=get_keyboard([btn])
    )


# Хендлер ответов на вопросы (без изменений в логике)
@dp.message(Quiz.answering)
async def handle_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    question_idx = data["current_question"]
    question = QUESTIONS[question_idx]

    if message.text not in question["answers"]:
        await message.answer("Используй кнопки 👇")
        return

    points = question["answers"][message.text]

    # обновляем счетчики
    if question["target"] == 1:
        data["total_score_1"] += points
    else:
        data["total_score_2"] += points

    question_idx += 1

    # если есть следующий вопрос
    if question_idx < len(QUESTIONS):
        data["current_question"] = question_idx
        await state.set_data(data)

        next_q = QUESTIONS[question_idx]
        await message.answer(
            f"*{question_idx + 1} из {len(QUESTIONS)}\.*: {next_q['text']}",
            reply_markup=get_keyboard(next_q["answers"].keys())
        )
        return

    # финал
    await finish_quiz(message, state, data)


async def main():
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2),
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
