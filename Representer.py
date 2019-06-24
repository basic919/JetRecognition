from os import listdir

input_path = "E:\Faks\Zavrsni\FullDB\Data\\"

planes = listdir(input_path)

for plane in planes:

    cameras = listdir(input_path + plane)

    for camera in cameras:

        file = open(input_path + plane + '\\' + camera + '\\' + 'normal.txt', "r")

        mean = {}
        n = 0
        output = ''

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

        for key in mean:
            output += key + '->' + str(mean[key]) + '\n'

        with open(input_path + plane + '\\' + camera + '\\' + 'represent.txt', 'w+') as rep:

            rep.write(output)
