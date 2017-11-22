import matplotlib.pyplot as plt
import numpy as np

from skimage.filters import threshold_adaptive
from PIL import Image
from collections import deque

def preprocess(pic_name):
    input_image = np.array(Image.open(pic_name).convert("L"))
    image = input_image
    block_size = 35
    binary_adaptive = threshold_adaptive(image, block_size, offset=10)

    # plt.imshow(binary_adaptive)
    # plt.show()
    # print(binary_adaptive.shape)
    binary_adaptive, input_image = largest_component(binary_adaptive, input_image)
    # binary_adaptive, input_image = find_border(binary_adaptive, input_image)
    # plt.imshow(binary_adaptive)
    # plt.show()
    plt.imshow(binary_adaptive)
    #plt.show()
    return (binary_adaptive, input_image)

def largest_component(image, input_image):
    max_area = 0
    count = 1
    flag = np.zeros(image.shape)

    dx = [0, 0, 1, -1]
    dy = [1, -1, 0, 0]
    width, height = image.shape

    ret = ()

    for x in range(width):
        for y in range(height):
            if image[x, y] or flag[x, y]!=0: 
                continue
            d = deque()
            d.append((x, y))
            flag[x, y] = count
            minX = x
            minY = y
            maxX = x
            maxY = y
            while d:
                curX, curY = d.popleft()
                minX = min(minX, curX)
                minY = min(minY, curY)
                maxX = max(maxX, curX)
                maxY = max(maxY, curY)
                for i in range(len(dx)):
                    nxtX = curX + dx[i]
                    nxtY = curY + dy[i]
                    if nxtX <0 or nxtX>=width or nxtY<0 or nxtY>=height: 
                        continue
                    if image[nxtX, nxtY] or flag[nxtX, nxtY]!=0: 
                        continue
                    flag[nxtX, nxtY] = count
                    d.append((nxtX, nxtY))
            area = (maxX-minX)*(maxY-minY)
            if(max_area<=area): 
                ret = count
                max_area = area
                ret = (minX, minY, maxX, maxY)
            count = count + 1
    minX, minY, maxX, maxY = ret
    return (image[minX:maxX+1, minY:maxY+1], input_image[minX:maxX+1, minY:maxY+1])

def find_border(image, input_image):
    ret = 0
    row, col = image.shape
    
    lbCol = 0
    cnt = 0
    for i in range(1, int(col/2)):
        tmp = 0
        for j in range(row):
            if image[j, i]: 
                tmp = tmp + 1
        if cnt <= tmp:
            lbCol = i
            cnt = tmp

    rbCol = 0
    cnt = 0
    for i in range(int(col/2), col):
        tmp = 0
        for j in range(row):
            if image[j, i]: 
                tmp = tmp + 1
        if cnt < tmp:
            rbCol = i
            cnt = tmp

    lbRow = 0
    cnt = 0
    for i in range(1, int(row/2)):
        tmp = 0
        for j in range(col):
            if image[i, j]: 
                tmp = tmp + 1
        if cnt <= tmp:
            lbRow = i
            cnt = tmp
    
    rbRow = 0
    cnt = 0
    for i in range(int(row/2), row):
        tmp = 0
        for j in range(col):
            if image[i, j]: 
                tmp = tmp + 1
        if cnt < tmp:
            rbRow = i
            cnt = tmp
    
    return (image[lbRow:rbRow+1, lbCol:rbCol+1], input_image[lbRow:rbRow+1, lbCol:rbCol+1])
