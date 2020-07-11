# TODO
from sys import argv, exit
from cs50 import SQL
import csv

if len(argv) != 2:
    print("Format : python import.py characters.csv")
    exit(1)

db = SQL("sqlite:///students.db")

with open(argv[1], 'r', newline='') as studentfile:
    students = csv.reader(studentfile)
    for row in students:
        if row[0] == "name":
            continue

        Names = row[0].split()
        if len(Names) == 3:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       Names[0], Names[1], Names[2], row[1], row[2])

        else:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       Names[0], None, Names[1], row[1], row[2])