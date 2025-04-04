import random
from itertools import product
from copy import deepcopy

game_board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ']]

def get_legal_moves(board):
    """
    >>> get_legal_moves([['X','X','X','X','X','X','X'],['X',' ','X','X','X','X','X'],['X',' ','X','X','X','X','X'],['X',' ','X','X','X','X','X'],['X',' ','X','X','X','X','X'],['X',' ','X','X','X','X','X']])
    [(1, 1)]

    >>> len(get_legal_moves([[' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' ']]))
    9

    """

    return [(x, y) for x, y in product(range(7), range(6)) if board[y][x] == " "]

def random_agent(board):
    """
    Random Agent

    Very basic agent that simply selects a random legal move
    """

    while True:
        x = random.randint(0, 7)
        y = random.randint(0, 6)

        if board[y][x] == " ":
            return (x, y)


def get_winner(board):
    """
    Returns the winner for a board state (X, O or no winner)

    >>> get_winner([['X','X','X'],['O','O','X'],['X','O','O']])
    'X'

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

