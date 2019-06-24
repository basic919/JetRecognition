import cv2
from numpy import fft


def largest_cont(conts):
    cont_ind = 0
    largest_area = 0

    if len(conts) > 0:
        i = 0
        for cnt in conts:
            area = cv2.contourArea(cnt)
            if area > largest_area:
                largest_area = area
                cont_ind = i
            i += 1
    return cont_ind


def fourier_dsc(conts, cont_ind):
    fdf = []

    pixels = len(conts[cont_ind])

    """for i in range(0, pixels):
        fdf.append(0)

        for j in range(0, pixels):
            fdf[i] += (conts[cont_ind][j][0][0] + 1j * conts[cont_ind][j][0][1]) * \
                      cmath.exp(-1j * ((2 * math.pi) / pixels) * (i * j))

            '''fdf[i] += (conts[0][j][0][0] + 1j * conts[0][j][0][1]) * (math.cos((2 * math.pi * i * j) / pixels) -
                                                                      1j * math.sin((2 * math.pi * i * j) / pixels))'''

        fdf[i] /= pixels"""

    coord = []
    for i in range(0, pixels):
        coord.append(conts[cont_ind][i][0][0] + 1j * conts[cont_ind][i][0][1])

    fdf = fft.fftn(coord)

    """for x in range(0, pixels):  # todo test
        if abs(fdf[x]) < 0.00000000000000000000000001:
            fdf[x] = 0"""

    # print('Fourier Descriptors:', len(fdf), '\n', fdf)

    return fdf


def granlundf(fds, koefs):
    dpq = {}
    tekst = ''
    m = len(fds)

    for koef in koefs:

        p = koef[0]
        q = koef[1]

        spremi = ((fds[p+1] ** q) * (fds[m + 1 - q] ** p)) / (fds[1] ** (p + q))
        if abs(spremi) < (10 ** (-25)):
            spremi = 0
        dpq[str(koef)] = spremi

        tekst += "*(" + str(p) + "," + str(q) + ")" + "->" + str(abs(spremi)) + "\n"
        print("(", p, ",", q, ")", "GFD: ", abs(spremi))

    # print('Granlund:\n', dpq)

    return dpq, tekst


def calc(im_path, koefs, scale):

    im = cv2.imread(im_path)

    height, width, channels = im.shape

    im = cv2.resize(im, (int(width * scale), int(height * scale)))

    im = cv2.blur(im, (3, 3))

    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    imgray = ~imgray
    ret, thresh = cv2.threshold(imgray, 170, 255, cv2.THRESH_BINARY)

    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # print('Number of contours #1:', len(contours))

    '''cv2.drawContours(im, contours, -1, (0, 0, 255), 2)
    cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
    cv2.imshow('Display', im)
    cv2.waitKey()'''

    fd = fourier_dsc(contours, largest_cont(contours))

    dpq, gdf = granlundf(fd, koefs)

    # crtanje

    '''window = pyglet.window.Window(width=int(width), height=int(height))

    x = 0

    cont_id = largest_cont(contours)
    pixels_n = len(contours[cont_id])

    def update(dt):
        nonlocal x
        nonlocal pixels_n
        if x < pixels_n - 1:
            x += 1

    pyglet.clock.schedule_interval(update, 1 / 60)

    @window.event
    def on_draw():
        nonlocal height
        nonlocal cont_id

        pyglet.graphics.draw(1, pyglet.gl.GL_POINTS, ('v2i', (contours[cont_id][x][0][0],
                                                              height - contours[cont_id][x][0][1])))

    pyglet.app.run()'''

    return gdf
