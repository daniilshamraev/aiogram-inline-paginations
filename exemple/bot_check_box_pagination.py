import random

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.executor import Executor

from aiogram_inline_paginations.paginator import CheckBoxPaginator

token = 'your token'

storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(CommandStart(), state='*')
async def start(message: types.Message):
    await message.answer('Hello text')

    kb = types.InlineKeyboardMarkup()  # some keyboard
    kb.add(
        *[
            types.InlineKeyboardButton(
                text=str(random.randint(1000000, 10000000)),
                callback_data=f'pass_{str(random.randint(1000000, 10000000))}'
            ) for i in range(2)
        ]
    )
    kb.add(
        *[
            types.InlineKeyboardButton(
                text=str(random.randint(1000000, 10000000)),
                callback_data=f'pass_{str(random.randint(1000000, 10000000))}'
            ) for i in range(3)
        ]
    )
    kb.add(
        types.InlineKeyboardButton(
            text=str(random.randint(1000000, 10000000)),
            callback_data=f'pass_{str(random.randint(1000000, 10000000))}'
        )
    )
    kb.add(
        *[
            types.InlineKeyboardButton(
                text=str(random.randint(1000000, 10000000)),
                callback_data=f'pass_{str(random.randint(1000000, 10000000))}'
            ) for i in range(2)
        ]
    )
    kb.add(
        *[
            types.InlineKeyboardButton(
                text=str(random.randint(1000000, 10000000)),
                callback_data=f'pass_{str(random.randint(1000000, 10000000))}'
            ) for i in range(50)
        ]
    )
    paginator = CheckBoxPaginator(
        data=kb,
        size=5,
        callback_startswith='page_',
        callback_startswith_button='pass_',
        confirm_text='Approve'
    )
    await message.answer(
        text='Some menu',
        reply_markup=paginator()
    )
    args, kwargs = paginator.paginator_handler()
    dp.register_callback_query_handler(*args, **kwargs)

    args, kwargs = paginator.select_handler()
    dp.register_callback_query_handler(*args, **kwargs)


if __name__ == '__main__':
    Executor(dp).start_polling()
