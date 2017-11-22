import preprocess 
import houghtransform as hf
import matplotlib.pyplot as plt
import numpy as np
import neuralnet 
import scrapedigit as sd
import solver as sudoku_solver

from PIL import Image

def main():
    CELL_H = 5
    CELL_W = 5
    image, input_image = preprocess.preprocess('data/sudoku7.png')
    points = hf.detect_gridlines(image)
    cropper = sd.cropper(points, image, input_image)

    # training_data, test_data = neuralnet.load_data() 
    # net = neuralnet.Network([CELL_H*CELL_W, 100, 10])
    # net.SGD(training_data, 300, 20, 0.05, lmbda=1.0, test_data=test_data)
    # net.save("digit_neuralnet.json")
    net = neuralnet.load("digit_neuralnet.json")

    # fig, axes = plt.subplots(nrows=9, ncols=9, figsize=(10, 10))
    # cntX = 0
    # cntY = 0

    # for row in axes:
    #     cntY = 0
    #     for col in row:
    #         lbX = min(points[cntX][cntY][1], points[cntX][cntY+1][1])
    #         ubX = max(points[cntX+1][cntY][1], points[cntX+1][cntY+1][1])
    #         lbY = min(points[cntX][cntY][0], points[cntX+1][cntY][0])
    #         ubY = max(points[cntX][cntY+1][0], points[cntX+1][cntY+1][0])
    #         col.imshow(input_image[lbX:ubX+1, lbY:ubY+1, :])
    #         cntY += 1
    #     cntX += 1
    # plt.show()

    fig, axes = plt.subplots(nrows=9, ncols=9, figsize=(10, 10))
    cntX = 0
    cntY = 0
    board = []

    for row in axes:
        cntY = 0
        board_row = []
        for col in row:
            old_cell = cropper.crop(cntX, cntY)
            old_cell = Image.fromarray(old_cell)
            # old_cell = Image.fromarray(input_image[lbX:ubX+1, lbY:ubY+1, :])
            # col.imshow(np.array(old_cell.convert("L"))/255.0)
            old_cell = old_cell.resize((CELL_W, CELL_H), Image.ANTIALIAS)
            old_cell = np.array(old_cell.convert("L"))
            cell = old_cell / 255.0
            predication = net.predict(np.reshape(cell, (CELL_H*CELL_W, 1)))
            #print(predication, end="")
            board_row.append(predication)
            col.imshow(cell)
            cntY += 1
        cntX += 1
        #print()
        board.append(board_row)
    
    # for i in range(len(board)):
    #     for j in range(len(board[i])):
    #         print(board[i][j], end='')
    #     print()
    solver = sudoku_solver.solver(board)
    solver.solve()
    plt.show()

if __name__ == "__main__":
    main()