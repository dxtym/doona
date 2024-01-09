import sqlite3 as sql

db = sql.connect("app/database/timetable.db")
cursor = db.cursor()

async def show_timetable(bot):
    await cursor.execute("SELECT * FROM timetable")
    await bot.answer(f"Timetable: {cursor.fetchall()}")

async def show_timetable_by_day(bot, day):
    await cursor.execute(f"SELECT * FROM timetable WHERE day='{day}'")
    await bot.answer(f"Timetable for {day}: {cursor.fetchall()}")
    
