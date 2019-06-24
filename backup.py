'''import functions # DESCRIPTION SAVER BACKUP
from os import listdir
import h5py


koefs = [[1, 2], [1, 3], [1, 4], [2, 2], [2, 3], [3, 2], [3, 3], [4, 2], [4, 3], [5, 2], [5, 3], [6, 2],
         [6, 3], [7, 2], [7, 3], [10, 2], [12, 2], [14, 2], [16, 2], [17, 2], [19, 2], [22, 2], [31, 2]]

scale = 1.0

input_path = "E:\Faks\Zavrsni\FullDB\Planes\\"
output_path = "E:\Faks\Zavrsni\FullDB\Data\\"

planes = listdir(input_path)


with h5py.File(output_path + 'dset.hdf5', 'a') as f:

    for plane in planes:

        if plane not in ["Dassault Rafale", "General Dynamics F-16 Fighting Falcon", "Eurofighter Typhoon"]:
            continue

        if plane not in f.keys():
            f.create_group(plane)

        cameras = listdir(input_path + plane)

        for camera in cameras:

            if camera != "Top":
                continue

            if camera not in f[plane].keys():
                f.create_group(plane + '/' + camera)

            files = listdir(input_path + plane + "\\" + camera)

            for file in files:
                if int(file.split(".")[0][-2:]) > 34:   # privremeno
                    continue

                if file not in f[plane + '/' + camera].keys():
                    f[plane + '/' + camera].create_dataset(file, (23, 3))   # TODO: sad dodat stvari u dataset i obrisat json sranja

                file_path = input_path + plane + "\\" + camera + "\\" + file

                gdf = functions.calc(file_path, koefs, scale)

                json_entry = {file.split(".")[0]: [{"scale": scale, "gdf": gdf}]}

                output = "#" + file.split(".")[0] + " [" + str(scale) + "]\n" + gdf + "\n"

                with open(output_path + plane + "\\" + camera + "\\" + "data.json'" 'a+') as outfile:
                    json.dump(json_entry, outfile)

                print("Entered: " + plane + " " + file)


print(planes)'''
