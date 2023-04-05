import pygame
from Piece import Piece
pygame.init()

class Board:

    def __init__(self,x,y,square_width,square_height):
        self.x = x
        self.y = y
        self.square_height = square_height
        self.square_width = square_width
        self.positions = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            []
        ]
    
    # For draw only board and not pieces. If it's invoked for the first time, it also initialize the pieces
    def draw_board(self,WINDOW):
        row_x = self.x
        row_y = self.y

        for row in range(8):
            for column in range(8):
                if (row + column) % 2 == 0:
                    # Drawing white squares
                    pygame.draw.rect(WINDOW, (230,230,230), pygame.rect.Rect(row_x, row_y, self.square_width, self.square_height))
                    # To fill the pieces list
                    # White squares is always empty that's why always appending 0
                    if len(self.positions[7]) * len(self.positions) < 64:
                        self.positions[row].append(0)

                elif (row + column) % 2 == 1:
                    pygame.draw.rect(WINDOW, (109,49,9), pygame.rect.Rect(row_x, row_y, self.square_width, self.square_height))

                    # Dark squares can have pieces. If the row is between 0 and 2, white pieces must be placed.
                    if len(self.positions[7]) * len(self.positions) < 64:
                        if 0 <= row <= 2:
                            self.positions[row].append(Piece(1))
                            self.positions[row][column].row = row
                            self.positions[row][column].column = column

                        elif 5 <= row <= 7:
                            self.positions[row].append(Piece(-1))
                            self.positions[row][column].row = row
                            self.positions[row][column].column = column
                        
                        # Dark squares can also be empty. That's why appending 0
                        else:
                            self.positions[row].append(0)
                
                row_x += self.square_width
            row_x = self.x
            row_y += self.square_height

    def draw_pieces(self,WINDOW):
        for row in self.positions:
            for piece in row:
                if piece != 0:
                    piece.draw(WINDOW)

    def draw(self,WINDOW):
        self.draw_board(WINDOW)
        self.draw_pieces(WINDOW)

    # If a piece has clicked and it has black color, returns True
    def is_clicked(self,row,column):
        if self.positions[row][column] != 0 and self.positions[row][column].color == (0,0,0):
            return self.positions[row][column] != 0
        return False

    # 
    def possible_moves(self,row,column):
        possible_moves = []
        if 0 <= row - 1 and 0 <= column - 1:
            if self.positions[row - 1][column - 1] == 0:
                self.positions[row][column].possible_moves.append((row - 1, column - 1))
                possible_moves.append((row - 1, column - 1))

        if row - 1 <= 7 and column + 1 <= 7:
            if self.positions[row - 1][column + 1] == 0:
                self.positions[row][column].possible_moves.append((row - 1, column + 1))
                possible_moves.append((row - 1, column + 1))

        return possible_moves

    def draw_possible_moves(self,WINDOW,possible_moves):
        for coordinate in possible_moves:
            pygame.draw.circle(WINDOW, (255,0,0), (coordinate[1] * 60 + 90, coordinate[0] * 60 + 90), 6)
    
    def move(self,coordinate,piece):
        self.positions[coordinate[0]][coordinate[1]] = piece
        self.positions[piece.row][piece.column] = 0
        piece.row = coordinate[0]
        piece.column = coordinate[1]


