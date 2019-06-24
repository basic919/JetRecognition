from os import listdir
import functions
from math import sqrt
from collections import Counter


koefs = [[1, 2], [1, 3], [1, 4], [2, 2], [3, 2], [4, 2], [6, 2]]

koefs_str = ['(1,2)', '(1,3)', '(1,4)', '(2,2)', '(3,2)', '(4,2)', '(6,2)']

scale = 1.0

q = 7

model = "Dassault Rafale"

input_path = 'E:\Faks\Zavrsni\FullDB\Test Planes\Saab JAS 39 Gripen\Side\side46.jpg'
data_path = "E:\Faks\Zavrsni\FullDB\Data\\"
normalization_path = 'E:\Faks\Zavrsni\FullDB\\normalization_data.txt'

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


gdf = functions.calc(input_path, koefs, scale)

mean = {}
stdev = {}

with open(normalization_path, 'r') as file:

    for line in file:

        if line[0] == '$':
            spl = line.split('->')
            mean[spl[0][1:]] = float(spl[1])

        elif line[0] == '&':
            spl = line.split('->')
            stdev[spl[0][1:]] = float(spl[1])


for line in gdf.splitlines():

    if line[0] == '*':
        spl = line.split('->')
        loaded[spl[0][1:]] = float(spl[1])

# Normalizing calculated values
for l in loaded:
    loaded[l] = (loaded[l] - mean[l]) / stdev[l]

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

print(counted)
print(result)
