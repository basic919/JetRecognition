import functions
from os import listdir
import os


koefs = [[1, 2], [1, 3], [1, 4], [2, 2], [2, 3], [3, 2], [3, 3], [4, 2], [4, 3], [5, 2], [5, 3], [6, 2],
         [6, 3], [7, 2], [7, 3], [10, 2], [12, 2], [14, 2], [16, 2], [17, 2], [19, 2], [22, 2], [31, 2]]

scale = 1.0

input_path = "E:\Faks\Zavrsni\FullDB\Planes\\"
output_path = "E:\Faks\Zavrsni\FullDB\Data\\"

planes = listdir(input_path)


for plane in planes:

    cameras = listdir(input_path + plane)

    for camera in cameras:

        files = listdir(input_path + plane + "\\" + camera)

        skippable = []

        if os.path.isfile(output_path + plane + "\\" + camera + "\\" + "stored.txt"):
            with open(output_path + plane + "\\" + camera + "\\" + "stored.txt", "r") as stored:
                for line in stored:
                    skippable.append(line.strip())

        for file in files:

            if "#" + file + " [" + str(scale) + ']' in skippable:

                continue

            else:
                with open(output_path + plane + "\\" + camera + "\\" + "stored.txt", "a+") as stored:
                    stored.write("#" + file + " [" + str(scale) + ']\n')

                view = input_path + plane + "\\" + camera + "\\" + file

                gdf = functions.calc(view, koefs, scale)

                output = "#" + file.split(".")[0] + " [" + str(scale) + "]\n" + gdf + "\n"

                with open(output_path + plane + "\\" + camera + "\\" + "coefficients.txt", "a+") as f:
                    f.write(output)

            print("Entered: " + plane + " " + file)


print(planes)
