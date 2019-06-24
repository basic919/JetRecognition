from os import listdir
from math import sqrt
from collections import Counter


koefs = [[2, 2], [2, 3], [3, 2], [5, 2], [4, 3], [4, 2]]

koefs_str = []

for koef in koefs:
    koefs_str.append('(' + str(koef[0]) + ',' + str(koef[1]) + ')')

q = 1

scale_path = 'scale100'

input_path = "E:\Faks\Zavrsni\Backups\FullDB3\Test Data\\" + scale_path + '\\'
data_path = "E:\Faks\Zavrsni\Backups\FullDB3\Data\\"

# input_path = "E:\Faks\Zavrsni\\FullDB\Test Data\\" + scale_path + '\\'
# data_path = "E:\Faks\Zavrsni\\FullDB\Data\\"

loaded = {}
possible = {}

# Picking up the saved data of all known planes

planes = listdir(data_path)

for plane in planes:

    cameras = listdir(data_path + plane)

    for camera in cameras:

        file = open(data_path + plane + '\\' + camera + '\\' + 'normal.txt', "r")

        name = ''

        for line in file:

            if line[0] == '#':
                name = line.strip()
                possible[plane + name] = {}

            elif line[0] == '*':
                spl = line.split('->')

                curr_coeff = spl[0][1:]

                if curr_coeff in koefs_str:

                    possible[plane + name][curr_coeff] = float(spl[1])

        file.close()


# gdf = functions.calc(input_path, koefs, scale)

mean = {}
stdev = {}

current = ''
output = 'qNN: ' + str(q) + '\nDimensions: ' + str(len(koefs)) + '\npq: ' + str(koefs_str) + '\n\n'
wrong = 0
right = 0

file = open(input_path + 'normal.txt', "r")

for line in file:

    if line[0] == '#':
        current = line[1:]

    elif line[0] == '*':
        spl = line.split('->')
        loaded[spl[0][1:]] = float(spl[1])

    elif line.strip() == '':

        distance = {}

        for plane in possible:

            diff_sum = 0

            for coeff in possible[plane]:
                diff_sum += (possible[plane][coeff] - loaded[coeff])**2

            distance[plane] = sqrt(diff_sum)

        sorted_distances = sorted(distance.items(), key=lambda x: x[1])[0:q]

        closest = []

        for i in sorted_distances:
            closest.append(i[0].split('#')[0])

        counted = Counter(closest)

        result = counted.most_common()[0][0]

        if current.split('>')[0] == result:
            output += current + ' -> True ' + '(' + result + ')' + '\n'
            right += 1
        else:
            output += current + ' -> False ' + '(' + result + ')' + '\n'
            wrong += 1

        print(counted)
        print(current + '?' + result)
        loaded = {}

file.close()

output += '\n\nWrong: ' + str(wrong) + '\nRight: ' + str(right) + '\n\nRate: ' + str(right / (right + wrong))

print('Wrong: ' + str(wrong))

with open(input_path + 'results.txt', 'w+') as file:

    file.write(output)
