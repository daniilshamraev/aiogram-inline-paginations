import asyncio
import random
from pprint import pprint

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram_inline_paginations.paginator import Paginator

token = '5242892984:AAEbT_e5IEICUvMdfO6Mzf911oDd8HSrvVk'

storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(storage=storage)


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer('Hello text')

    kb = InlineKeyboardBuilder()  # some keyboard
    kb.row(
        types.InlineKeyboardButton(
            text=str(random.randint(1000000, 10000000)),
            callback_data='pass'
        )
    )
    kb.row(
        types.InlineKeyboardButton(
            text=str(random.randint(1000000, 10000000)),
            callback_data='pass'
        )
    )
    kb.row(

            types.InlineKeyboardButton(
                text=str(random.randint(1000000, 10000000)),
                callback_data='pass'
            ),

    )
    kb.row(
        types.InlineKeyboardButton(
            text=str(random.randint(1000000, 10000000)),
            callback_data='pass'
        )
    )
    paginator = Paginator(data=kb.as_markup(), size=2, dp=dp)
    # pprint(
    #     kb.inline_keyboard
    # )
    await message.answer(
        text='Some menu',
        reply_markup=paginator(),
        # reply_markup=kb.as_markup()
    )
    # args, kwargs = paginator.paginator_handler()
    # dp.callback_query.register(*args, **kwargs)


if __name__ == '__main__':
    async def start_bot():
        await dp.start_polling(bot)

    e = asyncio.new_event_loop()
    e.run_until_complete(start_bot())
