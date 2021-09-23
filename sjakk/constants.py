import pygame

#størrelse på brettet
width, height = 800, 800

#Rader og kolonner på brettet
rows = 8
columns = 8
squareSize = width//columns

#Farger
white = (240,250,250)
red = (255,0,0)
blue = (0,0,255)
black = (0,0,0)
brown = (25, 25, 25)

#models for pieces
whitePawn = pygame.image.load('assets/WhitePawn.png')
whiteRook = pygame.image.load('assets/WhiteRook.png')
whiteKnight = pygame.image.load('assets/WhiteKnight.png')
whiteQueen = pygame.image.load('assets/WhiteQueen.png')
whiteBishop = pygame.image.load('assets/WhiteBishop.png')
whiteKing = pygame.image.load('assets/WhiteKing.png')
blackPawn = pygame.image.load('assets/BlackPawn.png')
blackRook = pygame.image.load('assets/BlackRook.png')
blackKnight = pygame.image.load('assets/BlackKnight.png')
blackQueen = pygame.image.load('assets/BlackQueen.png')
blackBishop = pygame.image.load('assets/BlackBishop.png')
blackKing = pygame.image.load('assets/BlackKing.png')


