from itertools import islice
from pprint import pprint
from typing import Iterable, Any, Iterator, Callable, Coroutine, Tuple

from aiogram import types, Dispatcher, Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Paginator:
    def __init__(
            self,
            data: types.InlineKeyboardMarkup |
                  Iterable[types.InlineKeyboardButton] |
                  Iterable[Iterable[types.InlineKeyboardButton]] |
                  InlineKeyboardBuilder
            ,
            state: State = None,
            callback_startswith: str = 'page_',
            size: int = 8,
            page_separator: str = '/',
            dp: Dispatcher | Router | None = None,
    ):
        """
        Example: paginator = Paginator(data=kb, size=5)

        :param data: An iterable object that stores an InlineKeyboardButton.
        :param callback_startswith: What should callback_data begin with in handler pagination. Default = 'page_'.
        :param size: Number of lines per page. Default = 8.
        :param state: Current state.
        :param page_separator: Separator for page numbers. Default = '/'.
        """
        self.dp = dp
        self.page_separator = page_separator
        self._state = state
        self._size = size
        self._startswith = callback_startswith
        if isinstance(data, types.InlineKeyboardMarkup):
            self._list_kb = list(
                self._chunk(
                    it=data.inline_keyboard,
                    size=self._size
                )
            )
        elif isinstance(data, Iterable):
            self._list_kb = list(
                self._chunk(
                    it=data,
                    size=self._size
                )
            )
        elif isinstance(data, InlineKeyboardBuilder):
            self._list_kb = list(
                self._chunk(
                    it=data.export(),
                    size=self._size
                )
            )
        else:
            raise ValueError(f'{data} is not valid data')

    """
    Class for pagination's in aiogram inline keyboards
    """

    def __call__(
            self,
            current_page=0,
            *args,
            **kwargs
    ) -> types.InlineKeyboardMarkup:
        """
        Example:

        await message.answer(
            text='Some menu',
            reply_markup=paginator()
        )

        :return: InlineKeyboardMarkup
        """
        _list_current_page = self._list_kb[current_page]

        paginations = self._get_paginator(
            counts=len(self._list_kb),
            page=current_page,
            page_separator=self.page_separator,
            startswith=self._startswith
        )
        pprint(
            [*_list_current_page, paginations]
        )
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[*_list_current_page, paginations])

        # keyboard.add(_list_current_page)
        # keyboard.row(paginations)
        # keyboard.adjust(3)

        if self.dp:
            self.paginator_handler()

        return keyboard

    @staticmethod
    def _get_page(call: types.CallbackQuery) -> int:
        """
        :param call: CallbackQuery in paginator handler.
        :return: Current page.
        """
        return int(call.data[-1])

    @staticmethod
    def _chunk(it, size) -> Iterator[tuple[Any, ...]]:
        """
        :param it: Source iterable object.
        :param size: Chunk size.
        :return: Iterator chunks pages.
        """
        it = iter(it)
        return iter(lambda: tuple(islice(it, size)), ())

    @staticmethod
    def _get_paginator(
            counts: int,
            page: int,
            page_separator: str = '/',
            startswith: str = 'page_'
    ) -> list[types.InlineKeyboardButton]:
        """
        :param counts: Counts total buttons.
        :param page: Current page.
        :param page_separator: Separator for page numbers. Default = '/'.
        :return: Page control line buttons.
        """
        counts -= 1

        paginations = []

        if page > 0:
            paginations.append(
                types.InlineKeyboardButton(
                    text='⏮️️',
                    callback_data=f'{startswith}0'
                )
            )
            paginations.append(
                types.InlineKeyboardButton(
                    text='⬅️',
                    callback_data=f'{startswith}{page - 1}'
                ),
            )
        paginations.append(
            types.InlineKeyboardButton(
                text=f'{page + 1}{page_separator}{counts + 1}',
                callback_data='pass'
            ),
        )
        if counts > page:
            paginations.append(
                types.InlineKeyboardButton(
                    text='➡️',
                    callback_data=f'{startswith}{page + 1}'
                )
            )
            paginations.append(
                types.InlineKeyboardButton(
                    text='⏭️',
                    callback_data=f'{startswith}{counts}'
                )
            )
        return paginations

    def paginator_handler(self) -> tuple[Callable[[CallbackQuery, FSMContext], Coroutine[Any, Any, None]], Text]:
        """
        Example:

        args, kwargs = paginator.paginator_handler()

        dp.register_callback_query_handler(*args, **kwargs)

        :return: Data for register handler pagination.
        """

        async def _page(call: types.CallbackQuery, state: FSMContext):
            page = self._get_page(call)

            await call.message.edit_reply_markup(
                reply_markup=self.__call__(
                    current_page=page
                )
            )
            await state.update_data({f'last_page_{self._startswith}': page})

        if not self.dp:
            return \
                (_page, Text(startswith=self._startswith))
        else:
            self.dp.callback_query.register(
                _page,
                Text(startswith=self._startswith),
            )

    # def paginator_handler(self):
    #     def decorator(func):
    #         def _wrapper(context: dict, *args, **kwargs):
    #             func(
    #                 context={
    #                     'startswith': self._startswith,
    #                     'state': self._state,
    #                     'data': self._list_kb,
    #                     'size': self._size
    #                 },
    #                 *args,
    #                 **kwargs
    #             )
    #
    #         return _wrapper
    #
    #     return decorator


