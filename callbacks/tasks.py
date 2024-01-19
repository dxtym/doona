import json
from contextlib import suppress
from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from states.task import Task
from keyboards.todo import generate_todo_keyboard

router = Router()


@router.callback_query(lambda query: query.data.startswith("delete"))
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


@router.callback_query(lambda message: message.data == "add_todo")
async def add_task(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Task.desc)
    await query.message.answer("🤦‍♀️ What do you want to add?")


@router.message(Task.desc)
async def task_name(message: Message, state: FSMContext) -> None:
    todos = json.load(open("./data/todos.json", "r"))
    todos.append({
        "id": len(todos) + 1,
        "task": message.text
    })
    json.dump(todos, open("./data/todos.json", "w"), indent=4)

    await state.clear()
    todo_keyboard = generate_todo_keyboard()
    await message.answer(
        f"📝 Things you've to finish:\n",
        reply_markup=todo_keyboard
    )