import functions
from os import listdir
import json

'''DESCRIPTION SAVER BACKUP!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'''


koefs = [[1, 2], [1, 3], [1, 4], [2, 2], [2, 3], [3, 2], [3, 3], [4, 2], [4, 3], [5, 2], [5, 3], [6, 2],
         [6, 3], [7, 2], [7, 3], [10, 2], [12, 2], [14, 2], [16, 2], [17, 2], [19, 2], [22, 2], [31, 2]]

scale = 1.0

input_path = "E:\Faks\Zavrsni\FullDB\Planes\\"
output_path = "E:\Faks\Zavrsni\FullDB\Data\\"

planes = listdir(input_path)


for plane in planes:

    if plane not in ["Dassault Rafale", "General Dynamics F-16 Fighting Falcon", "Eurofighter Typhoon"]:
        continue

    cameras = listdir(input_path + plane)

    for camera in cameras:

        if camera != "Top":
            continue

        files = listdir(input_path + plane + "\\" + camera)

        for file in files:
            if int(file.split(".")[0][-2:]) > 34:
                continue

            view = input_path + plane + "\\" + camera + "\\" + file

            gdf = functions.calc(view, koefs, scale)

            output = "#" + file.split(".")[0] + " [" + str(scale) + "]\n" + gdf + "\n"

            with open(output_path + plane + "\\" + camera + "\\" + "coefficients.txt", "a+") as f:
                f.write(output)

            print("Entered: " + plane + " " + file)


print(planes)
