from const import *
from square import Square
from piece import *
from move import Move
import copy
from sound import Sound
import os
import pygame





class Board:

    def __init__(self):
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def calc_moves(self, piece, row, col, bool = True): 
        # important method that calculates all the possible moves of a specific piece from a specific position
        def king_moves():
            adjs = [ # all adjacent moves of the king
                (row-1, col +0), # moving north on the board
                (row-1, col+1),  # moving north east on the board
                (row-1, col-1),  # moving north west on the board
                (row + 0, col+1), # moving east on the board
                (row + 0, col -1),  # moving west on the board
                (row + 1, col + 0),  # moving south on the board
                (row + 1, col +1),  # moving south east on the board
                (row + 1, col -1)  # moving south west on the board
            ]
            piece_moves(adjs)
            if not piece.moved:
                #castling to queens side(left)
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1,4):
                            if self.squares[row][c].has_piece(): # breaks when castling is not possible due to pieces being in the way
                                break

                            if c ==3:
                                piece.left_rook = left_rook 
                                # moves rook to new square after castling
                                initial = Square(row, 0)
                                final = Square(row,3)
                                moveR = Move(initial, final)  # moveR for moving rook
                                # moves king to new square after castling
                                initial = Square(row, col)
                                final = Square(row,2)
                                moveK = Move(initial, final)   # moveK for moving King

                                if bool: 
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR) : # checks of a player will be in check if they try to move the king and rook during castling
                                        left_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                else: 
                                    left_rook.add_move(moveR)
                                    piece.add_move(moveK)
        
        # for king castling to right side
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5,7):
                            if self.squares[row][c].has_piece(): # breaks when castling is not possible due to pieces being in the way
                                break

                            if c ==6:
                                piece.right_rook = right_rook # adds left rook to king 
                                # moves rook to new square after castling
                                initial = Square(row, 7)
                                final = Square(row,5)
                                moveR = Move(initial, final) 
                                # moves king to new square after castling
                                initial = Square(row, col)
                                final = Square(row,6)
                                moveK = Move(initial, final) 

                                if bool: 
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR) : # checks of a player will be in check if they try to move the king and rook during castling
                                        right_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                else: 
                                    right_rook.add_move(moveR)
                                    piece.add_move(moveK)




        def pawn_moves():
            if piece.moved:
                steps = 1
            else:
                steps = 2
            
            #vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1+steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        initial = Square(row, col)
                        final = Square(possible_move_row,col )
                        move = Move(initial, final)
                    #checking if there is a potential check in the game before the move can be made
                        if bool: 
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else: 
                            piece.add_move(move)  
                    else: # when the first square filled and pawn cannot move there
                        break
                else :# when the move is not in range
                    break
            
            # diagonal moves when a pawn captures a piece
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                        initial = Square(row,col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final =Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)
                        if bool:
                                 if not self.in_check(piece, move):
                                     piece.add_move(move)
                        else:
                                piece.add_move(move)
            # left en passant
            r = 3 if piece.color == 'white' else 4 # 3 for white pawns and 4 for black pawns.  r variable is for specific row
            fr = 2 if piece.color == 'white' else 5 # fr stands for final row of a pawn piece, it is 2 when a white pawn does en passant and 5 when a black pawn does en passant
            if Square.in_range(col-1) and row == r:
            # checking for pawn to left of pawn that just moved up 2 squares(left en passant) and also if opposing pawn is on the same row and the pawn that was just moved                 
                if self.squares[row][col-1].has_rival_piece(piece.color):
                     p = self.squares[row][col-1].piece
                     if isinstance(p, Pawn):
                         if p.en_passant:
                             intial = Square(row, col)
                             final = Square(fr, col-1, p)
                             move = Move(intial, final)
                             if bool:
                                 if not self.in_check(piece, move):
                                     piece.add_move(move)
                             else:
                                piece.add_move(move)
            # right en passant
            r = 3 if piece.color == 'white' else 4 # 3 for white pawns and 4 for black pawns.  r variable is for specific row
            fr = 2 if piece.color == 'white' else 5 # fr stands for final row of a pawn piece, it is 2 when a white pawn does en passant and 5 when a black pawn does en passant
            if Square.in_range(col+1) and row == r:
            # checking for pawn to left of pawn that just moved up 2 squares(left en passant) and also if opposing pawn is on the same row and the pawn that was just moved                 
                if self.squares[row][col+1].has_rival_piece(piece.color):
                     p = self.squares[row][col+1].piece
                     if isinstance(p, Pawn):
                         if p.en_passant:
                             intial = Square(row, col)
                             final = Square(fr, col+1, p)
                             move = Move(intial, final)
                             if bool:
                                 if not self.in_check(piece, move):
                                     piece.add_move(move)
                             else:
                                piece.add_move(move)
                             
        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr
                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        initial = Square(row,col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)
                        
                    
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            if bool: 
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else: 
                                piece.add_move(move)
        

                        elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                            if bool: 
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else: 
                                piece.add_move(move)
                            break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    
                    else: break
                    
                    

                        
                    possible_move_row =  possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr
            
        def piece_moves(adjs): # a method called by knight_moves and king_moves to remove repitition of code
           for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        # creating a square of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # creating a new move
                        move = Move(initial, final)
                        if bool: 
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else: break
                        else: 
                            piece.add_move(move)
        
        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]
            piece_moves(possible_moves)
        
        if isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1,1), # moving north east on the board
                (-1,-1), # moving north west on the board
                (1,1),  # moving south east on the board
                (1,-1)   # moving south west on the board
            ])
        elif isinstance(piece, Rook):
            straightline_moves([
                (-1,0), # moving north on the board
                (0,1),  # moving east on the board
                (1,0),    # moving south on the board
                (0,-1)   # moving west on the board
            ])
        elif isinstance(piece, Queen):
            straightline_moves([
               (-1,1), # moving north east on the board
                (-1,-1), # moving north west on the board
                (1,1),  # moving south east on the board
                (1,-1),   # moving south west on the board
                (-1,0), # moving north on the board
                (0,1),  # moving east on the board
                (1,0),    # moving south on the board
                (0,-1)   # moving west on the board
            ])
        elif isinstance(piece, King):
            king_moves()
    
    def move(self, piece,move, testing = False):
        initial = move.initial
        final = move.final
        self.last_move = None 
        en_passant_empty = self.squares[final.row][final.col].isempty()
        #console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece
        
        
        if isinstance(piece, Pawn):
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty : # if diff(difference in columns is 0, that means the pawn has not moved diagonally and captured a pawn via en passant
            # if it is not 0, the pawn has moved diagonally to capture a pawn
            # the second part is to make sure the square the pawn will move to after capturing a pawn via en passant is empty

            #console board move update
            
                    self.squares[initial.row][initial.col + diff].piece = None
                    self.squares[final.row][final.col].piece = piece
                    if not testing:
                        sound = Sound(os.path.join(
                            'assets/sounds/capture.wav'
                        )) 
                        sound.play()
            
            else:
            # pawn promotion
                self.check_promotion(piece, final)

        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if(diff<0) else piece.right_rook  
                # the difference between change in columns for a king during castling should be at least 2. if the differrence
                # is less than 0 in line 208, that means there were more than 2 spaces between a rook and a king, meaning that the king
                # was castling to the left(Queen's side castle). If its not, the only other option is that the king is castling with the right rook(King's side castle)
                self.move(rook, rook.moves[-1]) # using recursion to move specific rook(found in line 209) to final position(rook.moves[-1])

        


        piece.moved = True

        piece.clear_moves()
        # changing positions, clear and reset valid moves
        self.last_move = move # sets the last move

    def valid_move(self, piece, move):
        return move in piece.moves
    
    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
                pygame.init()
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                self.squares[final.row][final.col].piece = Queen(piece.color) # promotes immediately to Queen, by pressing q on key board
                                running = False
                            elif event.key == pygame.K_k:
                                self.squares[final.row][final.col].piece = Knight(piece.color) # promotes immediately to Knight, by pressing k on keyboard
                                running = False
                            elif event.key == pygame.K_o:
                                self.squares[final.row][final.col].piece = Rook(piece.color) # promotes immediately to Rook by pressing o on keyboard, r is already taken for restart
                                running = False
                            elif event.key == pygame.K_b:
                                self.squares[final.row][final.col].piece = Bishop(piece.color) # promotes immediately to Bishop, by pressing b on keyboard
                                running = False
                            else: break
                            # IMPORTANT: for promotion to actually occur, user must press on pawn right before it moving it to last row to get promoted, then press the character
                            # on the keyboard for piece they want the pawn to get promoted to twice. Then the pawn will show it's possible moves and the user will click on the square
                            # they want the pawn to move to and clicked the character on they keyboard they want to pawn to be promoted to one last time for promotion to occur
                            
    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2 #the only way a king can move two squares is if its castling, so this method tells you if a king has castled or not
    
    def set_true_en_passant(self, piece):
                if  not isinstance(piece, Pawn):
                    return
                for row in range(ROWS):
                    for col in range(COLS):
                        if isinstance(self.squares[row][col].piece, Pawn):
                            self.squares[row][col].piece.en_passant = False
                piece.en_passant = True
                        
                        
    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing = True)
        #creating a temporary board to see find if either kings will be in check

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_rival_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool = False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True # looping  through each move to see if final square the piece will move to has a king there, effectively meaning the piece will be in check
        return False

 # starting method name with underscore(_) declares it as private
    def _create(self):

        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6,7) if color == 'white' else (1,0)
        # adding pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
           

        #adding knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))
        

        #adding bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
        

        #adding rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))
        

        #adding king
        self.squares[row_other][4] = Square(row_other, 3, King(color))
        
        

        #adding queen
        self.squares[row_other][3] = Square(row_other, 4, Queen(color))
        