from tkinter import *
import functions
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from math import sqrt
from collections import Counter
from os import listdir


im_path = 'load.jpg'


def load_img():
    global im_path
    global im1
    global imL1

    im_path = askopenfilename()

    if im_path != '':

        im1 = Image.open(im_path)
        im1.thumbnail((588, 337))
        render = ImageTk.PhotoImage(im1)
        imL1.configure(image=render)
        imL1.image = render


# Classification is done here

def classify(t1, e1, e2):
    koefs = [[2, 2], [2, 3], [3, 2], [5, 2], [4, 3]]
    koefs_str = []
    data_path = "FullDB\Data\\"
    normalization_path = 'FullDB\\normalization_data.txt'

    loaded = {}
    possible = {}

    for koef in koefs:
        koefs_str.append('(' + str(koef[0]) + ',' + str(koef[1]) + ')')

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

    if e1 != '':
        q = int(e1.strip())

    else:
        q = 1

    if e2 != '':
        scale = float(e2.strip())

    else:
        scale = 1.0

    gdf = functions.calc(im_path, koefs, scale)

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
            diff_sum += (possible[plane][coeff] - loaded[coeff]) ** 2

        distance[plane] = sqrt(diff_sum)

    sorted_distances = sorted(distance.items(), key=lambda x: x[1])[0:q]

    closest = []

    for i in sorted_distances:
        closest.append(i[0].split('#')[0])

    counted = Counter(closest)

    result = counted.most_common()[0][0]

    print(counted)
    print(result)
    tekst1 = 'Nearest Neighbors ' + str(counted)
    tekst1 += "\n\nResult: " + result

    t1.configure(state="normal")
    t1.delete('1.0', END)
    t1.insert(INSERT, tekst1)
    t1.configure(state="disabled")


# GUI creation

top = Tk()
top.title("Jet Recognition")


frame = Frame(top)
frame.pack()

pathframe = Frame(frame)
pathframe.pack(side=TOP)

bottomframe = Frame(frame)
bottomframe.pack(side=BOTTOM)


centerframe = Frame(bottomframe)
centerframe.pack(side=TOP)

bottomleftframe = Frame(bottomframe)
bottomleftframe.pack(side=LEFT)

path_frame1 = Frame(pathframe)
path_frame1.pack(side=TOP)


scale_frame = Frame(pathframe)
scale_frame.pack(side=RIGHT)

center_left = Frame(centerframe)
center_left.pack(side=LEFT)
center_right = Frame(centerframe)
center_right.pack(side=RIGHT)


L1 = Label(path_frame1, text="Number of neighbors: ")
L1.pack(side=LEFT)

E1 = Entry(path_frame1, bd=2)
E1.pack(side=RIGHT)


L2 = Label(scale_frame, text="Scale: ")
L2.pack(side=LEFT)

E2 = Entry(scale_frame, bd=2)
E2.pack(side=RIGHT)

im1 = Image.open(im_path)
im1.thumbnail((588, 337))
render1 = ImageTk.PhotoImage(im1)

imL1 = Label(center_left, image=render1)
imL1.pack(side=TOP)

load_button1 = Button(center_left, text="Load Image", command=lambda: load_img())
load_button1.pack(side=BOTTOM)


text1 = Text(bottomleftframe, wrap=WORD)
text1.pack(side=LEFT)
text1.configure(state="disabled")


B = Button(frame, text="Recognize", command=lambda: classify(text1, E1.get(), E2.get()))
B.pack(side=BOTTOM)


top.mainloop()
