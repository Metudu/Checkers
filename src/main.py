import pygame,socket,threading,pickle
from Board import Board
pygame.init()

# General Variables
IP_ADDRESS = '3.67.195.65'
PORT = 5000

client = socket.socket()
client.connect((IP_ADDRESS, PORT))

def get_turn():
    while True:
        global your_turn
        print(your_turn)
        your_turn = pickle.loads(client.recv(512))

board = Board(60, 60, 60, 60)
clicked_piece = 0
your_colour, your_turn = pickle.loads(client.recv(1024))
run = pickle.loads(client.recv(512))

# Window 
WIDTH = 600
HEIGHT = 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers!')

# Colors
BACKGROUND = (200,200,200)

WINDOW.fill(BACKGROUND)
board.draw_board(WINDOW)
board.draw_pieces(WINDOW)
turn_thread = threading.Thread(target=get_turn)
turn_thread.start()

while run:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if your_turn:
                x_pos, y_pos = pygame.mouse.get_pos()
                row = (y_pos - 60) // 60
                column = (x_pos - 60) // 60

                # Eğer bir taşa tıklanmış ise
                if board.is_clicked(row, column):
                    clicked_piece = board.positions[row][column]
                    board.positions[row][column].radius *= 1.25
                    board.draw(WINDOW)
                    board.draw_possible_moves(WINDOW, board.possible_moves(row, column))
                    board.positions[row][column].radius /= 1.25

                else:
                    if clicked_piece != 0 and (row,column) in clicked_piece.possible_moves:
                        board.move((row,column),clicked_piece)
                        clicked_piece.possible_moves.clear()
                        your_turn = False
                        client.send(pickle.dumps(your_turn))
                    board.draw(WINDOW)
                    clicked_piece = 0

        if event.type == pygame.QUIT:
            run = False
            turn_thread._stop()
            break

pygame.quit()