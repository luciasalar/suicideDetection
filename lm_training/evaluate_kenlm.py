from sys import argv
from os import listdir

class_a = 0
class_b = 0
class_c = 0
class_d = 0

for filename in listdir(argv[1]):
    with open(argv[1] + "/" + filename, 'r') as inputfile:
        line = [float(x) for x in inputfile.readline().strip().split()]
        if min(line) == line[0]:
            class_a += 1
        elif min(line) == line[1]:
            class_b += 1
        elif min(line) == line[2]:
            class_c += 1
        else:
            class_d += 1
print("A:", class_a, "B:", class_b, "C:", class_c, "D:", class_d)
