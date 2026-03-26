import random
import time
from typing import List, Optional, Tuple

Board = List[List[str]]


def create_board() -> Board:
    """Initialize empty 3x3 board."""
    return [[" " for _ in range(3)] for _ in range(3)]


def print_board(board: Board) -> None:
    """Print the Tic-Tac-Toe board."""
    print("\n")
    for i, row in enumerate(board):
        print(" | ".join(row))
        if i < 2:
            print("-" * 9)
    print("\n")


def check_winner(board: Board) -> Optional[str]:
    """Return 'X' or 'O' if there's a winner, or 'Tie'/'None'."""
    lines = []

    # Rows, columns
    for i in range(3):
        lines.append(board[i])  # row
        lines.append([board[0][i], board[1][i], board[2][i]])  # column

    # Diagonals
    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])

    for line in lines:
        if line[0] != " " and line[0] == line[1] == line[2]:
            return line[0]

    if all(cell != " " for row in board for cell in row):
        return "Tie"

    return None


def available_moves(board: Board) -> List[Tuple[int, int]]:
    """Return list of empty cells."""
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]


def minimax(board: Board, player: str, depth: int = 0, max_depth: Optional[int] = None) -> Tuple[int, Optional[Tuple[int, int]]]:
    """
    Minimax algorithm.
    Returns (score, move)
    """
    winner = check_winner(board)
    if winner == "X":
        return 10 - depth, None
    elif winner == "O":
        return depth - 10, None
    elif winner == "Tie":
        return 0, None

    if max_depth is not None and depth >= max_depth:
        return 0, None  # shallow evaluation

    moves = available_moves(board)
    if player == "X":
        best_score = -float("inf")
        best_move = None
        for move in moves:
            r, c = move
            board[r][c] = player
            score, _ = minimax(board, "O", depth + 1, max_depth)
            board[r][c] = " "
            if score > best_score:
                best_score = score
                best_move = move
        return best_score, best_move
    else:
        best_score = float("inf")
        best_move = None
        for move in moves:
            r, c = move
            board[r][c] = player
            score, _ = minimax(board, "X", depth + 1, max_depth)
            board[r][c] = " "
            if score < best_score:
                best_score = score
                best_move = move
        return best_score, best_move


def player_move(board: Board, player: str, use_full_minimax: bool = True) -> None:
    """Make AI move for given player."""
    if use_full_minimax:
        _, move = minimax(board, player)
    else:
        # Limited depth minimax or random for weaker AI
        _, move = minimax(board, player, max_depth=2)
        if move is None:
            move = random.choice(available_moves(board))
    if move:
        r, c = move
        board[r][c] = player


def simulate_game(step_delay: float = 1.0) -> None:
    """Simulate AI vs AI Tic-Tac-Toe game."""
    board = create_board()
    players = [("X", True), ("O", False)]  # (symbol, use_full_minimax)
    turn = 0

    print("Starting Tic-Tac-Toe AI vs AI!\nX = Player 1 (strong), O = Player 2 (weaker)\n")
    print_board(board)
    time.sleep(step_delay)

    while True:
        symbol, strong_ai = players[turn % 2]
        print(f"Turn: {symbol}")
        player_move(board, symbol, use_full_minimax=strong_ai)
        print_board(board)
        time.sleep(step_delay)

        winner = check_winner(board)
        if winner:
            if winner == "Tie":
                print("Result: It's a tie!")
            else:
                print(f"Winner: {winner}!")
            break

        turn += 1


if __name__ == "__main__":
    simulate_game()