from aiogram.types import ( 
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)

# Move dummy data to JSON
todos = [
    "Do homework",
    "Catch a bus"
]

todo_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=todo, callback_data="done")] for todo in todos
    ]
)