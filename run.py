from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
import asyncio
from routers import app




# старт бота
async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(app)
    await dp.start_polling(bot)


if __name__ == "__main__":
    # неубиваемый цикл
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            if e == KeyboardInterrupt:  # ctrl+c
                break
            with open("error.log", "a") as f:
                f.write(f"{e}\n")
