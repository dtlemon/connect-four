import random
from itertools import product
from copy import deepcopy

game_board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ']]

def get_legal_moves(board):
    """
    >>> get_legal_moves([['X','X','X','X','X','X','X'],['X',' ','X','X','X','X','X'],['X',' ','X','X','X','X','X'],['X',' ','X','X','X','X','X'],['X',' ','X','X','X','X','X'],['X',' ','X','X','X','X','X']])
    [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]

    >>> len(get_legal_moves([[' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' ']]))
    42

    """

    return [(x, y) for x, y in product(range(7), range(6)) if board[y][x] == " "]

def show(board):
    """
    Displays a 7x6 Connect Four board.
    """

    print(" 0 1 2 3 4 5 6")  # Column headers
    print("+-------------+")

    for y in range(0, 6):  # 6 rows (from top to bottom)
        print("|" + " ".join(board[y]) + "|")

    print("+-------------+")

def get_winner(board):
    """
    Returns the winner for a board state (X, O or no winner)

    >>> get_winner([["X", "X", "X", "X", " ", " ", " "],
    ...     [" ", " ", " ", " ", " ", " ", " "],
    ...     [" ", " ", " ", " ", " ", " ", " "],
    ...     [" ", " ", " ", " ", " ", " ", " "],
    ...     [" ", " ", " ", " ", " ", " ", " "],
    ...     [" ", " ", " ", " ", " ", " ", " "]])
    'X'
    >>> get_winner([["O", "O", "O", "O", " ", " ", " "],
    ...     [" ", " ", " ", " ", " ", " ", " "],
    ...     [" ", " ", " ", " ", " ", " ", " "],
    ...     [" ", " ", " ", " ", " ", " ", " "],
    ...     [" ", " ", " ", " ", " ", " ", " "],
    ...     [" ", " ", " ", " ", " ", " ", " "]])
    'O'
    >>> get_winner([["X", " ", " ", " ", " ", " ", " "],
    ...     ["X", " ", " ", " ", " ", " ", " "],
    ...     ["X", " ", " ", " ", " ", " ", " "],
    ...     ["X", " ", " ", " ", " ", " ", " "],
    ...     [" ", " ", " ", " ", " ", " ", " "],
    ...     [" ", " ", " ", " ", " ", " ", " "]])
    'X'
    >>> get_winner([[" ", " ", " ", " ", " ", " ", " "],
    ...     [" ", " ", " ", " ", " ", " ", " "],
    ...     [" ", " ", " ", " ", " ", " ", " "],
    ...     [" ", " ", " ", " ", " ", " ", " "],
    ...     ["O", " ", " ", " ", " ", " ", " "],
    ...     ["X", "O", "X", " ", " ", " ", " "]])
    
    >>> get_winner([
    ...     ["X", "O", "X", "O", "X", "O", "X"],
    ...     ["O", "X", "X", "O", "X", "X", "O"],
    ...     ["X", "X", "O", "O", "O", "X", "O"],
    ...     ["O", "O", "O", "X", "O", "X", "O"],
    ...     ["X", "X", "X", "O", "X", "O", "X"],
    ...     ["O", "O", "O", "X", "O", "X", "X"]])
    'T'
    >>> get_winner([[" ", " ", " ", " ", " ", " ", " "],
    ...     [" ", " ", " ", " ", " ", " ", " "],
    ...     [" ", " ", " ", "X", " ", " ", " "],
    ...     [" ", " ", "X", " ", " ", " ", " "],
    ...     ["O", "X", "O", " ", " ", " ", " "],
    ...     ["X", "O", "O", " ", " ", " ", " "]])
    'X'
    >>> get_winner([[" ", " ", " ", " ", " ", " ", " "],
    ...     [" ", " ", " ", " ", " ", " ", " "],
    ...     ["O", " ", " ", "", " ", " ", " "],
    ...     ["X", "O", "X", " ", " ", " ", " "],
    ...     ["O", "X", "O", " ", " ", " ", " "],
    ...     ["X", "O", "O", "O", " ", " ", " "]])
    'O'

    """

    # Check for Horizontal wins
    for row in range(6):
        for col in range(7 - 3):
            if board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3] != " ":
                return board[row][col]
            
    # Check for Vertical wins
    for row in range(6 - 3):
        for col in range(7):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] != " ":
                return board[row][col]
            
    # Check for Diagonal wins that go bottom left to top right
    for row in range(3, 6):
        for col in range(7 - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] != " ":
                return board[row][col]

    # Check for diagonal wins that go bottom right to top left
    for row in range(6 - 3):
        for col in range(7 - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] != " ":
                return board[row][col]

    # Check for tie or incomplete game
    for row in range(6):
        for col in range(7):
            if board[row][col] == " ":
                return None        
    return "T"
  
#Creates function for dropping a piece into the Connect Four board
def drop_piece(board, column, player_symbol):
    for row in reversed(range(6)):
        if board[row][column] == " ":
            board[row][column] = player_symbol
            return row
    return -1

def easy_agent(board):
    """
    Random Agent

    Very basic agent that simply selects a random legal move
    """

    while True:
        x = random.randint(0, 7)

        if board[x] == " ":
            return (x)

def hard_agent(board, depth, maximizing, highest, lowest):
    winner = get_winner(board)
    if winner == "X":
        return 1
    elif winner == "O":
        return -1
    elif winner == "T":
        return 0
    
    if maximizing:
        max_eval = float('-inf')
        for col in get_legal_moves(board):
            # Find first empty row in this column (bottom-up)
            for row in reversed(range(6)):
                if board[row][col] == " ":
                    board[row][col] = "X"
                    eval = hard_agent(board, depth + 1, False, highest, lowest)
                    board[row][col] = " "
                    max_eval = max(max_eval, eval)
                    highest = max(highest, eval)
                    break  # Done with this column
            if lowest <= highest:
                break
        return max_eval
    
    else:
        min_eval = float('inf')
        for col in get_legal_moves(board):
            for row in reversed(range(6)):
                if board[row][col] == " ":
                    board[row][col] = "O"
                    eval = hard_agent(board, depth + 1, True, highest, lowest)
                    board[row][col] = " "
                    min_eval = min(min_eval, eval)
                    lowest = min(lowest, eval)
                    break
            if lowest <= highest:
                break
        return min_eval

def expert_agent(board):
    legal_moves = get_legal_moves(board)

    for move in legal_moves:
        for player in ["X", "O"]:
            temp_board = [row[:] for row in board]
            temp_board[move[1]][move[0]] = player
            if get_winner(temp_board) == player:
                return move if player == "X" else move 

if __name__ == "__main__":
    player = input("Enter player name: ")
    opp_difficulty = input("Opponent difficulty (please type the number that corresponds with the level you would like):\nEasy(1)\tIntermediate(2)\tExpert(3): ")

    show(game_board)
