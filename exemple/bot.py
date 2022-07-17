import random

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.executor import Executor

from paginator import Paginator

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
                callback_data='pass'
            ) for i in range(2)
        ]
    )
    kb.add(
        *[
            types.InlineKeyboardButton(
                text=str(random.randint(1000000, 10000000)),
                callback_data='pass'
            ) for i in range(3)
        ]
    )
    kb.add(
        types.InlineKeyboardButton(
            text=str(random.randint(1000000, 10000000)),
            callback_data='pass'
        )
    )
    kb.add(
        *[
            types.InlineKeyboardButton(
                text=str(random.randint(1000000, 10000000)),
                callback_data='pass'
            ) for i in range(2)
        ]
    )
    kb.add(
        *[
            types.InlineKeyboardButton(
                text=str(random.randint(1000000, 10000000)),
                callback_data='pass'
            ) for i in range(50)
        ]
    )
    paginator = Paginator(data=kb, size=5)
    await message.answer(
        text='Some menu',
        reply_markup=paginator()
    )
    args, kwargs = paginator.paginator_handler()
    dp.register_callback_query_handler(*args, **kwargs)


if __name__ == '__main__':
    Executor(dp).start_polling()
