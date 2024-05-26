import random
from hex import Hex

class Board:
    
    def __init__(self, standardPenguins = True, boardsize=3):
        ''' creates the board and the pieces '''

        self.boardsize = boardsize
        
        self.gamepieces = []
        
        self.hittables = [(-3, 0), (-3, 1), (-3, 2), (-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-2, 3), (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3), (0, -3), (0, -2), (0, -1), (0, 1), (0, 2), (0, 3), (1, -3), (1, -2), (1, -1), (1, 0), (1, 1), (1, 2), (2, -3), (2, -2), (2, -1), (2, 0), (2, 1), (2, 2), (3, -2), (3, -1), (3, 0)]
        
        self.supports = [(-2, 4), (-1, 4), (0, 4), (1, 3), (2, 3), (3, 2), (3, 1), (4, 0), (4, -1), (4, -2), (4, -3), (3, -3), (3, -4), (2, -4), (1, -4), (0, -4), (-1, -3), (-2, -3), (-3, -2), (-3, -1), (-4, 0), (-4, 1), (-4, 2), (-4, 3), (-3, 3), (-3, 4), (-2, 4), (-1, 4)]

        self.gamepieces.append(Hex(0, 0, 0, "penguin"))

        #for penguins-style game setup
        if standardPenguins:
            random_indices = random.sample(range(len(self.hittables)), len(self.hittables) // 2)
            counter = 0
            for piece in self.hittables:
                if counter in random_indices:
                    self.gamepieces.append(Hex(piece[0], piece[1], -piece[0]-piece[1], "blue"))
                else:
                    self.gamepieces.append(Hex(piece[0], piece[1], -piece[0]-piece[1], "white"))
                counter += 1
            for piece in self.supports:
                self.gamepieces.append(Hex(piece[0], piece[1], -piece[0]-piece[1], "support"))
        
        #for hex-style game setup
        else:
            
            def generate_array(n):
                k = 1 + sum(6*i - 6 for i in range(2, n+1))
                array = ["blue"] * k

                random_indices = random.sample(range(2, k), k // 2)
                for index in random_indices:
                    array[index] = "white"

                return array


            counter = 0
            piecesetup = generate_array(boardsize + 1)
            for i in range (-boardsize-1, boardsize+2): #accounting for supports
                for j in range (-boardsize-1, boardsize+2): #accounting for supports
                    if (abs(i) + abs(j) + abs(-i-j))/2 <= boardsize: #if in playing area
                        print(counter)
                        self.gamepieces.append(Hex(i, j, -i-j, piecesetup[counter]))  
                        counter += 1
                    if (abs(i) + abs(j) + abs(-i-j))/2 == boardsize + 1:
                        self.gamepieces.append(Hex(i, j, -i-j, "support"))

    def find_hex_from_coordinates(self, q, r, s):
        for piece in self.gamepieces:
            if piece.q == q and piece.r == r and piece.s == s:
                return piece
        return None

    def remove_hex_no_gravity(self, q, r, s):
        for piece in self.gamepieces:
            if piece.q == q and piece.r == r and piece.s == s:
                self.gamepieces.remove(piece)
                return True
        return False
    
    def remove_hex(self, q, r, s):
        for piece in self.gamepieces:
            if piece.q == q and piece.r == r and piece.s == s:
                self.gamepieces.remove(piece)
            
                for neighbor in self.returnNeighbors(piece):
                    if neighbor != None and neighbor.hextype != "support" and not self.is_piece_supported(neighbor):
                        self.remove_hex(neighbor.q, neighbor.r, neighbor.s)
    
    def is_hex_a_neighbor(self, hex, qo, ro, so):
        '''check if a hex is a neighbor of another hex'''
        q, r, s = hex.q, hex.r, hex.s
        if self.find_hex_from_coordinates(q+qo, r+ro, s+so) != None:
            return True
        return False
    
    def is_piece_supported(self, piece):
        '''check if a piece can stay up
            there are 5 possibilities,
            - two three-prongs
            - three lines
        '''
        pieceSupported = False

        neighborCheck = [(1, 0, -1), (1, -1, 0), (0, -1, 1), (-1, 0, 1), (-1, 1, 0), (0, 1, -1)]
        nl = []
        for thing in neighborCheck:
            nl.append(self.is_hex_a_neighbor(piece, thing[0], thing[1], thing[2]))

        if nl[0] and nl[2] and nl[4]:
            pieceSupported = True
        elif nl[1] and nl[3] and nl[5]:
            pieceSupported = True
        elif nl[0] and nl[3]:
            pieceSupported = True
        elif nl[1] and nl[4]:
            pieceSupported = True
        elif nl[2] and nl[5]:
            pieceSupported = True

        return pieceSupported  
    
    def returnNeighbors(self, piece):
        '''returns the neighbors of a piece'''
        neighborCheck = [(1, 0, -1), (1, -1, 0), (0, -1, 1), (-1, 0, 1), (-1, 1, 0), (0, 1, -1)]
        nl = []
        for thing in neighborCheck:
            nl.append(self.find_hex_from_coordinates(piece.q + thing[0], piece.r + thing[1], piece.s + thing[2]))

        return nl

    def penguinOnBoard(self):
        if self.find_hex_from_coordinates(0, 0, 0) == None:
            return False
        return True