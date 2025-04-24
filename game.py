import random
import math # For Monte Carlo Search
from itertools import product
from copy import deepcopy

game_board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ']]

def get_legal_moves(board):
    """
    Returns a list of columns where a move can be legally made.
    A move is legal if the top cell in the column is empty.
    """

    legal_moves = []
    for col in range(7):
        if board[0][col] == " ":
            legal_moves.append(col)
    return legal_moves

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
    Easy Agent

    Very basic agent that simply selects a random legal move

    Returns a column value
    """

    while True:
        x = random.randint(0, 6)

        if board[0][x] == " ":
            return (x)

def intermediate_agent(board):
    """
    Intermediate Agent

    Plays a piece that has an opportunity to get 4 in a row
    If it gets blocked, starts a new column

    Returns column for a move to play
    """
    legal_moves = get_legal_moves(board)

    # If we can win or block a winning move, do that first 
    for move in legal_moves:
        for player in ["X", "O"]:
            temp_board = [row[:] for row in board]
            drop_piece(temp_board, move, player)
            if get_winner(temp_board) == player:
                return move
                    
    # Try to create a vertical, horizontal, or diagonal threat
    for move in legal_moves:
        temp_board = [row[:] for row in board]
        drop_piece(temp_board, move, "X")  # Try the move for the AI (X)

        # Check if this move creates a vertical "4 in a row" (if possible)
        for row in range(5, -1, -1):  # Start from the bottom
            if temp_board[row][move] == " ":
                if row <= 2:  
                    if temp_board[row+1][move] == "X" and temp_board[row+2][move] == "X" and temp_board[row+3][move] == "X":
                        return move

        # Check if this move creates a horizontal "4 in a row"
        for row in range(6):
            for col in range(4):  
                if temp_board[row][col] == "X" and temp_board[row][col+1] == "X" and temp_board[row][col+2] == "X" and temp_board[row][col+3] == "X":
                    return move

        # If no winning move, return random move
        if len(legal_moves) > 0:
            return random.choice(legal_moves)
    return -1


def expert_agent(board):
    """
    Expert Agent

    Agent plays perfectly through using a monte carlo search tree but is still beatable since the user goes first
    """
    
    legal_moves = get_legal_moves(board)

    # If we can win or block a winning move, do that first 
    for move in legal_moves:
        temp_board = [row[:] for row in board]
        drop_piece(temp_board, move, "X")
        if get_winner(temp_board) == "X":
            return move
    for move in legal_moves:
        temp_board = [row[:] for row in board]
        drop_piece(temp_board, move, "O")
        if get_winner(temp_board) == "O":
            return move
    
    class Node:
        def __init__(self, board, move=None, parent=None, player = "O"):
            # Copy of board
            self.board = [row[:] for row in board]  
            # Last move
            self.move = move  
            # Assign parent and child nodes which are all different game states
            self.parent = parent  
            self.children = []  
            # Number of times this node has been visited
            self.visits = 0  
            # Number of wins from this board/node
            self.wins = 0  
            # Whose turn it is at the particular node
            self.player = player

        # Check to see if all possible moves have been expanded
        def is_fully_expanded(self):
            return len(self.children) == len(get_legal_moves(self.board))
        
        # Selection Algorithm - Use Upper Confidence Bound for Trees as selection appraoch
        def best_child(self, exploration_weight=1.4):
            return max(
                self.children,
                key=lambda child: (child.wins / (child.visits + 1e-6)) +
                exploration_weight * math.sqrt(math.log(self.visits + 1) / (child.visits + 1e-6))
            )
        
    # Expansion - See new possible game states for a given move
    def expand_node(node):
        # Get all moves
        legal_moves = get_legal_moves(node.board)
        # Get moves already explored
        existing_moves = {child.move for child in node.children}
        # Find an unexplored move and add child nodes (new game states) to it
        for move in legal_moves:
            if move not in existing_moves:
                new_board = [row[:] for row in node.board]
                next_player = "O" if node.player == "X" else "X"
                drop_piece(new_board, move, node.player)
                child_node = Node(new_board, move, node, next_player)
                node.children.append(child_node)
                return child_node
        # If all moves are expanded return none
        return None
    
    # Simulation - simulates random game from a given game state and returns winner
    def simulate_random_game(board, current_player):
        # Create copy of board 
        temp_board = [row[:] for row in board]
        player = "X" if current_player == "O" else "O"
        # create infinite loop that will break when game ends
        while True:
            # Get all possible moves
            moves = get_legal_moves(temp_board)
            # If there are no moves return a tie
            if not moves:
                return "T"
            # Make a random move 
            move = random.choice(moves)
            drop_piece(temp_board, move, player)
            # See if random move won the game
            winner = get_winner(temp_board)
            if winner:
                return winner
            # Switch to other player and continue game
            player = "O" if player == "X" else "X"
    
    # Backpropagte - updates stats after a simulation
    def backpropagate(node, result):
        while node:
            node.visits += 1
            if result == "X":
                node.wins += 1
            elif result == "O":
                node.wins -= 1
            node = node.parent

    # Function that uses Monte Carlo Search Tree class to determine best move
    def mcts(board, iterations):
        root = Node(board, player="O")
        for _ in range(iterations):
            node = root
            # Selection: Traverse down the tree using best move
            while node.is_fully_expanded() and node.children:
                node = node.best_child()
            # Expansion: If node (move) is not fully expanded, add a new child (game state)
            if not node.is_fully_expanded():
                node = expand_node(node)
            # Simulation: Play a random game from this state
            result = simulate_random_game(node.board, node.player)
            # Backpropagation: Update the tree based on the result
            backpropagate(node, result)
        # If no children exist, pick a random legal move
        if not root.children:
            legal_moves = get_legal_moves(board)
            return random.choice(legal_moves) if legal_moves else None
        # Choose the best move based on visit count
        return max(root.children, key=lambda child: child.visits).move

    return mcts(board, iterations=500)

def play_game(difficulty, board):
    match difficulty:
        case "1":
            return easy_agent(board)
        case "2":
            return intermediate_agent(board)
        case "3":
            return expert_agent(board)
        case _:
            print("Invalid difficulty selected. Defaulting to Expert.")
            return expert_agent(board)

def main_game_loop():
    board = [[' ' for _ in range(7)] for _ in range(6)]
    show(board)

    while True:
        try:
            col = int(input("Enter column (0-6): "))
            if not 0 <= col <= 6:
                print("Invalid column. Try again.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue

        row = drop_piece(board, col, "O")
        if row == -1:
            print("Column full. Try again.")
            continue

        show(board)
        result = get_winner(board)
        if result == "O":
            print("You win!")
            break
        elif result == "T":
            print("It's a tie!")
            break

        ai_col = play_game(opp_difficulty, board)
        drop_piece(board, ai_col, "X")
        print(f"AI chose column {ai_col}")
        show(board)

        result = get_winner(board)
        if result == "X":
            print("The AI wins!")
            break
        elif result == "T":
            print("It's a tie!")
            break

if __name__ == "__main__":
    player = input("Enter player name: ")
    opp_difficulty = input("Opponent difficulty (please type the number that corresponds with the level you would like):\nEasy(1)\tIntermediate(2)\tExpert(3): ")
    main_game_loop()

