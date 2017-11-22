import numpy as np
import math
import matplotlib.pyplot as plt

from skimage.transform import hough_line

def detect_gridlines(image):
    ERROR_CONST = 25.0

    height, width = image.shape
    image = np.invert(image)
    h, theta, d = hough_line(image)

    row, col = h.shape
    
    lst = []
    for i in range(row):
        for j in range(col):
            if h[i, j]>0:
                lst.append((h[i,j], d[i], theta[j]))
    
    lst.sort()
    horizontal = []
    vertical = []
    cnt_h = 0
    cnt_v = 0
    error_vertical = width / ERROR_CONST
    error_horizontal = height / ERROR_CONST

    for i in range(len(lst)-1, 0, -1):
        if abs(lst[i][2]-0) <= 0.01 and cnt_v<10:
            flag = True
            for j in range(len(vertical)):
                if abs(vertical[j][0]-lst[i][1]) <= error_vertical:
                    flag = False
                    break
            if flag:
                vertical.append((lst[i][1], lst[i][2]))
                cnt_v = cnt_v + 1
        elif (lst[i][2]==theta[0] or lst[i][2]==theta[179]) and cnt_h<10:
            flag = True
            for j in range(len(horizontal)):
                if abs(horizontal[j][0]-lst[i][1]) <= error_horizontal:
                    flag = False
                    break
            if flag:
                horizontal.append((lst[i][1], lst[i][2]))
                cnt_h = cnt_h + 1

    # print(cnt_h, cnt_v)
    # for i in range(cnt_h):
    #     print(horizontal[i])

    # for i in range(cnt_v):
    #     print(vertical[i])
    return detect_cells(horizontal, vertical, image)

def detect_cells(horizontal, vertical, image):
    plt.imshow(image)
    height, width = image.shape
    error_horizontal = []
    for i in range(len(horizontal)):
        error_horizontal.append(abs(math.sin(horizontal[i][1])))
    
    points = []
    for i in range(len(vertical)):
        line_points = []
        y = 0
        while y < height:
            x = int((vertical[i][0] - y * math.sin(vertical[i][1])) / math.cos(vertical[i][1]))
            for j in range(len(horizontal)):
                p = x*math.cos(horizontal[j][1]) + y*math.sin(horizontal[j][1])
                delta_p = abs(horizontal[j][0]-p)
                if delta_p <= error_horizontal[j]:
                    line_points.append((min(x, width-1), y))
                    y += 1
                    break
            y += 1
        # for k in range(len(line_points)):
        #     print(line_points[k])
        # print(len(line_points))
        # print("=============")
        points.append(line_points)
    
    points = [[points[j][i] for j in range(10)] for i in range(10)]
    for i in range(10):
        points[i].sort()
    # print(points)
    return points
    
    