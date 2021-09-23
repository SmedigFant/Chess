import pygame
from .constants import squareSize, whiteBishop, whiteKing, whiteKnight, whitePawn, whiteQueen, whiteRook
from .constants import blackBishop, blackKing, blackKnight, blackPawn, blackQueen, blackRook
from .constants import blue, red
import numpy as np

def switch(objectBoard, row, col, x, y):
    temp = objectBoard[x][y]
    objectBoard[x][y] = objectBoard[row][col]
    objectBoard[row][col] = temp
    return objectBoard



class Piece:
    def __init__(self, x, y, name, colour):
        self.movesAvailableList = []
        self.moveNr = 0
        self.colour = colour
        self.name = name
        self.col = y
        self.row = x
        self.y = (self.col)*squareSize + 20
        self.x = (self.row)*squareSize + 20
        self.canCastle = 0
        
    
    def draw(self, win):     
        if self.colour == "white":
            if self.name == "Pawn":
                win.blit(whitePawn, (self.y, self.x))
            elif self.name == "Rook":
                win.blit(whiteRook, (self.y, self.x))
            elif self.name == "Bishop":
                win.blit(whiteBishop, (self.y, self.x))
            elif self.name == "Knight":
                win.blit(whiteKnight, (self.y, self.x))
            elif self.name == "Queen":
                win.blit(whiteQueen, (self.y, self.x))
            elif self.name == "King":
                win.blit(whiteKing, (self.y, self.x))

        elif self.colour == "black":
            if self.name == "Pawn":
                win.blit(blackPawn, (self.y, self.x))
            elif self.name == "Rook":
                win.blit(blackRook, (self.y, self.x))
            elif self.name == "Bishop":
                win.blit(blackBishop, (self.y, self.x))
            elif self.name == "Knight":
                win.blit(blackKnight, (self.y, self.x))
            elif self.name == "Queen":
                win.blit(blackQueen, (self.y, self.x))
            elif self.name == "King":
                win.blit(blackKing, (self.y, self.x))
    
    def moveHere(self, objectBoard, win, row, col):
        board = objectBoard
        moved = 0
        for positions in self.movesAvailableList:
            if positions == [col, row]:
                #sletter det objektet som blir tatt og 
                #erstatter det med et empty space før vi flytter
                objectBoard[row][col].deleteSelf()
                takenSpot = EmptySpace(row, col, name="empty", colour=None)
                objectBoard[row][col] = takenSpot 

                #EmptySpace(row, col, name="empty", colour=None)
                switch(objectBoard, row, col, self.row, self.col)
                self.x = (row)*squareSize + 20
                self.y = (col)*squareSize + 20
                self.col = (self.y - 20)//squareSize
                self.row = (self.x - 20)//squareSize
                self.moveNr = 1 + self.moveNr 
                moved = 1
        if moved == 0:
            print('did not actually move')
        return board

    
        

    def __repr__(self):
        return self.name
    
    def deleteSelf(self):
        print("deleter ",  self.colour, " ", (self))
        del self





