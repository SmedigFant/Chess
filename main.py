import pygame
import time
from copy import deepcopy
from sjakk.constants import width, height, squareSize
from sjakk.board import Board
from sjakk.piece import Pawn, Rook, Bishop, Knight, King, Queen
from sjakk.computer import computerRandom, computerHasAllMoves

FPS = 20

window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Sjakk')

def getPosFromMouse(pos):
    x,y = pos
    row = y // squareSize
    column = x // squareSize
    return row, column

#For å bytte hvilken spiller har neste trekk, sett turn = changeTurn(turn)
def changeTurn(turn):  
    if turn == 'black':
        print("changing from 0 to 1")
        return 'white'
    elif turn == 'white':
        print("changing from 1 to 0")
        return 'black'

#Sjekker om et trekk gjør at man setter seg selv i sjakk
#Vi kan simulere trekket før vi faktisk flytter brikken, hvis trekket
#fører til at kongen står i sjakk, vil det si at trekket er ugyldig
#Tror det er best om vi faktisk flytter brikkene uten å blitte de og etter
#hver sjekk bare flytte brikkene tilbake slik at vi later som om det aldri
#skjedde
#def checkCheck()


if __name__ == "__main__":
    running = True
    clock = pygame.time.Clock()
    board = Board(width, height)
    board.initializeClassicBoard()
    
    for i in range(len(board.objectBoard)):
        print(board.objectBoard[i])
    
    
    board.drawBoard(window)
    board.draw(window)
      
    pygame.display.update()
    
    


    clickNr = 0
    selected = 0
    movesMade = 0
    turn = 'white'
    #whiteKingPos = [3, 7]
    #blackKingPos = [4, 0]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            
            #Someone clicked on the board and we need to check some things
            #1. If we do not have a selected piece already, we have to identify a new
            #   piece that the player is trying to select.
            #   If the player is clicking an empty space and does not have a selected piece
            #   we should give a warning saying that the player has to select a piece first in 
            #   order to move it.
            #   /* MORE TEXT CAN BE ADDED, CANT BE ARSED ATM */

            if turn == 'black':
                print('blacks turn')
                madeMove = computerRandom(board, window, 'black')
                if madeMove == True:
                    turn = changeTurn(turn)
                    print('black made a move')
                else: 
                    print('Game over, black is in checkmate')
                    time.wait(3)
                    quit()
            elif turn == 'white':
                print('whites turn!')
                madeMove = computerHasAllMoves(board, window, 'white')
                if madeMove == True:
                    turn = changeTurn(turn)
                    print('white made a move')
                else: 
                    print('Game over, black is in checkmate')
                    time.wait(3)
                    quit()
                
                
                

            if event.type == pygame.MOUSEBUTTONDOWN and selected == 0:
                print('selected == 0')
                
                board.drawBoard(window)
                board.draw(window)
                #Get the position of the mouse
                pos = pygame.mouse.get_pos()
                row, col = getPosFromMouse(pos)

                #Find out which piece was clicked
                #Remember to implement turnbased choosing here
                #We should not be able to select a piece that is not supposed to move this turn
                
                board.selectedPiece = board.objectBoard[row][col]  
                if board.selectedPiece.name != "empty" and board.selectedPiece.colour == turn:
                    selected = 1
                    #Find where this piece can move
                    board.availableMoves(window)
                    #show the moves
                    pygame.display.update()
                   
                else:
                    pass
                print("is a piece selected? ", selected)
                print(turn)




            elif event.type == pygame.MOUSEBUTTONDOWN and selected == 1:  
                print('selected == 1')  
                pos = pygame.mouse.get_pos()
                row, col = getPosFromMouse(pos)
                #check the potentially new selected piece
                newPiece = board.objectBoard[row][col]
                print(newPiece, board.selectedPiece)

                if newPiece != board.selectedPiece and newPiece.name != "empty" and newPiece.colour == board.selectedPiece.colour:
                    print('new piece selected')
                    board.selectedPiece = newPiece
                    #Find where this piece can move
                    board.drawBoard(window)
                    board.draw(window)
                    board.availableMoves(window)
                    pygame.display.update()
                
                elif newPiece == board.selectedPiece:
                    selected = 0
                    board.drawBoard(window)
                    board.draw(window)
                    pygame.display.update()

                #newPiece.colour == board.selectedPiece.colour:
                elif board.selectedPiece != None:
                    #Vi må sjekke om brikken vi har valgt, faktisk kan flytte til posisjonen
                    #som brukeren vil
                    board.availableMoves(window)
                    desiredMove = [col, row]
                    movesList = board.selectedPiece.movesAvailableList

                    #If the move we want to make is in the list of available moves
                    if desiredMove in movesList:
                        #Need a backup of how the board looked incase we have to revert it
                        newBoard = deepcopy(board)
                        

                        #Check if move does not put own king in check
                        #checkCheck(board.selectedPiece, desired move, full board)
                        #Moving the piece
                        newBoard.moveHere(window, row, col)

                        #Now we should check if the move resulted in 
                        #putting ourselves in check
                        #If this is the case, then we revert back to previousBoard
                        #Make sure the piece does not have the same available moves
                        #it had before it moved
                        
                        if newBoard.checkMoves(window, turn) == True:
                            board = newBoard
                            print('Move is legal')
                            board.selectedPiece.movesAvailableList = []

                            #No piece is now selected
                            selected = 0
                            board.drawBoard(window)
                            board.draw(window)
                            pygame.display.update()

                            #Changing the turn to opposite player
                            turn = changeTurn(turn)
                            movesMade = movesMade + 1

                        else:  
                            print('You are in check, please move again')
                            selected = 0
                            board.drawBoard(window)
                            board.draw(window)
                            pygame.display.update()

                        
                    #If the move is not in the list of available moves  
                    else:
                        print('You cannot move here with this piece')
                        print(desiredMove)
                        print(movesList)
                        board.drawBoard(window)
                        board.draw(window)
                        pygame.display.update()
                        selected = 0
                        
                    

    pygame.quit()
            
