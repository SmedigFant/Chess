import pygame
from .constants import width, height, white, blue, black, brown, rows, columns, squareSize
from .piece import Piece
import numpy as np
from .piece import Pawn, Rook, Knight, Bishop, King, Queen, EmptySpace



class Board:
    #initialize the board
    def __init__(self, width, height):
        self.width = width
        self.turn = False
        self.height = height
        #Remember that self.board is only here to initialize the objectboard
        #it is not updated after the first move, only the objectboard is updated
        self.board = np.zeros((8,8))
        self.selectedPiece = None
        self.objectBoard = []
        
        
    #draws the board, fills with black and draws white squares where we want them
    def drawBoard(self, win):
        win.fill(brown)
        for row in range(rows):
            for column in range(row%2, rows, 2):
                pygame.draw.rect(win, white, 
                    (row*squareSize, column*squareSize, squareSize, squareSize))

        
    #initialize the pieces on the board how it is classically set up
    def initializeClassicBoard(self):
        self.board[0] = [2,3,4,5,6,4,3,2]
        self.board[1] = [1,1,1,1,1,1,1,1]
        self.board[6] = [1,1,1,1,1,1,1,1]
        self.board[7] = [2,3,4,6,5,4,3,2]

        colour = "black"
        x,y = self.board.shape


        for i in range(y):
            if i > 1:
                colour = "white"
            self.objectBoard.append([])
            for j in range(x):
                name = ""
                if self.board[i,j] == 1:
                    name = "Pawn"
                    self.objectBoard[i].append(Pawn(i,j,name, colour))

                elif self.board[i,j] == 2:
                    name = "Rook"
                    self.objectBoard[i].append(Rook(i,j,name, colour))

                elif self.board[i,j] == 3:
                    name = "Knight"
                    self.objectBoard[i].append(Knight(i,j,name, colour))

                elif self.board[i,j] == 4:
                    name = "Bishop"
                    self.objectBoard[i].append(Bishop(i,j,name, colour))

                elif self.board[i,j] == 5:
                    name = "Queen"
                    self.objectBoard[i].append(Queen(i,j,name, colour))

                elif self.board[i,j] == 6:
                    name = "King"
                    self.objectBoard[i].append(King(i,j,name, colour))

                elif self.board[i,j] == 0:
                    name = "empty"
                    self.objectBoard[i].append(EmptySpace(i, j, name, colour=None))
    
    def availableMoves(self, win):
        #We want to know how the board looks, and which piece we want to move
        self.selectedPiece.movesAvailable(self.objectBoard, win)

        #To check where we want to move, we have to know how our piece CAN move
    
    def moveHere(self, win, row, col):
        #Må oppdatere objectBoard ved å flytte en brikke og returnere det nye 
        #brettet vi får
        self.objectBoard = self.selectedPiece.moveHere(self.objectBoard, win, row, col)

    #Checking if the player just put himself in check after it moved
    #by checking all the available moves of the opponent
    def checkMoves(self, win, turn):
        #for all the pieces on the board with a distinct colour, we should call
        #the function movesAvailable and append it to a list of all the tiles
        #that can be moved to by the opposing player

        legalMove = 1
        dangerousTiles = []
        kingPos = []
        for i in range(8):
            for piece in self.objectBoard[i]:
                if piece.colour != turn and piece.name != 'empty':
                    piece.movesAvailable(self.objectBoard, win, draw=False)
                    for element in piece.movesAvailableList:
                        dangerousTiles.append(element)
                    #Remembering to delete the list of available moves, just to not
                    #arrive at a point where it may result in faults if the system
                    #thinks that a piece can move somewhere after not updating the list
                    piece.movesAvailableList = []
                if piece.colour == turn and piece.name == 'King':
                    kingPos = [piece.col, piece.row]
        if kingPos in dangerousTiles:
            legalMove = 0
            print('selfCheck')

        return legalMove
              

    def draw(self, window):
        for pieceList in self.objectBoard:
            for piece in pieceList:
                if piece != "empty":
                    piece.draw(window)
    
    

        
                    

                
                
                
        
        



        
            

        
        




            
