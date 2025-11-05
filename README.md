# aiogram-inline-paginations

Простая библиотека для aiogram, которая позволяет легко создавать пагинацию для любых Inline-клавиатур.

## Установка

### Установка через pip:

```shell
pip install aiogram-inline-paginations
```

### Установка через poetry:

```shell
poetry add aiogram-inline-paginations
```

## Быстрый старт

### Создание объекта пагинации

```python
from aiogram_inline_paginations.paginator import Paginator
from aiogram import types

kb = types.InlineKeyboardMarkup()
paginator = Paginator(data=kb, size=5)
```

## API Reference

### Класс `Paginator`

Основной класс для создания пагинации клавиатур.

#### Параметры конструктора

- **`data`** (`types.InlineKeyboardMarkup | Iterable[types.InlineKeyboardButton] | Iterable[Iterable[types.InlineKeyboardButton]] | InlineKeyboardBuilder`): 
  - Готовая клавиатура `InlineKeyboardMarkup` или любой итерируемый объект с кнопками `InlineKeyboardButton`.
  - Можно передать список списков кнопок или `InlineKeyboardBuilder`.

- **`size`** (`int`, по умолчанию: `8`): 
  - Количество строк кнопок на одной странице, исключая панель навигации.

- **`callback_startswith`** (`str`, по умолчанию: `'page_'`): 
  - Префикс для `callback_data` в обработчике пагинации. Используется для идентификации callback-запросов пагинации.

- **`page_separator`** (`str`, по умолчанию: `'/'`): 
  - Разделитель для номеров страниц в отображении (например, "1/5").

- **`state`** (`State | None`, по умолчанию: `None`): 
  - Текущее состояние FSM (опционально). Используется для привязки обработчиков к определенному состоянию.

- **`dp`** (`Dispatcher | Router | None`, по умолчанию: `None`): 
  - Диспетчер или роутер aiogram. Если передан, обработчики пагинации будут зарегистрированы автоматически.

#### Методы

##### `__call__(current_page: int = 0) -> types.InlineKeyboardMarkup`

Возвращает клавиатуру с пагинацией для указанной страницы.

**Параметры:**
- `current_page` (`int`, по умолчанию: `0`): Номер текущей страницы (начиная с 0).

**Возвращает:**
- `types.InlineKeyboardMarkup`: Клавиатура с кнопками текущей страницы и элементами управления пагинацией.

**Пример:**
```python
await message.answer(
    text='Some menu',
    reply_markup=paginator(current_page=0)
)
```

##### `paginator_handler() -> tuple | None`

Возвращает данные для регистрации обработчика пагинации (если `dp` не передан).

**Возвращает:**
- `tuple[Callable, Text] | None`: Кортеж с обработчиком и фильтром, или `None` если обработчик уже зарегистрирован через `dp`.

**Пример использования без `dp`:**
```python
paginator = Paginator(data=kb, size=5)

# Регистрация обработчика вручную
args, kwargs = paginator.paginator_handler()
if args:
    dp.callback_query.register(*args, **kwargs)
```

### Класс `CheckBoxPaginator`

Класс для создания пагинации с возможностью выбора элементов (чекбоксы).

Наследуется от `Paginator` и добавляет функциональность выбора элементов.

#### Дополнительные параметры конструктора

- **`callback_startswith_button`** (`str`, по умолчанию: `'select_'`): 
  - Префикс для `callback_data` кнопок, которые можно выбрать.

- **`confirm_text`** (`str`, по умолчанию: `'Подтвердить'`): 
  - Текст на кнопке подтверждения выбора.

Все остальные параметры идентичны параметрам класса `Paginator`.

#### Методы

##### `__call__(current_page: int = 0, selected: list[str] | None = None) -> types.InlineKeyboardMarkup`

Возвращает клавиатуру с пагинацией и выбранными элементами.

**Параметры:**
- `current_page` (`int`, по умолчанию: `0`): Номер текущей страницы.
- `selected` (`list[str] | None`, по умолчанию: `None`): Список `callback_data` выбранных кнопок.

**Возвращает:**
- `types.InlineKeyboardMarkup`: Клавиатура с пагинацией, выбранными элементами (помечены ✅) и кнопкой подтверждения.

##### `select_handler() -> tuple | None`

Возвращает данные для регистрации обработчика выбора элементов (если `dp` не передан).

**Возвращает:**
- `tuple[Callable, Text], dict | None`: Данные для регистрации обработчика, или `None` если обработчик уже зарегистрирован.

## Примеры использования

### Пример 1: Базовое использование с автоматической регистрацией

