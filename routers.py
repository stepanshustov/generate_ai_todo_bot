import time
from typing import *
from aiogram.filters import *
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, BaseMiddleware
from aiogram.types import *

from AI_gigachat import make_to_do_list
from image_generator import async_generate_todo_image
from config import HELP_MESSAGE, START_MESSAGE

# защита от спама
class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 0.5):
        self.rate_limit = rate_limit
        self.last_processed = {}

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        # Проверяем, что событие - это сообщение
        if not isinstance(event, Message):
            return await handler(event, data)

        user_id = event.from_user.id
        current_time = time.time()

        # Проверяем время последнего сообщения
        if user_id in self.last_processed:
            elapsed = current_time - self.last_processed[user_id]
            if elapsed < self.rate_limit:
                # Если сообщение пришло слишком рано - блокируем
                await event.answer("⏳ Слишком часто! Подождите немного...")
                return

        # Обновляем время последнего сообщения
        self.last_processed[user_id] = current_time
        return await handler(event, data)


class MyStates(StatesGroup):
    users_request = State()


app = Router()
app.message.middleware(ThrottlingMiddleware(5)) # запрос раз в 5 секунд


@app.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(START_MESSAGE, parse_mode="html", )


@app.message(Command("help"))
async def help_(message: Message):
    await message.answer(HELP_MESSAGE, parse_mode="html")


@app.message()
async def users_request(message: Message, state: FSMContext):
    t = message.text.strip()
    resp = await make_to_do_list(t)  # (bool, str)
    if not resp[0]:
        await message.answer(resp[1])  # ошибка/некорректный запрос
        return

    # получаем список дел
    todolist = [list(map(str.strip, el.split("|"))) for el in resp[1].split("\n")]
    # Получаем и проверяем результат
    res = await async_generate_todo_image(todolist)
    # print(res)
    if not res[0]:
        await message.answer("Произошла ошибка при генерации изображения.")
        return
    img_bytesio = res[1]

    # Сбрасываем курсор в начало
    img_bytesio.seek(0)

    # Создаём BufferedInputFile
    image_file = BufferedInputFile(
        file=img_bytesio.getvalue(),
        filename="todo_list.png"
    )
    await message.answer_photo(photo=image_file)
