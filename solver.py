
class solver(object):
    def __init__(self, board):
        self.board = board
    
    def preprocess(self):
        board = self.board
        row = []
        for i in range(9):
            num = 0
            for j in range(9):
                if board[i][j]!=0:
                    num = num + (1<<board[i][j])
            row.append(num)
        
        col = []
        for i in range(9):
            num = 0
            for j in range(9):
                if board[j][i]!=0:
                    num = num + (1<<board[j][i])
            col.append(num)

        group = []
        for i in range(3):
            i = i*3
            for j in range(3):
                j = j*3
                num = 0
                for k in range(3):
                    k = i+k
                    for p in range(3):
                        p = j+p
                        if board[k][p] !=0:
                            num = num + (1<<board[k][p])
                group.append(num)

        self.row = row
        self.col = col
        self.group = group
    
    def dfs(self, idx):
        if idx==81:
            return True
        x = int(idx/9.0)
        y = int(idx%9.0)
        groupID = int(x/3.0) * 3 + int(y/3.0)
        if self.board[x][y] != 0:
            return self.dfs(idx+1)
        ret = False
        for i in range(9):
            i = i + 1
            if (1<<i & self.row[x]) !=0 or (1<<i & self.col[y])!=0 or (1<<i & self.group[groupID])!=0:
                continue
            self.board[x][y] = i
            self.row[x] += 1<<i
            self.col[y] += 1<<i
            self.group[groupID] += 1<<i
            if self.dfs(idx+1): 
                ret = True
                break
            self.board[x][y] = 0
            self.row[x] -= 1<<i
            self.col[y] -= 1<<i
            self.group[groupID] -= 1<<i
        return ret

    def solve(self):
        self.preprocess()
        self.dfs(1)  
        board = self.board
        for i in range(len(board)):
            for j in range(len(board[i])):
                print(board[i][j], end='')
            print()

# board = [
#     [5, 3, 0, 0, 7, 0, 0, 0, 0],
#     [6, 0, 0, 1, 9, 5, 0, 0, 0],
#     [0, 9, 8, 0, 0, 0, 0, 6, 0],
#     [8, 0, 0, 0, 6, 0, 0, 0, 3],
#     [4, 0, 0, 8, 0, 3, 0, 0, 1],
#     [7, 0, 0, 0, 2, 0, 0, 0, 6],
#     [0, 6, 0, 0, 0, 0, 2, 8, 0],
#     [0, 0, 0, 4, 1, 9, 0, 0, 5],
#     [0, 0, 0, 0, 8, 0, 0, 7, 9]
# ]

# board2 = [
#     [2,9,5,7,4,3,8,6,1],
#     [4,3,2,8,6,5,9,2,7],
#     [8,7,6,1,9,2,5,4,3],
#     [3,8,7,4,5,9,2,1,6],
#     [6,1,2,3,8,7,4,9,5],
#     [5,4,9,2,1,0,7,3,8],
#     [7,6,3,5,3,4,1,8,9],
#     [9,2,8,6,7,1,3,5,4],
#     [1,5,4,9,3,8,6,7,2]
# ]
# solver = solver(board)
# solver.solve()
    