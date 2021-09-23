import pygame
import random
import time
import numpy as np
from .piece import Piece
from .piece import Pawn, Rook, Knight, Bishop, King, Queen, EmptySpace
from sjakk.board import Board
from copy import deepcopy

def computerRandom(board, window, color):
    #Trenger:
    #   -Liste over brikker som skal velges fra
    #   -Så velger vi en av disse brikkene
    #   -Deretter velger vi ett av trekkene den kan ta
    #   -Så må vi sjekke om dette trekket er lovlig
    #   -Hvis ikke, fjerner vi trekket fra listen og finner et nytt
    #   -Hvis brikken ikke kan gjøre noen trekk må vi finne en ny brikke
    #   -Hvis vi har gått gjennom alle brikkene og ikke kan finne et gyldig trekk
    #    kan vi anta at vi står i sjakk matt

    listOfPieces = []
    madeMove = False
    print(board.objectBoard)
    for i in range(8):
        for element in board.objectBoard[i]:
            if element.colour == color:
                print(element)
                listOfPieces.append(element)

    while len(listOfPieces) != 0:
        round = 0
        randomPiece = random.choice(listOfPieces)
        print(randomPiece.name)
        board.selectedPiece = randomPiece
        randomPiece.movesAvailable(board.objectBoard, window, draw=True)
        pygame.display.update()
        time.sleep(1)

        #Nå skal randomPiece ha en oversikt over alle trekkene den kan utføre
        #Vi velger et av trekkene
        while len(randomPiece.movesAvailableList) != 0:
            chosenMove = random.choice(randomPiece.movesAvailableList)


            #Vi gjør trekket i et separat brett som er direkte kopiert fra det andre brettet
            newBoard = deepcopy(board)
            newBoard.moveHere(window, chosenMove[1], chosenMove[0])

            #Vi sjekker om trekket er lovlig, hvis ikke må vi slette 
            #trekket som et alternativ

            if newBoard.checkMoves(window, color) == True:
                print(board.objectBoard)
                board.moveHere(window, chosenMove[1], chosenMove[0])
                print(board.objectBoard)
                del newBoard
                print('Move is legal')
                print(randomPiece.name)
                print(chosenMove)
                randomPiece.movesAvailableList = []
                madeMove = True
                #No piece is now selected
                board.selectedPiece = None
                board.drawBoard(window)
                board.draw(window)
                pygame.display.update()
                print('updated')
                return madeMove
            else:
                print('This move is not legal: ' + randomPiece.name)
                randomPiece.movesAvailableList.remove(chosenMove)
            del newBoard
        listOfPieces.remove(randomPiece)
        round += 1
        print(round)
    return madeMove


def computerHasAllMoves(board, window, color):
    listOfPieces = []
    movesPerPiece = []
    allMoves = []
    madeMove = False
    print(board.objectBoard)

    for i in range(8):
        for element in board.objectBoard[i]:
            if element.colour == color:
                listOfPieces.append(element)
    
    for currentPiece in listOfPieces:
        currentPiece.movesAvailable(board.objectBoard, window, draw=False)
        nrMoves = len(currentPiece.movesAvailableList)
        movesPerPiece.append(nrMoves)
        for move in currentPiece.movesAvailableList:
            allMoves.append(move)
    
    while madeMove == False:
        randomNumber = random.randint(0, len(allMoves)-1)
        chosenMove = allMoves[randomNumber]

        i = 0
        while randomNumber > -1 or randomNumber == -1:
            print('randomNumber: ', randomNumber)
            print('The ', i, ' piece can move', movesPerPiece[i])
            randomNumber = randomNumber - movesPerPiece[i]
            if randomNumber == -1 or randomNumber < -1:
                break
            i += 1

        chosenPiece = listOfPieces[i]
        print(chosenPiece.name)
        board.selectedPiece = chosenPiece
        
        newBoard = deepcopy(board)
        newBoard.moveHere(window, chosenMove[1], chosenMove[0])

        if newBoard.checkMoves(window, color) == True:
            print('printing the chosen piece for white!: ', chosenPiece.name)
            print('And its moves: ', chosenPiece.movesAvailableList)
            print(chosenMove)
            board.moveHere(window, chosenMove[1], chosenMove[0])
            
            del newBoard
            print('Move is legal')

            for piece in listOfPieces:
                piece.movesAvailableList = []
            madeMove = True
            #No piece is now selected
            board.selectedPiece = None
            board.drawBoard(window)
            board.draw(window)
            pygame.display.update()
            print('updated')
            return madeMove
        else:
            print('This move is not legal: ' + chosenPiece.name)
            chosenPiece.movesAvailableList.remove(chosenMove)
        del newBoard
    return madeMove

                        
                            
            
            
            
