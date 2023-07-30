from random import randint
from math import inf

PLAYER = 0
COMPUTER = 1

def main():
	board = [[' ' for i in range(7)] for j in range(6)]
	print_board(board)
	turn = randint(0, 1)
	f = open("player_input.txt", "w")
	if turn == PLAYER:
		print('Player starts')
	else:
		print('Computer starts')
	while True:
		if turn == PLAYER:
			player_move(board, f)
			if check_for_win(board, 'X') == True:
				print_board(board)
				print('Player wins!')
				break
			turn = COMPUTER
		else:
			eval, temp = minimax(board, 5, True)
			print(eval)
			for idx, i in enumerate(temp):
				if i != board[idx]:
					for j in range(7):
						if i[j] != board[idx][j]:
							print('Computer placed in column ' + str(j + 1))
					board[idx] = i
					break
			if check_for_win(board, 'O') == True:
				print_board(board)
				print('Computer wins!')
				break
			turn = PLAYER
		print_board(board)


def minimax(board, depth, maximum):
	if depth == 0:
		result = evaluate_state(board)
		return result, None
	
	if maximum:
		max_eval = float('-inf')
		best_move = None
		for move in generate_moves(board, 'O'):
			evaluation, _ = minimax(move, depth - 1, False)
			if evaluation > max_eval:
				max_eval = evaluation
				best_move = move
		return max_eval, best_move
	else:
		min_eval = float('inf')
		best_move = None
		for move in generate_moves(board, 'X'):
			evaluation, _ = minimax(move, depth - 1, True)
			if evaluation < min_eval:
				min_eval = evaluation
				best_move = move

		return min_eval, best_move

def generate_moves(board, move):
	moves = []
	for col in range(1, 8):
		if valid_move(board, col):
			new_board = [row[:] for row in board]
			row = get_row(board, col)
			new_board[row][col - 1] = move
			moves.append(new_board)
	return moves
	
def evaluate_state(board):
	# Check for a horizontal pattern
	if check_for_win(board, 'X'):
		print_board(board)
		return -100
	elif check_for_win(board, 'O'):
		print_board(board)
		return 100

	cpu = 0
	player = 0
	for row in range(6):
		for col in range(4):
			if board[row][col] == board[row][col+1] == board[row][col+2] == 'X':
				player += 1
			elif board[row][col] ==  board[row][col+1] ==  board[row][col+2] == 'O':
				cpu += 1

	# Check for a vertical pattern
	for col in range(7):
		for row in range(3):
			if board[row][col] ==  board[row+1][col] ==  board[row + 2][col] == 'X':
				player += 1
			elif board[row][col] ==  board[row + 1][col] ==  board[row + 2][col] == 'O':
				cpu += 1

	# Check for a diagonal pattern (bottom-left to top-right)
	for row in range(3):
		for col in range(4):
			if board[row][col] ==  board[row+1][col+1] ==  board[row+2][col+2] == 'X':
				player += 1
			elif board[row][col] ==  board[row+1][col+1] ==  board[row+2][col+2] == 'O':
				cpu += 1

	# Check for a diagonal pattern (bottom-right to top-left)
	for row in range(3):
		for col in range(3, 7):
			if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == PLAYER:
				player += 1
			elif board[row][col] == board[row+1][col-1] == board[row+2][col-2] == COMPUTER:
				cpu += 1

	return cpu - player
				
def check_for_win(board, player):
	# Check for a horizontal win
	for row in range(6):
		for col in range(4):
			if board[row][col] ==  board[row][col+1] ==  board[row][col+2] ==  board[row][col+3] == player:
				print('horiztonal win')
				return True

	# Check for a vertical win
	for col in range(7):
		for row in range(3):
			if board[row][col] ==  board[row+1][col] ==  board[row+2][col] ==  board[row+3][col] == player:
				print('vertical win')
				return True

	# Check for a diagonal win (bottom-right to top-left)
	for row in range(3):
		for col in range(4):
			if board[row][col] ==  board[row+1][col+1] ==  board[row+2][col+2] == board[row+3][col+3] == player:
				print('diagonal win, bottom right')
				return True

	# Check for a diagonal win (bottom-left to top-right)
	for row in range(3):
		for col in range(3, 7):
			if board[row][col] ==  board[row+1][col-1] ==  board[row+2][col-2] ==  board[row+3][col-3] == player:
				print('diagonal win bottom left')
				return True

	return False


def player_move(board, f):
	print('input a column')
	col = int(input())
	f.write(str(col) + '\n')
	while not valid_move(board, col):
		print('invalid move, try again')
		col = int(input())
	row = get_row(board, col)
	print('player placed in column ' + str(col))
	board[row][col - 1] = 'X'



def print_board(board):
	for i in range(6):
		print('|', end='')
		for j in range(7):
			print(board[i][j], end='|')
		print()
	print('---------------')
	print(' 1 2 3 4 5 6 7')

def valid_move(board, col):
	if col < 1 or col > 7:
		return False
	if board[0][col - 1] != ' ':
		return False
	return True

def get_row(board, col):
	for i in range(5, -1, -1):
		if board[i][col - 1] == ' ':
			return i
	return -1

if __name__ == '__main__':
	main()