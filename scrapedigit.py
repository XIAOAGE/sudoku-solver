import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from collections import deque

class cropper(object):
    def __init__(self, points, image, input_image):
        self.points = points
        self.image = image
        self.input_image = input_image

    def bfs(self, x, y, lbX, ubX, lbY, ubY):
        X_PERCENT = 1
        Y_PERCENT = 1
        dx = [-1, 1, 0, 0, -1, 1, -1, 1]
        dy = [0, 0, 1, -1, 1, -1, -1, 1]
        input_image = self.input_image
        image = np.array(Image.fromarray(input_image).convert("L"))
        height, width = image.shape
        #print(lbX, ubX, lbY, ubY, height, width)
        flag = np.zeros((height, width))
        start = (-1, -1)
        d = deque()
        d.append((x, y))
        flag[x, y] = 1
        while d:
            curX, curY = d.popleft()
            if image[curX, curY] != 255:
                start = (curX, curY)
                break
            for i in range(len(dx)):
                nxtX = curX + dx[i]
                nxtY = curY + dy[i]
                if nxtX<int(lbX*X_PERCENT) or nxtY<int(lbY*X_PERCENT) or nxtX>int(ubX*Y_PERCENT) or nxtY>int(ubY*Y_PERCENT): 
                    continue
                if flag[nxtX, nxtY] != 0: 
                    continue
                flag[nxtX, nxtY] = 2
                d.append((nxtX, nxtY))

        d = deque()
        x, y = start
        if x==-1 and y==-1:
            ret = np.zeros((height, width))
            ret.fill(255.0)
            return ret
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
                if nxtX<lbX or nxtY<lbY or nxtX>ubX or nxtY>ubY: 
                    continue
                if flag[nxtX, nxtY] == 1 or image[nxtX, nxtY]==255: 
                    continue
                minX = min(minX, nxtX)
                maxX = max(maxX, nxtX)
                minY = min(minY, nxtY)
                maxY = max(maxY, nxtY)
                flag[nxtX, nxtY] = 1
                d.append((nxtX, nxtY))
        #print(lbX, minX, lbY, minY, ubX, maxX, ubY, maxY)
        # print(minX, maxX, minY, maxY)
        return input_image[minX:maxX+1, minY:maxY+1]
          

    def crop(self, cntX, cntY):
        points = self.points
        input_image = self.input_image
        lbX = min(points[cntX][cntY][1], points[cntX][cntY+1][1])
        ubX = max(points[cntX+1][cntY][1], points[cntX+1][cntY+1][1])
        lbY = min(points[cntX][cntY][0], points[cntX+1][cntY][0])
        ubY = max(points[cntX][cntY+1][0], points[cntX+1][cntY+1][0])
        ret_image = self.bfs(int((lbX+ubX)/2), int((lbY+ubY)/2), lbX, ubX, lbY, ubY)
        return ret_image
        # lbX = lbX + int((ubX-lbX)*0.2)
        # ubX = ubX - int((ubX-lbX)*0.3)
        # lbY = lbY + int((ubY-lbY)*0.32)
        # ubY = ubY - int((ubY-lbY)*0.44)

        #print(net.predict(np.reshape(cell, (CELL_H*CELL_W, 1))), end='')
        # distX = ubX-lbX+1
        # distY = ubY-lbY+1
        # deltaX = CELL_H-distX
        # deltaY = CELL_W-distY
        # cell = np.zeros((CELL_H,distY))
        # cell.fill(255)

        # lsX = deltaX/2.0
        # if lsX>=0: 
        #     lsX = int(lsX)
        #     rsX = distX + lsX
        #     cell[lsX:rsX, :] = old_cell 
        # else:
        #     lsX = abs(int(lsX))
        #     rsX = lsX + CELL_H
        #     cell = old_cell[lsX:rsX, :]

        # old_cell = cell
        # cell = np.zeros((CELL_H, CELL_W))
        # cell.fill(255)

        # usY = deltaY/2.0
        # if usY>=0: 
        #     usY = int(usY)
        #     bsY = distY + usY
        #     cell[:,usY:bsY] = old_cell 
        # else:
        #     usY = abs(int(usY))
        #     bsY = usY + CELL_W
        #     cell = old_cell[:,usY:bsY]
        
        # col.imshow(cell)
        # cell /= 255.0