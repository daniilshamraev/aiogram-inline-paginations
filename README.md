# aiogram-inline-paginations

## Description

A simple library for aiogram that allows you to easily do pagination for any Inline keyboards.

Install for pip:

```shell
pip install aiogram-inline-paginations
```

Install for poetry:

```shell
poetry add aiogram-inline-paginations
```

## Create paginations object

```python
from aiogram_inline_paginations.paginator import Paginator
from aiogram import types

kb = types.InlineKeyboardMarkup()
paginator = Paginator(data=kb, size=5)
```

### Params

**data**: Any ready-to-use keyboard InlineKeyboardMarkup or any iterable object with InlineKeyboardButton.

**size**: The number of rows of buttons on one page, excluding the navigation bar.

### Return

A paginator object that, when called, returns a ready-made keyboard with pagination.

## Get data for registrations handler paginator

```python
from aiogram_inline_paginations.paginator import Paginator
from aiogram import types

kb = types.InlineKeyboardMarkup()
paginator = Paginator(data=kb, size=5)


@dp.message_handler()
async def some_func(message: types.Message):
    await message.answer(
        text='Some menu',
        reply_markup=paginator()
    )

    args, kwargs = paginator.paginator_handler()
    dp.register_callback_query_handler(*args, **kwargs)

```

### Return paginator_handler()

Data for registrations paginator.

## Example

```python
import random

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.executor import Executor

from aiogram_inline_paginations.paginator import Paginator

token = 'your token'

storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(CommandStart(), state='*')
async def start(message: types.Message):
    await message.answer('Hello text')

    kb = types.InlineKeyboardMarkup()  # some keyboard

    '''To demonstrate, I will add more than 50 buttons to the keyboard and divide them into 5 lines per page'''
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

```

## Screenshots

First page:

![img_1.png](https://github.com/daniilshamraev/aiogram-inline-paginations/blob/master/img/img_1.png?raw=true)

Second page:

![img_2.png](https://github.com/daniilshamraev/aiogram-inline-paginations/blob/master/img/img_2.png?raw=true)

Last page:

![img_3.png](https://github.com/daniilshamraev/aiogram-inline-paginations/blob/master/img/img_3.png?raw=true)

*The order of entries is not lost.*

## License MIT