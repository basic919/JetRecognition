from os import listdir

input_path = "E:\Faks\Zavrsni\FullDB\Data\\"
output_path = "E:\Faks\Zavrsni\FullDB\\"


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

planes = listdir(input_path)

for plane in planes:

    cameras = listdir(input_path + plane)

    for camera in cameras:

        output = ''

        file = open(input_path + plane + '\\' + camera + '\\' + 'coefficients.txt', "r")

        for line in file:

            if line[0] == "*":
                spl = line.split("->")

                save = (float(spl[1]) - float(mean[spl[0][1:]])) / float(stdev[spl[0][1:]])

                output += spl[0] + '->' + str(save) + '\n'

            else:
                output += line

        file.close()

        with open(input_path + plane + '\\' + camera + '\\' + 'normal.txt', "w+") as normal:

            normal.write(output)
