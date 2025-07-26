from typing import Tuple

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import asyncio

# Загрузка шрифтов
try:
    font_title = ImageFont.truetype("fonts/Roboto-Bold.ttf", 32)
    font_date = ImageFont.truetype("fonts/Roboto-Bold.ttf", 24)
    font_time = ImageFont.truetype("fonts/Roboto-Regular.ttf", 22)
    font_task = ImageFont.truetype("fonts/Roboto-Regular.ttf", 22)
except:
    # Fallback на системные шрифты
    font_title = ImageFont.load_default(32)
    font_date = ImageFont.load_default(24)
    font_time = ImageFont.load_default(22)
    font_task = ImageFont.load_default(22)

# Параметры оформления
BG_COLOR = (250, 250, 190)  # Белый фон
HEADER_COLOR = (70, 130, 180)  # SteelBlue
TEXT_COLOR = (0, 0, 0)  # Чёрный
DATE_COLOR = (50, 50, 50)  # Тёмно-серый
TIME_COLOR = (100, 100, 100)  # Серый
ACCENT_COLOR = (30, 144, 255)  # DodgerBlue

# Отступы и размеры
Y_PADDING = 70


# Генерирует изображение из списка задач
def generate_todo_image(tasks: list) -> BytesIO:
    mxw = font_title.getlength("СПИСОК ДЕЛ") + 50  # Определяем максимальную ширину текста
    max_date_len = 0  # Определяем максимальную длину даты
    for el in tasks:
        max_date_len = max(max(font_date.getlength(el[0]), font_date.getlength(el[1])),
                           max_date_len)
    max_date_len += 50
    for el in tasks:
        mxw = max(mxw, font_task.getlength(el[2]))
    # Рассчитываем высоту изображения
    total_height = Y_PADDING * len(tasks) + 100  # Отступы + заголовок
    total_width = + int(mxw + 30) + int(max_date_len) # Отступы + ширина текста # Отступы + задачи

    # Создаём изображение с рассчитанной высотой
    img = Image.new('RGB', (total_width, total_height), BG_COLOR)
    draw = ImageDraw.Draw(img)
    header_xy = (total_width // 2, Y_PADDING - 40)
    # Рисуем заголовок
    draw.text(
        header_xy,
        "СПИСОК ДЕЛ",
        font=font_title,
        fill=(90, 90, 240),
        anchor="mm"
    )

    # Рисуем задачи
    for i, el in enumerate(tasks):
        # Рисуем дату
        draw.text(
            (30, Y_PADDING * (i + 1)),
            el[0],
            font=font_date,
            fill=DATE_COLOR
        )

        # Рисуем время
        draw.text(
            (30, Y_PADDING * (i + 1.4)),
            f"{el[1]}",
            font=font_time,
            fill=TIME_COLOR
        )

        # Рисуем задачу
        draw.text(
            (max_date_len, Y_PADDING * (i + 1)),
            el[2],
            font=font_task,
            fill=TEXT_COLOR
        )
    # Сохраняем в BytesIO
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG', quality=95)
    img_bytes.seek(0)
    return img_bytes


# Выполняет генерацию изображения в отдельном потоке, чтобы не блокировать основной поток
async def async_generate_todo_image(tasks: list) -> Tuple[bool, BytesIO | None]:
    try:
        img = await asyncio.to_thread(generate_todo_image, tasks)
        return True, img
    except Exception as e:
        with open("error.log", "a") as f:
            f.write(f"{e}\n")
        return False, None


if __name__ == "__main__":
    tasks = [
        ("12 ", "12:00", "Сделать задачу 1"),
        ("13 июля", "13:00", "Сделать задачу 2"),
        ("14 июля", "14:00", "Сделать  3")]
    img_bytes = generate_todo_image(tasks)

    # Сохраняем в файл
    with open('test_image.png', 'wb') as f:
        f.write(img_bytes.getvalue())  # Берём сырые байты и пишем в файл
