import json
from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.text.startswith("delete"))
async def delete_task(query: CallbackQuery, callback_data: str) -> None:
    task_id = callback_data.split("_")[1]
    todos = json.load(open("./data/todos.json", "r"))
    todos = [todo for todo in todos if todo["id"] != task_id]
    json.dump(todos, open("./data/todos.json", "w"), indent=4)

    await query.answer("✅ Alright, you surely missed that!")
