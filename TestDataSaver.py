import functions
from os import listdir
import os


koefs = [[1, 2], [1, 3], [1, 4], [2, 2], [2, 3], [3, 2], [3, 3], [4, 2], [4, 3], [5, 2], [5, 3], [6, 2],
         [6, 3], [7, 2], [7, 3], [10, 2], [12, 2], [14, 2], [16, 2], [17, 2], [19, 2], [22, 2], [31, 2]]

scale = 1.0

scale_path = 'scale' + str(int(scale * 100))

input_path = "E:\Faks\Zavrsni\\FullDB\Test Planes\\"
output_path = "E:\Faks\Zavrsni\\FullDB\Test Data\\" + scale_path + '\\'


planes = listdir(input_path)

for plane in planes:

    cameras = listdir(input_path + plane)

    for camera in cameras:

        files = listdir(input_path + plane + "\\" + camera)

        skippable = []

        if os.path.isfile(output_path + "stored.txt"):
            with open(output_path + "stored.txt", "r") as stored:
                for line in stored:
                    skippable.append(line.strip())

        for file in files:

            if "#" + plane + '>' + file + " [" + str(scale) + ']' in skippable:

                continue

            else:
                with open(output_path + "stored.txt", "a+") as stored:
                    stored.write("#" + plane + '>' + file + " [" + str(scale) + ']\n')

                view = input_path + plane + "\\" + camera + "\\" + file

                gdf = functions.calc(view, koefs, scale)

                output = "#" + plane + '>' + file.split(".")[0] + " [" + str(scale) + "]\n" + gdf + "\n"

                with open(output_path + "coefficients.txt", "a+") as f:
                    f.write(output)

            print("Entered: " + plane + " " + file)


print(planes)


norm = open("E:\Faks\Zavrsni\FullDB\\normalization_data.txt", "r")

mean = {}
stdev = {}

for line in norm:
    if line[0] == "$":
        spl = line.split('->')
        mean[spl[0][1:]] = spl[1]

    elif line[0] == "&":
        spl = line.split('->')
        stdev[spl[0][1:]] = spl[1]


# normalization

output = ''

file = open(output_path + 'coefficients.txt', "r")

for line in file:

    if line[0] == "*":
        spl = line.split("->")

        save = (float(spl[1]) - float(mean[spl[0][1:]])) / float(stdev[spl[0][1:]])

        output += spl[0] + '->' + str(save) + '\n'

    else:
        output += line

file.close()

with open(output_path + 'normal.txt', "w+") as normal:

    normal.write(output)
