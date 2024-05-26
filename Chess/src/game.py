import pygame

from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square


class Game:

    def __init__(self):
        self.board = Board()
        self.hovered_sqr = None
        self.next_player = 'white'
        self.dragger = Dragger()
        self.config = Config()

    # Show methods
    def show_bg(self, surface):
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg.light if (row+ col) %2 == 0 else theme.bg.dark
                rect = (col*SQSIZE, row*SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

                if col == 0:
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light # alternates color of number on each square depending if square is a light or dark color green. If square is dark green, the number is a light green color and vice versa for light green. It makes it easier to see number
                    lbl = self.config.font.render(str(ROWS -row), 1, color)
                    lbl_pos = (5, 5+ row * SQSIZE) # this calculation places each number on the top left corner of each column
                    surface.blit(lbl, lbl_pos)
                if row == 7:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light # alternates color of number on each square depending if square is a light or dark color green. If square is dark green, the number is a light green color and vice versa for light green. It makes it easier to see number
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color) # the one is for aliais, it removes the alias effect, which makes edges looked for jagged and look blurry
                    lbl_pos = (col*SQSIZE + SQSIZE-20, HEIGHT -20) # this calculation places each letter at the bottom right corner of the last row of the chess board
                    surface.blit(lbl, lbl_pos)
    
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
            # checking if there is a piece on a specific square
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    if piece is not self.dragger.piece:
                        piece.set_texture(size = 80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE //2, row * SQSIZE + SQSIZE//2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect) # blit receives the object we want to shwow on screen and its position
    def show_moves(self, surface):
        theme = self.config.theme
        if self.dragger.dragging:
            piece = self.dragger.piece
            # looping all possible valid moves
            for move in piece.moves:
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                rect  = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
    def show_hover(self, surface):
        if self.hovered_sqr:
            color = (180, 180, 180)

            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)

            pygame.draw.rect(surface, color, rect, width =3)
    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def show_last_move(self, surface):
        theme = self.config.theme
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                rect = (pos.col * SQSIZE, pos.row *SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
    def change_theme(self):
        self.config.change_theme()
    def sound_effect(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()
    def reset(self):
        self.__init__()
        