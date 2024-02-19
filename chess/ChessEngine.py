class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.whitePiece = ["wR", "wN", "wB", "wQ", "wp"]
        self.blackPiece = ["bR", "bN", "bB", "bQ", "bp"]
        self.whiteMove = True
        # self.opponent = self.blackPiece
        self.moveLog = []
        self.validMoves = []

        self.pieceMoves = {
            "wP": self.pawnMove, "bP": self.pawnMove,
            "wR": self.rookMove, "bR": self.rookMove,
            "wB": self.bishopMove, "bB": self.bishopMove,
            "wN": self.knightMove, "bN": self.knightMove,
            "wQ": self.queenMove, "bQ": self.queenMove
        }

    def makeMove(self, move):
        if move.pieceMoved != "--" and self.isCorrectPiece(move):
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            if move.pieceCaptured != "--":
                move.soundEffect("capture")
            else:
                move.soundEffect("move-self")
            self.moveLog.append(move)
            self.whiteMove = not self.whiteMove
            # defining who,s the opponent
            # if self.whiteMove == True:
            #     self.opponent = self.blackPiece
            # else:
            #     self.opponent = self.whitePiece

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteMove = not self.whiteMove



    def isValidMove(self, x, y, opponent):
        if(x < 0 or x >= 8 or y < 0 or y >= 8 ):
            return False

        piece = self.board[x][y]
        return piece == "--" or (piece in opponent)

    def isValidPawnMove(self, x, y, opponent, condition):
        if (x < 0 or x >= 8 or y < 0 or y >= 8):
            return False

        piece = self.board[x][y]
        if condition == 1 and piece == "--":
            return True
        elif condition == 2 and piece in opponent:
            return True
        else:
            return False

    def isCorrectPiece(self,move):
        if self.whiteMove == True:
            if move.pieceMoved in self.whitePiece:
                return True
            else:
                return False
        elif self.whiteMove == False:
            if move.pieceMoved in self.blackPiece:
                return True
            else:
                return False

    def queenMove(self, move):
        self.validMoves = []
        dx = [1, -1, 0, 0, 1, -1, 1, -1]
        dy = [0, 0, 1, -1, 1, -1, -1, 1]
        if self.whiteMove == True:
            self.opponent = self.blackPiece
        else:
            self.opponent = self.whitePiece

        for i in range(len(dx)):
            x = dx[i] + move.startRow
            y = dy[i] + move.startCol

            while(self.isValidMove(x,y,self.opponent)):
                self.validMoves.append((x,y))

                if self.board[x][y] != "--":
                    break

                x += dx[i]
                y += dy[i]
        return self.validMoves

    def rookMove(self, move):
        self.validMoves = []
        dx = [1, -1, 0, 0]
        dy = [0, 0, 1, -1]
        if self.whiteMove == True:
            self.opponent = self.blackPiece
        else:
            self.opponent = self.whitePiece

        for i in range(len(dx)):
            x = dx[i] + move.startRow
            y = dy[i] + move.startCol

            while(self.isValidMove(x,y,self.opponent)):
                self.validMoves.append((x,y))

                if self.board[x][y] != "--":
                    break

                x += dx[i]
                y += dy[i]

        return self.validMoves

    def bishopMove(self, move):
        self.validMoves = []
        dx = [1, -1, 1, -1]
        dy = [1, -1, -1, 1]
        if self.whiteMove == True:
            self.opponent = self.blackPiece
        else:
            self.opponent = self.whitePiece

        for i in range(len(dx)):
            x = dx[i] + move.startRow
            y = dy[i] + move.startCol

            while(self.isValidMove(x,y,self.opponent)):
                self.validMoves.append((x,y))

                if self.board[x][y] != "--":
                    break

                x += dx[i]
                y += dy[i]

        return self.validMoves

    def knightMove(self, move):
        self.validMoves = []
        dx = [-2, -1, 1, 2, -2, -1, 1, 2]
        dy = [-1, -2, -2, -1, 1, 2, 2, 1]
        if self.whiteMove == True:
            self.opponent = self.blackPiece
        else:
            self.opponent = self.whitePiece

        for i in range(len(dx)):
            x = dx[i] + move.startRow
            y = dy[i] + move.startCol
            if self.isValidMove(x,y,self.opponent):
                self.validMoves.append((x,y))

        # return self.validMoves

    def pawnMove(self, move):
        self.validMoves = []
        dy = [1, 0, -1]
        dx = [-1, -1, -1]
        if self.whiteMove == True:
            self.opponent = self.blackPiece
        else:
            self.opponent = self.whitePiece

        for i in range(len(dx)):
            x = dx[i] + move.startRow
            y = dy[i] + move.startCol

            if self.whiteMove and move.startRow == 6:
                count = 2
            elif not self.whiteMove and move.startRow == 1:
                count = 2
            else:
                count = 1

            if i % 2 != 0:
                condition = 1
            else:
                condition = 2
                count = 1

            while self.isValidPawnMove(x, y, self.opponent, condition) and count > 0:
                self.validMoves.append((x,y))
                x = dx[i] + x
                y = dy[i] + y
                count -= 1

        return self.validMoves
    





class move:

    def __init__(self, startSQ, endSQ , board):
        self.startRow = startSQ[0]
        self.startCol = startSQ[1]
        self.endRow = endSQ[0]
        self.endCol = endSQ[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

    def soundEffect(self, opperation):
        from pygame import mixer
        mixer.init()
        mixer.music.load("sounds/" + opperation + ".mp3")
        mixer.music.set_volume(0.3)
        mixer.music.play()
        while mixer.music.get_busy():
            pass
        mixer.music.stop()




