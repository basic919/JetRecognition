from math import sqrt
from os import listdir


input_path = "E:\Faks\Zavrsni\FullDB\Data\\"
output_path = "E:\Faks\Zavrsni\FullDB\\normalization_data.txt"


mean = {}
stdev = {}
n = 0


planes = listdir(input_path)

for plane in planes:

    cameras = listdir(input_path + plane)

    for camera in cameras:

        if camera != "Top":
            continue

        file = open(input_path + plane + '\\' + camera + '\\' + 'coefficients.txt', "r")

        for line in file:

            if line[0] == "#":
                n += 1

            elif line[0] == "*":
                spl = line.split("->")
                if spl[0][1:] in mean:
                    mean[spl[0][1:]] += float(spl[1])
                else:
                    mean[spl[0][1:]] = float(spl[1])

        file.close()


for key in mean:
    mean[key] = mean[key] / n


for plane in planes:

    cameras = listdir(input_path + plane)

    for camera in cameras:

        file = open(input_path + plane + '\\' + camera + '\\' + 'coefficients.txt', "r")

        for line in file:

            if line[0] == "*":
                spl = line.split("->")
                if spl[0][1:] in stdev:
                    stdev[spl[0][1:]] += (float(spl[1]) - mean[spl[0][1:]])**2
                else:
                    stdev[spl[0][1:]] = (float(spl[1]) - mean[spl[0][1:]])**2

        file.close()


for key in stdev:
    stdev[key] = sqrt(stdev[key] / (n - 1))


output = ""

for key in mean:
    output += "$" + key + "->" + str(mean[key]) + "\n"
output += "\n"

for key in stdev:
    output += "&" + key + "->" + str(stdev[key]) + "\n"
output += "\n"

f = open(output_path, "w+")
f.write(output)
f.close()
