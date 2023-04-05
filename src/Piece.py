import pygame
pygame.init()

class Piece:

    def __init__(self,color):
        self.row = 0
        self.column = 0
        self.radius = 12
        self.possible_moves = []

        if color == 1:
            self.color = (255,255,255)
        else:
            self.color = (0,0,0)
    
    def draw(self,WINDOW):
        pygame.draw.circle(WINDOW, self.color, (self.column * 60 + 90, self.row * 60 + 90), self.radius)
    