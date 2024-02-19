
import pygame as p
import ChessEngine


HEIGHT = WIDTH = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animation letter on
IMAGES = {}
validMoves = []

def load_images():
    pieces = ["bR", "bN", "bB", "bK", "bQ", "bp", "wR", "wN", "wB", "wK", "wQ", "wp", "dot"]
    for piece in pieces:
        IMAGES[piece] = p.image.load("images/" + piece + ".png")

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    load_images()
    running = True
    sqSelected = ()
    playerClicked = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicked = []
                else:
                    sqSelected = (row, col)
                    playerClicked.append(sqSelected)
                # if len(playerClicked) == 1:
                #     sqSelected = (0, 0)
                #     playerClicked.append(sqSelected)
                #     piece = ChessEngine.move(playerClicked[0], playerClicked[1], gs.board)
                #     validMoves = gs.pieceMoves[piece.pieceMoved](piece)
                #     playerClicked.pop()
                if len(playerClicked) == 2:
                    move = ChessEngine.move(playerClicked[0], playerClicked[1], gs.board)
                    if move.pieceMoved == "wN" or move.pieceMoved == "bN":
                        gs.queenMove(move)
                        if playerClicked[1] in gs.validMoves:
                            gs.makeMove(move)
                            sqSelected = ()
                            playerClicked = []

                        else:
                            sqSelected = ()
                            playerClicked = []
                            continue
                    else:
                        gs.makeMove(move)
                        sqSelected = ()
                        playerClicked = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()

            draw_game_state(screen, gs)
            clock.tick(MAX_FPS)
            p.display.flip()


def draw_game_state(screen, gs):
    draw_board(screen)
    draw_piece(screen, gs.board)
    drawDots(screen, validMoves, gs.board)




def draw_board(screen):
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
           Color = colors[(r+c)%2]
           p.draw.rect(screen, Color, p.Rect( c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE ))

def draw_piece(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawDots(screen, validMoves, board):
    for i in validMoves:
        r = i[0]
        c = i[1]
        piece = board[r][c]
        if piece == "--":
            screen.blit(IMAGES["dot"], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))




if __name__ == "__main__":
    main()



