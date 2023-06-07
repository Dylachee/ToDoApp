import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
import requests
from aiogram import executor

API_TOKEN = '6121953768:AAHna5KPC4Ji71ytW0YeV-_pLPEg0cDrkQw'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Привет! Этот бот поможет управлять списком TODO. Используй команду /help для получения списка доступных команд.")


@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    help_text = "Доступные команды:\n\n" \
                "/start - начать\n" \
                "/help - получить список команд\n" \
                "/list - показать список TODO\n" \
                "/add - добавить новый TODO\n" \
                

    await message.reply(help_text)


@dp.message_handler(commands=['list'])
async def cmd_list(message: types.Message):
    response = requests.get('http://127.0.0.1:8000/todos/')  # Отправляем GET-запрос на ваш сервер
    todos = response.json()  # Получаем список TODO из ответа сервера
    if todos:
        response_text = "Список TODO:\n\n"
        for index, todo in enumerate(todos, start=1):
            task = todo.get('task', 'Нет описания')
            completed = todo.get('completed', False)
            status = '[x]' if completed else '[ ]'
            response_text += f"{index}. {status} {task}\n"
    else:
        response_text = "Список TODO пуст."

    await message.reply(response_text, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['add'])
async def cmd_add(message: types.Message):
    await message.reply("Введите новую задачу:")


@dp.message_handler()
async def add_todo(message: types.Message):
    new_todo = {"task": message.text, "completed": False}
    response = requests.post('http://127.0.0.1:8000/todos/', json=new_todo)  # Отправляем POST-запрос на ваш сервер для добавления нового TODO

    if response.status_code == 201:
        await message.reply("Задача успешно добавлена!")
    else:
        await message.reply("Не удалось добавить задачу.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
