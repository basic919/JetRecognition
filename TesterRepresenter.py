from os import listdir
import functions
from math import sqrt


koefs = [[14, 2], [10, 2], [2, 2], [10, 2], [1, 2], [1, 4], [7, 2]]

koefs_str = ['(14,2)', '(10,2)', '(2,2)', '(10,2)', '(1,2)', '(1, 4)', '(7, 2)']

scale = 1.0

model = "Sukhoi Su-34"

input_path = 'E:\Faks\Zavrsni\FullDB\Planes\\' + model + '\\Top\\top37.jpg'
data_path = "E:\Faks\Zavrsni\FullDB\Data\\"
normalization_path = 'E:\Faks\Zavrsni\FullDB\\normalization_data.txt'

loaded = {}
possible = {}

# Picking up the saved data of all known planes

planes = listdir(data_path)

for plane in planes:

    possible[plane] = {}

    cameras = listdir(data_path + plane)

    for camera in cameras:

        file = open(data_path + plane + '\\' + camera + '\\' + 'represent.txt', "r")

        for line in file:

            spl = line.split('->')

            if spl[0] in koefs_str:

                possible[plane][spl[0]] = float(spl[1])

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


result = min(distance, key=distance.get)

print(distance)
print(result)
