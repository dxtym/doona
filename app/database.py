import sqlite3 as sql

db= sql.connect('database.db')
cursor = db.cursor()

# TODO: Add timetable to database for caching