class CheckBoxPaginator(Paginator):

    def __init__(self, data: types.InlineKeyboardMarkup |
                             Iterable[types.InlineKeyboardButton] |
                             Iterable[Iterable[types.InlineKeyboardButton]],
                 state: State = None,
                 callback_startswith: str = 'page_',
                 size: int = 8,
                 page_separator: str = '/',
                 callback_startswith_button: str = 'select_',
                 confirm_text: str = 'Подтвердить',
                 dp: Dispatcher | None = None):
        """
        Example: paginator = Paginator(data=kb, size=5)

        :param data: An iterable object that stores an InlineKeyboardButton.
        :param callback_startswith: What should callback_data begin with in handler pagination. Default = 'page_'.
        :param size: Number of lines per page. Default = 8.
        :param state: Current state.
        :param page_separator: Separator for page numbers. Default = '/'.
        :param callback_startswith_button: Callback start with buttons.
        :param confirm_text: Text on button confirm.
        """

        super().__init__(data, state, callback_startswith, size, page_separator, dp)
        self.dp = dp
        self.page_separator = page_separator
        self._state = state
        self._size = size
        self._startswith = callback_startswith
        self._startswith_button = callback_startswith_button
        self._confirm_text = confirm_text
        if isinstance(data, types.InlineKeyboardMarkup):
            self._list_kb = list(
                self._chunk(
                    it=data.inline_keyboard,
                    size=self._size
                )
            )
        elif isinstance(data, Iterable):
            self._list_kb = list(
                self._chunk(
                    it=data,
                    size=self._size
                )
            )

    def __call__(
            self,
            current_page=0,
            selected: list[list[types.KeyboardButton]] = None,
            *args,
            **kwargs
    ) -> types.InlineKeyboardMarkup:
        """
        Example:

        await message.answer(
            text='Some menu',
            reply_markup=paginator()
        )

        :return: InlineKeyboardMarkup
        """
        _list_current_page = self._list_kb[current_page]

        for lst in _list_current_page:
            for button in lst:
                button: types.InlineKeyboardButton
                if selected:
                    if button.callback_data in selected:
                        if not button.text.endswith('✅'):
                            button.text += ' ✅'
                    else:
                        if button.text.endswith(' ✅'):
                            button.text = button.text[:-2]
                else:
                    if button.text.endswith(' ✅'):
                        button.text = button.text[:-2]

        paginations = self._get_paginator(
            counts=len(self._list_kb),
            page=current_page,
            page_separator=self.page_separator,
            startswith=self._startswith
        )
        keyboard = types.InlineKeyboardMarkup(
            row_width=5,
            inline_keyboard=_list_current_page
        )

        confirm_button = types.InlineKeyboardButton(
            text=self._confirm_text,
            callback_data=f'{self._confirm_text}confirm'
        )
        keyboard.inline_keyboard.append(*paginations)
        keyboard.inline_keyboard.append(*confirm_button)

        if self.dp:
            self.paginator_handler()
            self.select_handler()

        return keyboard

    def paginator_handler(self) -> tuple[
        tuple[Callable[[CallbackQuery], Coroutine[Any, Any, None]], Text],
        dict[str, State | str]
    ]:
        """
        Example:

        args, kwargs = paginator.paginator_handler()

        dp.register_callback_query_handler(*args, **kwargs)

        :return: Data for register handler pagination.
        """

        async def _page(call: types.CallbackQuery, state: FSMContext):
            page = self._get_page(call)
            data = await state.get_data()

            selected = data.get(f'{self._startswith}selected', None)
            if selected:
                kb = self.__call__(current_page=page, selected=selected)
            else:
                kb = self.__call__(current_page=page)
                await state.update_data({f'{self._startswith}selected': []})
            await call.message.edit_reply_markup(
                reply_markup=kb
            )
            await state.update_data({f'last_page_{self._startswith}': page})

        if not self.dp:
            return \
                (_page, Text(startswith=self._startswith)), \
                    {'state': self._state if self._state else '*'}
        else:
            self.dp.callback_query.register(
                _page,
                Text(startswith=self._startswith),
                **{'state': self._state if self._state else '*'}
            )

    def select_handler(self):

        async def _select(call: types.CallbackQuery, state: FSMContext):
            data = await state.get_data()
            page = data.get(f'last_page_{self._startswith}', 0)

            selected = data.get(f'{self._startswith}selected', [])

            if selected:
                selected: list

                if call.data in selected:
                    selected.remove(call.data)
                    await state.update_data({f'{self._startswith}selected': selected})
                else:
                    selected.append(call.data)
                    await state.update_data({f'{self._startswith}selected': selected})

                await state.update_data({f'{self._startswith}selected': selected})

                data = await state.get_data()
                selected = data.get(f'{self._startswith}selected', None)

                await call.message.edit_reply_markup(
                    reply_markup=self.__call__(
                        current_page=page,
                        selected=selected
                    )
                )
            else:
                await state.update_data({f'{self._startswith}selected': [call.data, ]})
                await call.message.edit_reply_markup(
                    reply_markup=self.__call__(
                        current_page=page,
                        selected=[call.data, ]
                    )
                )

            await state.update_data({f'last_page_{self._startswith}': page})

        if not self.dp:
            return \
                (_select, Text(startswith=self._startswith_button)), \
                    {'state': self._state if self._state else '*'}
        else:
            self.dp.callback_query.register(
                _select,
                Text(startswith=self._startswith_button),
                **{'state': self._state if self._state else '*'}
            )