class Pawn(Piece):
    def movesAvailable(self, oldBoard, win, draw=True):
        self.movesAvailableList = []
        Ydirection = None
        #Sets the direction the pawns can move, downwards and to the right are
        #positive directions

        if self.colour == "black":
            Ydirection = 1
        elif self.colour == "white":
            Ydirection = -1

        blueXPos = (self.col*squareSize)+squareSize//2
        redXPos1 = ((self.col+1)*squareSize)+squareSize//2
        redXPos2 = ((self.col-1)*squareSize)+squareSize//2
        
        blueYPos1 = ((self.row+(1*Ydirection))*squareSize)+squareSize//2
        blueYPos2 = ((self.row+(2*Ydirection))*squareSize)+squareSize//2
        newYPos1 = self.row+(1*Ydirection)
        newYPos2 = self.row+(2*Ydirection)
       
        


        if self.moveNr == 0:
            if oldBoard[self.row+(1*Ydirection)][self.col].name == "empty":
                if draw==True:
                    pygame.draw.circle(win, blue, (blueXPos, blueYPos1), squareSize//4)
                self.movesAvailableList.append([self.col, self.row+(1*Ydirection)])

            if oldBoard[self.row+(2*Ydirection)][self.col].name == "empty":
                if draw==True:
                    pygame.draw.circle(win, blue, (blueXPos, blueYPos2), squareSize//4)
                self.movesAvailableList.append([self.col, self.row+(2*Ydirection)])
            
            #If the pawn is on one of the sides, we have to make sure we dont set our
            #possiblePiece to find a piece outside of the board
            outOfBoundsLarger = 0
            outOfBoundsSmaller = 0
            if self.col == 7:
                outOfBoundsLarger = 1
            elif self.col == 0:
                outOfBoundsSmaller = 1

            if not outOfBoundsLarger:
                #Checks if there is a piece that the pawn can take on one side
                possiblePiece = oldBoard[self.row+(1*Ydirection)][self.col+1]
                if possiblePiece.name != "empty" and possiblePiece.colour != self.colour:
                    if draw==True:
                        pygame.draw.circle(win, red, (redXPos1, blueYPos1), squareSize//4)
                    self.movesAvailableList.append([self.col+1, self.row+(1*Ydirection)])
            if not outOfBoundsSmaller:
                #Checks if the pawn can take a piece on the other side
                possiblePiece = oldBoard[self.row+(1*Ydirection)][self.col-1]
                if possiblePiece.name != "empty" and possiblePiece.colour != self.colour:
                    if draw==True:    
                        pygame.draw.circle(win, red, (redXPos2, blueYPos1), squareSize//4)
                    self.movesAvailableList.append([self.col-1, self.row+(1*Ydirection)])
        
        else:
            if oldBoard[self.row+(1*Ydirection)][self.col].name == "empty":
                if draw==True:
                    pygame.draw.circle(win, blue, (blueXPos, blueYPos1), squareSize//4)
                self.movesAvailableList.append([self.col, self.row+(1*Ydirection)])
            
            #If the pawn is on one of the sides, we have to make sure we dont set our
            #possiblePiece to find a piece outside of the board
            outOfBoundsLarger = 0
            outOfBoundsSmaller = 0
            if self.col == 7:
                outOfBoundsLarger = 1
            elif self.col == 0:
                outOfBoundsSmaller = 1

            if not outOfBoundsLarger:
                #Checks if there is a piece that the pawn can take on one side
                possiblePiece = oldBoard[self.row+(1*Ydirection)][self.col+1]
                if possiblePiece.name != "empty" and possiblePiece.colour != self.colour:
                    if draw==True:
                        pygame.draw.circle(win, red, (redXPos1, blueYPos1), squareSize//4)
                    self.movesAvailableList.append([self.col+1, self.row+(1*Ydirection)])
            if not outOfBoundsSmaller:
                #Checks if the pawn can take a piece on the other side
                possiblePiece = oldBoard[self.row+(1*Ydirection)][self.col-1]
                if possiblePiece.name != "empty" and possiblePiece.colour != self.colour:
                    if draw==True:
                        pygame.draw.circle(win, red, (redXPos2, blueYPos1), squareSize//4)
                    self.movesAvailableList.append([self.col-1, self.row+(1*Ydirection)])
                

class King(Piece):
    def __init__(self, x, y, name, colour):
        self.movesAvailableList = []
        self.moveNr = 0
        self.colour = colour
        self.name = name
        self.col = y
        self.row = x
        self.y = (self.col)*squareSize + 20
        self.x = (self.row)*squareSize + 20
        self.canCastle = 1

    def movesAvailable(self, oldBoard, win, draw=True):
        self.movesAvailableList = []
        for i in range(3):
            for j in range(3):
                blueXPos = ((self.col-j+1)*squareSize)+squareSize//2
                blueYPos = ((self.row-i+1)*squareSize)+squareSize//2
                bluePos = [blueXPos, blueYPos]

                #Sjekker at vi ikke går utenfor brettet
                if (blueXPos < 0 or blueXPos > 7*squareSize + squareSize//2):
                    break
                if (blueYPos < 0 or blueYPos > 7*squareSize + squareSize//2):
                    break

                try:
                    if oldBoard[self.row-i+1][self.col-j+1].name == "empty":
                        if draw==True:
                            pygame.draw.circle(win, blue, (blueXPos, blueYPos), squareSize//4)
                        self.movesAvailableList.append([self.col-j+1, self.row-i+1])
                        continue
                    elif oldBoard[self.row-i+1][self.col-j+1].colour != self.colour:
                        if draw==True:
                            pygame.draw.circle(win, red, (blueXPos, blueYPos), squareSize//4)
                        self.movesAvailableList.append([self.col-j+1, self.row-i+1])
                        continue
                    elif oldBoard[self.row-i+1][self.col-j+1].colour == self.colour:
                        continue
                except IndexError:
                    pass

    


    

class Knight(Piece):
    def movesAvailable(self, oldBoard, win, draw=True):
        self.movesAvailableList = []    
        #For some reason the x and the y for drawing is different from the x and y
        #for checking the list of numbers (Probably because of a wrong implementation CHECK BEFORE FINISHING)
        knightMoves = np.array(((-1,2),(-2,1),(-2,-1),(-1,-2),(1,2),(2,1),(2,-1),(1,-2)))
       
        for e in knightMoves:
            newX = self.col + e[0]
            newY = self.row + e[1]

            #Because we're using a list to check if there exists a board at a position
            #We Have to skip an iteration in case we get a negative number as these
            #indexes will correlate to an index, but not the one we are after. This
            #is because of how list indexes work list[-1] = last item in list.
            if newX <= -1 or newY <= -1:
                continue
            
            blueXPos = ((newX)*squareSize)+squareSize//2
            blueYPos = ((newY)*squareSize)+squareSize//2

            #Sjekker at vi ikke går utenfor brettet
            if (blueXPos < 0 or blueXPos > 7*squareSize + squareSize//2):
                continue
            if (blueYPos < 0 or blueYPos > 7*squareSize + squareSize//2):
                continue

            try:
                if oldBoard[newY][newX].name == "empty":
                    if draw==True:
                        pygame.draw.circle(win, blue,(blueXPos, blueYPos), squareSize//4)
                    self.movesAvailableList.append([newX, newY])
                    continue
                elif oldBoard[newY][newX].colour != self.colour:
                    if draw==True:
                        pygame.draw.circle(win, red,(blueXPos, blueYPos), squareSize//4)
                    self.movesAvailableList.append([newX, newY])
                    continue
                elif oldBoard[newY][newX].colour == self.colour:
                    continue
            except IndexError:
                pass


class Queen(Piece):
    def movesAvailable(self, oldBoard, win, draw=True):
        self.movesAvailableList = []
        #First we check in one direction if the queen can move here, as long as 
        #she does not encounter another piece or runs out of the board
        #she will be able to keep going

        for i in range(3):
            for j in range(3):
                newX = self.col
                newY = self.row

                while True:        
                    newX += -j+1
                    newY += -i+1

                    blueXPos = ((newX)*squareSize)+squareSize//2
                    blueYPos = ((newY)*squareSize)+squareSize//2

                    #Sjekker at vi ikke går utenfor brettet
                    if (blueXPos < 0 or blueXPos > 7*squareSize + squareSize//2):
                        break
                    if (blueYPos < 0 or blueYPos > 7*squareSize + squareSize//2):
                        break
                    
                    try:
                        if oldBoard[newY][newX].name == "empty":
                            if draw==True:
                                pygame.draw.circle(win, blue, (blueXPos, blueYPos), squareSize//4)
                            self.movesAvailableList.append([newX, newY])
                            #print("I CAN MOVE HERE")
                        elif oldBoard[newY][newX].colour != self.colour:
                            if draw==True:
                                pygame.draw.circle(win, red, (blueXPos, blueYPos), squareSize//4)
                            self.movesAvailableList.append([newX, newY])
                            #print("enemy spotted")
                            break
                        elif oldBoard[newY][newX].colour == self.colour:
                            #print("here")
                            break
                        
                    except IndexError:
                        break
                        



class Rook(Piece):
    def __init__(self, x, y, name, colour):
        self.movesAvailableList = []
        self.moveNr = 0
        self.colour = colour
        self.name = name
        self.col = y
        self.row = x
        self.y = (self.col)*squareSize + 20
        self.x = (self.row)*squareSize + 20
        self.canCastle = 1

    def movesAvailable(self, oldBoard, win, draw=True):
        self.movesAvailableList = []
        for i in range(3):
            for j in range(3):
                newX = self.col
                newY = self.row 

                while True:
                    deltaX = -j+1
                    deltaY =-i+1

                    newX += deltaX
                    newY += deltaY

                    distanceX = abs(deltaX)
                    distanceY = abs(deltaY)

                    #Hvis vi går på skrå, hopper vi ut og finner neste potensielle trekk
                    if distanceX == distanceY:
                        break
                    
                    blueXPos = ((newX)*squareSize)+squareSize//2
                    blueYPos = ((newY)*squareSize)+squareSize//2

                    #Sjekker at vi ikke går utenfor brettet
                    if (blueXPos < 0 or blueXPos > 7*squareSize + squareSize//2):
                        break
                    if (blueYPos < 0 or blueYPos > 7*squareSize + squareSize//2):
                        break

                    try:
                        if oldBoard[newY][newX].name == "empty":
                            if draw==True:
                                pygame.draw.circle(win, blue, (blueXPos, blueYPos), squareSize//4)
                            self.movesAvailableList.append([newX, newY])
                        elif oldBoard[newY][newX].colour != self.colour:
                            if draw==True:    
                                pygame.draw.circle(win, red, (blueXPos, blueYPos), squareSize//4)
                            self.movesAvailableList.append([newX, newY])
                            break
                        elif oldBoard[newY][newX].colour == self.colour:
                            break
                    except IndexError:
                        break



class Bishop(Piece):
    def movesAvailable(self, oldBoard, win, draw=True):
        self.movesAvailableList = []
        for i in range(3):
            for j in range(3):
                newX = self.col
                newY = self.row 

                while True:
                    deltaX = -j+1
                    deltaY = -i+1

                    newX += deltaX
                    newY += deltaY

                    distanceX = abs(deltaX)
                    distanceY = abs(deltaY)

                    if (distanceX + distanceY) != 2:
                        break
                    
                    blueXPos = ((newX)*squareSize)+squareSize//2
                    blueYPos = ((newY)*squareSize)+squareSize//2

                    #Sjekker at vi ikke går utenfor brettet
                    if (blueXPos < 0 or blueXPos > 7*squareSize + squareSize//2):
                        break
                    if (blueYPos < 0 or blueYPos > 7*squareSize + squareSize//2):
                        break

                    try:
                        if oldBoard[newY][newX].name == "empty":
                            if draw==True:
                                pygame.draw.circle(win, blue, (blueXPos, blueYPos), squareSize//4)
                            self.movesAvailableList.append([newX, newY])
                        elif oldBoard[newY][newX].colour != self.colour:
                            if draw==True:    
                                pygame.draw.circle(win, red, (blueXPos, blueYPos), squareSize//4)
                            self.movesAvailableList.append([newX, newY])
                            break
                        elif oldBoard[newY][newX].colour == self.colour:
                            break
                    except IndexError:
                        break
                    
                    #If the length of movement in one direction is different from
                    #the other direction, we break out of the while loop and continue on
                    #the next iteration of the for-loop
                    

class EmptySpace(Piece):
    def movesAvailable(self, oldBoard, win):
        print("this is not a piece")
    