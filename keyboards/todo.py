import json
from aiogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)


def generate_todo_keyboard() -> InlineKeyboardMarkup:
    todos = json.load(open("./data/todos.json", "r"))
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{todo['task']}", 
                    callback_data=f"delete_{todo['id']}"
                )
            ] for todo in todos
        ]
    )


todo_keyboard = generate_todo_keyboard()
todo_keyboard.inline_keyboard.append(
    [InlineKeyboardButton(text="Add", callback_data="add_todo")]
)