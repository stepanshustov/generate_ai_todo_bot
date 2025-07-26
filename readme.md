# 🤖 AI To-Do List Generator Bot (Telegram)
_Учебный проект | Learning project_

Генерирует визуальную картинку списка дел на основе текста с помощью LLM **GigaChat Lite**.  
Generates visual to-do list images from text using **GigaChat Lite** LLM.

[Telegram Bot](https://t.me/aigeneratetodobot)  
⚠️ **Бот может временно не работать из-за исчерпания бесплатных токенов GigaChat!**  
⚠️ **Bot may be unavailable due to exhausted free tokens!**

## ⚙️ Требования | Requirements
- Python 3.9+ (проверено на 3.10.12/3.12.3 Linux)
- API-ключ [GigaChat](https://developers.sber.ru/portal/products/gigachat)
- Токен Telegram-бота ([@BotFather](https://t.me/BotFather))
- `pip install -r req.txt`

## 🚀 Быстрый старт | Quick Start
```bash
# 1. Установите зависимости
pip install -r req.txt

# 2. Создайте .env файл и добавьте токены:
echo "BOT_TOKEN=ваш_токен_телеграм" > .env
echo "GIGACHAT_API_KEY=ваш_токен_гигачат" >> .env

# 3. Запустите бота
python run.py
