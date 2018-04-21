from AlphaBeta import *
from BoardLogic import *
from heuristics import *
import time
import pygame
from pygame.locals import *

alpha = float('-inf')
beta = float('inf')

def boardOutput(board): # irrelevant after my modifications (need to reorder printing of array indices) ~Criss

		print(board[0]+"--------------------------"+board[1]+"--------------------------"+board[2]+"    ");
		print("|                           |                           |");
		print("|       "+board[3]+"------------------"+board[4]+"------------------"+board[5]+"----     |");
		print("|       |                   |                    |      |");
		print("|       |                   |                    |      |");
		print("|       |        "+board[6]+"---------"+board[7]+"---------"+board[8]+"           |      |");
		print("|       |         |                   |          |      |");
		print("|       |         |                   |          |      |");
		print(board[9]+"-------"+board[10]+"--------"+board[11]+"                   "+board[12]+"--------"+board[13]+"-------"+board[14]+"    ");
		print("|       |         |                   |          |      |");
		print("|       |         |                   |          |      |");
		print("|       |        "+board[15]+"---------"+board[16]+"---------"+board[17]+"           |      |");
		print("|       |                   |                    |      |");
		print("|       |                   |                    |      |");
		print("|       "+board[18]+"------------------"+board[19]+"------------------"+board[20]+"         |");
		print("|                           |                           |");
		print("|                           |                           |");
		print(board[21]+"--------------------------"+board[22]+"--------------------------"+board[23]+"----");

def drawBoard(window, board):
	# Fields are represented in order as they appear from left to right and from top to bottom.
	# positions of fields (rects 25x25), designed for 800x600 window
	positions = [
		(200, 100),
		(375, 100),
		(575, 100),
		(250, 150),
		(375, 150),
		(525, 150),
		(300, 200),
		(375, 200),
		(475, 200),
		(200, 300),
		(250, 300),
		(300, 300),
		(475, 300),
		(525, 300),
		(575, 300),
		(300, 400),
		(575, 300),
		(475, 400),
		(250, 450),
		(375, 450),
		(525, 450),
		(200, 475),
		(375, 475),
		(575, 475)
	]

	evalColor = lambda val: (255, 0, 0) if val=="1" else ((0, 0, 255) if val=="2" else (0, 255, 0)) # player1: red; player2: blue; free: green

	window.fill((255, 255, 255))

	lineColor = (0, 0, 0)
	pygame.draw.line(window, lineColor, positions[0], positions[2])
	pygame.draw.line(window, lineColor, positions[3], positions[5])
	pygame.draw.line(window, lineColor, positions[6], positions[8])
	pygame.draw.line(window, lineColor, positions[6], positions[15])
	pygame.draw.line(window, lineColor, positions[8], positions[17])
	pygame.draw.line(window, lineColor, positions[15], positions[17])
	pygame.draw.line(window, lineColor, positions[3], positions[18])
	pygame.draw.line(window, lineColor, positions[5], positions[20])
	pygame.draw.line(window, lineColor, positions[18], positions[20])
	pygame.draw.line(window, lineColor, positions[0], positions[21])
	pygame.draw.line(window, lineColor, positions[2], positions[23])
	pygame.draw.line(window, lineColor, positions[21], positions[23])
	pygame.draw.line(window, lineColor, positions[12], positions[14])
	pygame.draw.line(window, lineColor, positions[9], positions[11])

	for i in range(0, len(board)):
		pygame.draw.rect(window, (evalColor(board[i])), Rect(positions[i], (25, 25)))

	pygame.display.update()

def handleEvents():
	for e in pygame.event.get():
		if e.type == QUIT:
			return QUIT

def AI_VS_AI(window, depth1, depth2, heuristic1, heuristic2):

	board = []
	for i in range(24):
		board.append("X")

	evaluation = evaluator()

	doNotEnterStage2 = False
	print("Stage 1")
	for i in range(9):
		if handleEvents() == QUIT:
			doNotEnterStage2 = True
			break

		#boardOutput(board)
		evalBoard = alphaBetaPruning(board, depth1, True, alpha, beta, True, heuristic1)

		if evalBoard.evaluator == float('inf'):
			print("AI Bot 1 has won!")
			doNotEnterStage2 = True
			break
		else:
			board = evalBoard.board

		#boardOutput(board)
		evalBoard = alphaBetaPruning(board, depth2, False, alpha, beta, True, heuristic2)

		if evalBoard.evaluator == float('-inf'):
			print("AI Bot 2 has won!")
			doNotEnterStage2 = True
			break
		else:
			board = evalBoard.board

		drawBoard(window, board)

	drawBoard(window, board)
	if doNotEnterStage2:
		return None

	print("Stage 2")
	while True:
		if handleEvents() == QUIT:
			break

		#boardOutput(board)
		evalBoard = alphaBetaPruning(board, depth1, True, alpha, beta, False, heuristic1)

		if evalBoard.evaluator == float('inf'):
			print("AI Bot 1 has won!")
			break
		else:
			board = evalBoard.board

		#boardOutput(board)
		evaluation = alphaBetaPruning(board, depth2, False, alpha, beta, False, heuristic2)

		if evaluation.evaluator == float('-inf'):
			print("AI Bot 2 has won")
			break
		else:
			board = evaluation.board

		drawBoard(window, board)
	drawBoard(window, board)


if __name__ == "__main__":

	print("Welcome to Nine Mens Morris")
	print("==========================")
	gametype = eval(input("Please enter 1 to start: "))

	while gametype != 1:
		gametype = eval(input("Please enter 1 to start: "))

	pygame.init()
	window = pygame.display.set_mode([800, 600])

	if gametype == 1:
		ai1_depth = int(input("Enter first AI level: "))
		ai2_depth = int(input("Enter second AI level: "))
		AI_VS_AI(window, ai1_depth, ai2_depth, potentialMillsHeuristic, numberOfPiecesHeuristic)

	pygame.quit()