```python
import asyncio
import random

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram_inline_paginations.paginator import Paginator

token = 'your token'

storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(storage=storage)


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer('Hello text')

    kb = InlineKeyboardBuilder()
    
    # Добавляем более 50 кнопок для демонстрации пагинации
    for i in range(57):
        kb.row(
            types.InlineKeyboardButton(
                text=str(random.randint(1000000, 10000000)),
                callback_data='pass'
            )
        )

    # Создаем пагинатор с автоматической регистрацией обработчиков
    paginator = Paginator(data=kb.as_markup(), size=5, dp=dp)

    await message.answer(
        text='Some menu',
        reply_markup=paginator()
    )


if __name__ == '__main__':
    async def main():
        await dp.start_polling(bot)

    asyncio.run(main())
```

### Пример 2: Использование без автоматической регистрации обработчиков

```python
from aiogram_inline_paginations.paginator import Paginator
from aiogram.filters import Text

# Создаем пагинатор без dp
paginator = Paginator(data=kb, size=5)

# Регистрируем обработчик вручную
args, kwargs = paginator.paginator_handler()
if args:
    dp.callback_query.register(*args, **kwargs)

# Используем пагинатор
await message.answer(
    text='Some menu',
    reply_markup=paginator(current_page=0)
)
```

### Пример 3: CheckBoxPaginator с выбором элементов

```python
import asyncio
import random

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram_inline_paginations.paginator import CheckBoxPaginator

token = 'your token'

storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(storage=storage)


@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await message.answer('Hello text')

    kb = types.InlineKeyboardMarkup()
    
    # Создаем клавиатуру с кнопками
    for i in range(10):
        kb.add(
            types.InlineKeyboardButton(
                text=f'Item {i}',
                callback_data=f'select_{i}'
            )
        )
    
    # Создаем пагинатор с выбором элементов
    paginator = CheckBoxPaginator(
        data=kb,
        size=5,
        callback_startswith='page_',
        callback_startswith_button='select_',
        confirm_text='Approve',
        dp=dp
    )
    
    await message.answer(
        text='Select items:',
        reply_markup=paginator()
    )


@dp.callback_query(Text(startswith='Approve', endswith='confirm'))
async def approve(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    # Получаем выбранные элементы
    selected = data.get('page_selected', None)
    
    if selected:
        await call.answer(
            text=f'Your selected:\n' + '\n'.join(selected)
        )
    else:
        await call.answer(text='Nothing selected')


if __name__ == '__main__':
    async def main():
        await dp.start_polling(bot)

    asyncio.run(main())
```

## Работа с выбранными элементами (CheckBoxPaginator)

### Получение выбранных элементов

Выбранные элементы хранятся в состоянии FSM под ключом `{callback_startswith}selected`:

```python
data = await state.get_data()
selected = data.get(f'{callback_startswith}selected', None)
```

### Обработка callback подтверждения

Кнопка подтверждения создает callback с данными в формате:
```python
f"{confirm_text}confirm"
```

Пример обработки:
```python
@dp.callback_query(Text(startswith='Approve', endswith='confirm'))
async def approve(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = data.get('page_selected', None)
    # Обработка выбранных элементов
```

## Обработка ошибок

### Пустая клавиатура

Если передана пустая клавиатура, будет выброшено исключение:

```python
try:
    paginator = Paginator(data=empty_kb, size=5)
    await message.answer(reply_markup=paginator())
except ValueError as e:
    await message.answer(f"Ошибка: {e}")
```

### Некорректный номер страницы

Если указан номер страницы вне допустимого диапазона, он будет автоматически скорректирован:

```python
# Если current_page < 0, будет установлено 0
# Если current_page >= количества страниц, будет установлен индекс последней страницы
paginator(current_page=999)  # Автоматически скорректируется
```

### Некорректный callback_data

Если callback_data не соответствует ожидаемому формату, метод `_get_page` выбросит исключение:

```python
# В обработчике пагинации будет выброшено ValueError
# если callback_data не начинается с callback_startswith
```

## Screenshots

### Первая страница:

![img_1.png](https://github.com/daniilshamraev/aiogram-inline-paginations/blob/master/img/img_1.png?raw=true)

### Вторая страница:

![img_2.png](https://github.com/daniilshamraev/aiogram-inline-paginations/blob/master/img/img_2.png?raw=true)

### Последняя страница:

![img_3.png](https://github.com/daniilshamraev/aiogram-inline-paginations/blob/master/img/img_3.png?raw=true)

*Порядок элементов сохраняется.*

## Лицензия

MIT License
