import glob
import numpy as np

from PIL import Image
from collections import deque

def shrink_helper(image):
    dx = [-1, 1, 0, 0, -1, 1, -1, 1]
    dy = [0, 0, 1, -1, 1, -1, -1, 1]
        
    height, width = image.shape
    x = int(height/2)
    y = int(width/2)
    flag = np.zeros((height, width))
    start = (0,0)
    d = deque()
    d.append((x, y))
    flag[x, y] = 1
    while d:
        curX, curY = d.popleft()
        if not image[curX, curY]:
            start = (curX, curY)
            break
        for i in range(len(dx)):
            nxtX = curX + dx[i]
            nxtY = curY + dy[i]
            if nxtX<0 or nxtY<0 or nxtX>=height or nxtY>=width: 
                continue
            if flag[nxtX, nxtY] != 0: 
                continue
            flag[nxtX, nxtY] = 2
            d.append((nxtX, nxtY))

    d = deque()
    x, y = start
    d.append((x, y))
    minX = x
    maxX = x
    minY = y
    maxY = y

    while d:
        curX, curY = d.popleft()
        for i in range(len(dx)):
            nxtX = curX + dx[i]
            nxtY = curY + dy[i]
            if nxtX<0 or nxtY<0 or nxtX>=height or nxtY>=width: 
                continue
            if flag[nxtX, nxtY] == 1 or image[nxtX, nxtY]: 
                continue
            minX = min(minX, nxtX)
            maxX = max(maxX, nxtX)
            minY = min(minY, nxtY)
            maxY = max(maxY, nxtY)
            flag[nxtX, nxtY] = 1
            d.append((nxtX, nxtY))
    return image[minX:maxX+1, minY:maxY+1]

def shrink_image(file_path):
    for image_name in glob.glob(file_path):
        image = np.array(Image.open(image_name))
        image = shrink_helper(image)
        print(image.shape)
        image = Image.fromarray(image)
        image.save(image_name)
    

# for i in range(9):
#     i = i+1
#     shrink_image("data/30x20/Set1/"+str(i)+"/*")
#     shrink_image("data/30x20/Set2/"+str(i)+"/*")
#     shrink_image("data/60x40/Set1/"+str(i)+"/*")
#     shrink_image("data/60x40/Set2/"+str(i)+"/*")