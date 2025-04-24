import random
import math # For Monte Carlo Search
from itertools import product
from copy import deepcopy

game_board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ']]

def get_legal_moves(board):
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

    Returns (x, y) for a move to play
    """
    legal_moves = get_legal_moves(board)

    if (3, 6) in legal_moves:
        return 3
    
    # If we can win or block a winning move, do that first 
    for move in legal_moves:
        for player in ["X", "O"]:
            temp_board = [row[:] for row in board]
            drop_piece(temp_board, move, player)
            if get_winner(temp_board) == player:
                return move[0]
                    
        # If there are 4 available spots in a column with O, do that
        for x, y in move:
            if 2 < y < 5:
                return x
        # If there are 4 available spots in a row with O, do that
            elif (x + 1, y) in legal_moves and (x + 2, y) in legal_moves:
                if (x + 3, y) in legal_moves:
                    return x 
            elif (x - 1, y) in legal_moves and (x - 2, y) in legal_moves:
                 if (x - 3, y) in legal_moves:
                    return x
        # If no way to win, return random move
        else:
            x = random.randint(0, 7)

            if board[x] == " ":
                return (x)
    return -1

# Creates a "hard agent" using a minimax function
def hard_agent(board, depth, maximizing, highest, lowest):
    # Returns a value for what the outcome of the winner is
    winner = get_winner(board)
    if winner == "X":
        return 1
    elif winner == "O":
        return -1
    elif winner == "T":
        return 0
    
    if maximizing:
        # Starts with lowest possible value for maximizing score
        max_eval = float('-inf')
        # Loop to look for all valid columns available on board
        for col in get_legal_moves(board):
            # Find first empty row in this column (bottom-up)
            for row in reversed(range(6)):
                # Simulate move to find best possible move
                if board[row][col] == " ":
                    board[row][col] = "X"
                    # Looks 3 moves ahead on the board
                    eval = hard_agent(board, depth + 3, False, highest, lowest)
                    # Backtracks so that we can evaluate all options
                    board[row][col] = " "
                    max_eval = max(max_eval, eval)
                    # Update highest possible score
                    highest = max(highest, eval)
                    break
            # If minimizer has a better option, stop evaluating
            if lowest <= highest:
                break
        # Return the best score
        return max_eval
    
    else:
        # Starts with highest possible value for minimizing score
        min_eval = float('inf')
        # Loops through all valid columns
        for col in get_legal_moves(board):
            for row in reversed(range(6)):
                # Simulates minimizing piece
                if board[row][col] == " ":
                    board[row][col] = "O"
                    # Looks 3 moves ahead on the board, next call is maximizer's turn
                    eval = hard_agent(board, depth + 3, True, highest, lowest)
                    board[row][col] = " "
                    # Keeps track of lowest evaluation so far
                    min_eval = min(min_eval, eval)
                    lowest = min(lowest, eval)
                    break
            # If minimizer is worse, stop evaluating
            if lowest <= highest:
                break
        # Return lowest possible score
        return min_eval

def expert_agent(board):
    """
    Expert Agent

    Agent is impossible for the user to beat as it plays perfecting through using a monte carlo search tree
    """
    
    legal_moves = get_legal_moves(board)

    # If we can win or block a winning move, do that first 
    for move in legal_moves:
        for player in ["X", "O"]:
            temp_board = [row[:] for row in board]
            drop_piece(temp_board, move, player)
            if get_winner(temp_board) == player:
                return move[0]
    
    class Node:
        def __init__(self, board, move=None, parent=None):
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
                drop_piece(new_board, move, "X")
                child_node = Node(new_board, move, node)
                node.children.append(child_node)
                return child_node
        # If all moves are expanded return none
        return None
    
    # Simulation - simulates random game from a given game state and returns winner
    def simulate_random_game(board):
        # Create copy of board and itliaze player to X
        temp_board = [row[:] for row in board]
        player = "X"
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
        root = Node(board)
        for _ in range(iterations):
            node = root
            # Selection: Traverse down the tree using best move
            while node.is_fully_expanded() and node.children:
                node = node.best_child()
            # Expansion: If node (move) is not fully expanded, add a new child (game state)
            if not node.is_fully_expanded():
                node = expand_node(node)
            # Simulation: Play a random game from this state
            result = simulate_random_game(node.board)
            # Backpropagation: Update the tree based on the result
            backpropagate(node, result)
        # If no children exist, pick a random legal move
        if not root.children:
            legal_moves = get_legal_moves(board)
            return random.choice(legal_moves) if legal_moves else None
        # Choose the best move based on visit count
        return max(root.children, key=lambda child: child.visits).move

    return mcts(board, iterations=100)

def play_game(difficulty, board):
    piece = input("Please select a column (0-6): ")
    drop_piece(board, int(piece), "O")
    match difficulty:
        case "1":
            return easy_agent(board)
        case "2":
            return intermediate_agent(board)
        case "3":
            best_score = float("-inf")
            best_col = None
            for col in range(7):
                temp_board = [row[:] for row in board]
                row = drop_piece(temp_board, col, "O")
                if row != -1:
                    score = hard_agent(temp_board, 0, False, float("-inf"), float("inf"))
                    if score > best_score:
                        best_score = score
                        best_col = col
            return best_col
        case "4":
            return expert_agent(board)
        case _:
            print("Invalid difficulty selected. Defaulting to Hard.")
            return hard_agent(board)

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

        row = drop_piece(board, col, "X")
        if row == -1:
            print("Column full. Try again.")
            continue

        show(board)
        result = get_winner(board)
        if result == "X":
            print("You win!")
            break
        elif result == "T":
            print("It's a tie!")
            break

        ai_col = play_game(opp_difficulty, board)
        drop_piece(board, ai_col, "O")
        print(f"AI chose column {ai_col}")
        show(board)

        result = get_winner(board)
        if result == "O":
            print("AI wins!")
            break
        elif result == "T":
            print("It's a tie!")
            break

if __name__ == "__main__":
    player = input("Enter player name: ")
    opp_difficulty = input("Opponent difficulty (please type the number that corresponds with the level you would like):\nEasy(1)\tIntermediate(2)\tHard(3)\tExpert(4): ")
    show(game_board)
    play_game(opp_difficulty, game_board)