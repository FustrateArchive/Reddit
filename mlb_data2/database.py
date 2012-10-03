"""
"""

import sqlite3

connection = sqlite3.connect("./baseball.db")
connection.row_factory = sqlite3.Row
db = connection.cursor()
db_version = 1