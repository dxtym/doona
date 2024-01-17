import json
from contextlib import suppress
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from keyboards.todo import generate_todo_keyboard

router = Router()


@router.callback_query(lambda callback_query: callback_query.data.startswith("delete"))
async def delete_task(query: CallbackQuery) -> None:
    task_id = int(query.data.split("_")[1])
    todos = json.load(open("./data/todos.json", "r"))
    for todo in todos:
        if todo["id"] == task_id:
            todos.remove(todo)
            break
    json.dump(todos, open("./data/todos.json", "w"), indent=4)

    todo_keyboard = generate_todo_keyboard()

    with suppress(TelegramBadRequest):
        await query.message.edit_text(
            f"📝 Things you've to finish:\n",
            reply_markup=todo_keyboard
        )
    await query.answer("💅 Alright, I'm sure you missed that!")