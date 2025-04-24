import numpy as np
import time
import random

class TicTacToe:
    def __init__(self, difficulty="hard"):
        # Initialize the 3x3 board with zeros (empty spaces)
        self.board = np.zeros((3, 3), dtype=int)
        # 1 represents 'X', -1 represents 'O', 0 represents empty
        self.player = 1  # Player 1 ('X') starts
        self.difficulty = difficulty  # "easy" or "hard"

    def available_moves(self):
        """Returns a list of available (row, col) positions on the board"""
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i, j] == 0:
                    moves.append((i, j))
        return moves

    def make_move(self, position, player=None):
        """Makes a move on the board at the specified position"""
        if player is None:
            player = self.player

        row, col = position
        if self.board[row, col] != 0:
            return False  # Invalid move, spot already taken

        self.board[row, col] = player
        self.player = -player  # Switch player
        return True

    def undo_move(self, position):
        """Undoes a move on the board at the specified position"""
        row, col = position
        self.player = -self.player  # Switch back to previous player
        self.board[row, col] = 0  # Set position back to empty

    def check_winner(self):
        """Checks if there's a winner or if the game is a draw
        Returns:
            1 if 'X' wins, -1 if 'O' wins, 0 if draw, None if game is ongoing
        """
        # Check rows
        for i in range(3):
            if abs(np.sum(self.board[i, :])) == 3:
                return self.board[i, 0]

        # Check columns
        for i in range(3):
            if abs(np.sum(self.board[:, i])) == 3:
                return self.board[0, i]

        # Check diagonals
        if abs(np.sum([self.board[i, i] for i in range(3)])) == 3:
            return self.board[0, 0]
        if abs(np.sum([self.board[i, 2-i] for i in range(3)])) == 3:
            return self.board[0, 2]

        # Check if board is full (draw)
        if len(self.available_moves()) == 0:
            return 0

        # Game is ongoing
        return None

    def is_terminal(self):
        """Checks if the game is over (either a win or a draw)"""
        return self.check_winner() is not None

    def display_board(self):
        """Displays the board in a user-friendly format"""
        symbols = {1: 'X', -1: 'O', 0: ' '}
        print("\n")
        for i in range(3):
            print(" " + " | ".join([symbols[self.board[i, j]] for j in range(3)]))
            if i < 2:
                print("-" * 9)
        print("\n")

    def minimax(self, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
        """Minimax algorithm with alpha-beta pruning for determining the best move
       
        Args:
            depth: Current depth in the game tree
            is_maximizing: True if current player is maximizing, False if minimizing
            alpha: Alpha value for alpha-beta pruning
            beta: Beta value for alpha-beta pruning
           
        Returns:
            best_score: The best score possible from the current position
        """
        # First check if game is over
        winner = self.check_winner()
        if winner is not None:
            return winner  # Return utility value (1 for X win, -1 for O win, 0 for draw)

        # If maximizing player's turn
        if is_maximizing:
            best_score = float('-inf')
            for move in self.available_moves():
                self.make_move(move, 1)  # Make move for 'X'
                score = self.minimax(depth + 1, False, alpha, beta)
                self.undo_move(move)  # Undo the move
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  # Beta cutoff
            return best_score
        # If minimizing player's turn
        else:
            best_score = float('inf')
            for move in self.available_moves():
                self.make_move(move, -1)  # Make move for 'O'
                score = self.minimax(depth + 1, True, alpha, beta)
                self.undo_move(move)  # Undo the move
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            return best_score

    def best_move(self, player):
        """Determines the best move for the given player based on difficulty"""
        # For easy mode, 70% of the time make a random move
        if self.difficulty == "easy" and random.random() < 0.7:
            available = self.available_moves()
            return random.choice(available) if available else None
           
        # Original minimax logic for hard mode or 30% of the time in easy mode
        best_score = float('-inf') if player == 1 else float('inf')
        best_move = None
       
        # Try each available move and pick the best one
        for move in self.available_moves():
            self.make_move(move, player)
           
            # Get score using minimax algorithm
            if player == 1:  # Maximizing player
                score = self.minimax(0, False)
                if score > best_score:
                    best_score = score
                    best_move = move
            else:  # Minimizing player
                score = self.minimax(0, True)
                if score < best_score:
                    best_score = score
                    best_move = move
                   
            self.undo_move(move)
           
        return best_move

def play_game():
    # Game mode selection
    print("Select game mode:")
    print("1. Human vs Computer (Human goes first - Easy)")
    print("2. Human vs Computer (Human goes first - Hard)")
    print("3. Computer vs Human (Computer goes first)")
    print("4. Computer vs Computer")
   
    while True:
        try:
            mode = int(input("Enter mode (1-4): "))
            if mode in [1, 2, 3, 4]:
                break
            else:
                print("Please enter a valid mode (1-4).")
        except ValueError:
            print("Please enter a number (1-4).")
   
    # Create game with appropriate difficulty
    difficulty = "easy" if mode == 1 else "hard"
    game = TicTacToe(difficulty)
   
    # Main game loop
    current_player = 1  # X starts
   
    while not game.is_terminal():
        game.display_board()
       
        # Human's turn
        if (mode in [1, 2] and current_player == 1) or (mode == 3 and current_player == -1):
            print(f"Player {'X' if current_player == 1 else 'O'}'s turn")
            while True:
                try:
                    row = int(input("Enter row (0-2): "))
                    col = int(input("Enter column (0-2): "))
                    if 0 <= row <= 2 and 0 <= col <= 2 and game.board[row, col] == 0:
                        break
                    else:
                        print("Invalid move. Please try again.")
                except ValueError:
                    print("Please enter valid numbers.")
           
            game.make_move((row, col), current_player)
       
        # Computer's turn
        else:
            difficulty_text = "Easy" if game.difficulty == "easy" else "Hard"
            print(f"Computer ({('X' if current_player == 1 else 'O')}) is thinking... [{difficulty_text} mode]")
            time.sleep(1)  # Add a small delay to make it seem like the computer is "thinking"
            move = game.best_move(current_player)
            print(f"Computer plays at position: {move}")
            game.make_move(move, current_player)
       
        current_player = -current_player
   
    # Game over
    game.display_board()
    winner = game.check_winner()
    if winner == 1:
        print("X wins!")
    elif winner == -1:
        print("O wins!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    play_game()

