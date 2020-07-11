from csv import reader, DictReader
import csv
from sys import argv, exit


if len(argv) != 3:
    print("Format : python dna.py data.csv sequence.txt")
    exit(1)

with open(argv[1], newline='') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        azote = row
        azote.pop(0)
        break

azotes = {}

for item in azote:
    azotes[item] = 1

with open(argv[2]) as txtfile:
    seqreader = reader(txtfile)
    for line in seqreader:
        seq = line

sequence = seq[0]

for key in azotes:
    k = len(key)
    count = 0
    countMAX = 0
    
    for i in range(len(sequence)):
        while count > 0:
            count -= 1

        if sequence[i: i + k] == key:
            while sequence[i - k: i] == sequence[i: i + k]:
                count += 1
                i += k

            if count > countMAX:
                countMAX = count

    azotes[key] += countMAX


with open(argv[1], newline='') as csvfile:
    datareader = DictReader(csvfile)
    for moldu in datareader:
        match = 0

        for sequence in azotes:
            if azotes[sequence] == int(moldu[sequence]):
                match += 1
        if match == len(azotes):
            print(moldu['name'])
            exit()

    print("No match")