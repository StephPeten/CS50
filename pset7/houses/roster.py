# TODO
from sys import argv, exit
from cs50 import SQL

if len(argv) != 2:
    print("Format : python roster.py HogwartsHouse")
    exit(1)

db = SQL("sqlite:///students.db")

students = db.execute("SELECT * FROM students WHERE house = (?) ORDER BY last", argv[1])

for row in students:
    if row['middle'] == None:
        print(f"{row['first']} {row['last']}, born {row['birth']}")
    else:
        print(f"{row['first']} {row['middle']} {row['last']}, born {row['birth']}")