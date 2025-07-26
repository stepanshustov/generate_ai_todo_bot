from typing import *

from gigachat import GigaChat
from config import GIGACHAT_API_KEY, GIGACHAT_PROMPT
from datetime import datetime
import asyncio

# Словари для перевода месяца и дня недели
months_ru = {
    1: "января", 2: "февраля", 3: "марта",
    4: "апреля", 5: "мая", 6: "июня",
    7: "июля", 8: "августа", 9: "сентября",
    10: "октября", 11: "ноября", 12: "декабря"
}

weekdays_ru = {
    0: "понедельник", 1: "вторник", 2: "среда",
    3: "четверг", 4: "пятница", 5: "суббота", 6: "воскресенье"
}


def get_today() -> str:
    today = datetime.today()
    day = today.day
    month = months_ru[today.month]
    weekday = weekdays_ru[today.weekday()]

    return f"{day} {month} {weekday}"


# при успехе вернет True и список задач в формате: [дата] | [время] | [список задач]
async def make_to_do_list(tin: str) -> Tuple[bool, str]:
    try:
        if len(tin.split()) > 100:
            return False, "Слишком длинный запрос"
        tin = ' '.join(tin.split())
        async with GigaChat(credentials=GIGACHAT_API_KEY, verify_ssl_certs=False) as giga:
            today = get_today()
            response = await giga.achat(GIGACHAT_PROMPT.format(tin, today))
        tout = response.choices[0].message.content.split("\n")
        # print(response.choices[0].message.content)
        if tout[0].lower().strip() == "да":
            return True, "\n".join(tout[1:])
        return False, "Проверьте запрос и попробуйте еще раз"
    except Exception as e:
        with open("error.log", "a") as f:
            f.write(f"{e}\n")
        return False, "Не удалось обработать запрос"


# async def main():
#     a = input()
#     print((await make_to_do_list(a))[1])
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
#     # print(get_today())
