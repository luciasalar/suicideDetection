import csv
from sys import argv
from os import listdir
from typing import List

def getTrueLabel(scores: List[str]) -> str:
    scores_float = [float(x) for x in scores]
    if min(scores_float) == scores_float[0]:
            return 'a'
    elif min(scores_float) == scores_float[1]:
        return 'b'
    elif min(scores_float) == scores_float[2]:
        return 'c'
    else:
        return 'd'

with open(argv[2], 'w', newline='') as csvfile:
    fieldnames = ['userid', 'a_score', 'b_score', 'c_score', 'd_score', 'predicted_label']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for directory in listdir(argv[1]):
        for filename in listdir(argv[1] + "/" + directory):
            with open(argv[1] + "/" + directory + "/" + filename, 'r') as inputfile:
                line = inputfile.readline().strip().split()
                label = getTrueLabel(line)
                writer.writerow({'userid': filename.split('.')[0], 'a_score': line[0], 'b_score': line[1], 'c_score': line[2], 'd_score': line[3], 'predicted_label': label})
