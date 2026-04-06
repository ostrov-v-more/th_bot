from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

KEYBOARDS = {}


def get_keyboard(options):
    key = tuple(options)
    if key not in KEYBOARDS:
        builder = ReplyKeyboardBuilder()
        for opt in options:
            builder.add(types.KeyboardButton(text=opt))
        KEYBOARDS[key] = builder.as_markup(resize_keyboard=True)
    return KEYBOARDS[key]
