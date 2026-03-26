import random
from typing import List, Optional, Tuple

Board = List[List[str]]


def create_board() -> Board:
    return [[" " for _ in range(3)] for _ in range(3)]


def print_board(board: Board) -> None:
    print("\n")
    for i, row in enumerate(board):
        print(" | ".join(row))
        if i < 2:
            print("-" * 9)
    print("\n")


def check_winner(board: Board) -> Optional[str]:
    lines = []
    for i in range(3):
        lines.append(board[i])  # row
        lines.append([board[0][i], board[1][i], board[2][i]])  # column
    lines.append([board[0][0], board[1][1], board[2][2]])  # diag
    lines.append([board[0][2], board[1][1], board[2][0]])  # diag

    for line in lines:
        if line[0] != " " and line[0] == line[1] == line[2]:
            return line[0]

    if all(cell != " " for row in board for cell in row):
        return "Tie"

    return None


def available_moves(board: Board) -> List[Tuple[int, int]]:
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]


def minimax(board: Board, player: str, depth: int = 0) -> Tuple[int, Optional[Tuple[int, int]]]:
    winner = check_winner(board)
    if winner == "X":
        return 10 - depth, None
    elif winner == "O":
        return depth - 10, None
    elif winner == "Tie":
        return 0, None

    moves = available_moves(board)
    if player == "X":
        best_score = -float("inf")
        best_move = None
        for move in moves:
            r, c = move
            board[r][c] = player
            score, _ = minimax(board, "O", depth + 1)
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
            score, _ = minimax(board, "X", depth + 1)
            board[r][c] = " "
            if score < best_score:
                best_score = score
                best_move = move
        return best_score, best_move


def player_move(board: Board, player: str) -> None:
    while True:
        try:
            move = input(f"Enter your move {player} (row col, 1-3 each): ")
            r, c = map(int, move.strip().split())
            r -= 1
            c -= 1
            if (r, c) in available_moves(board):
                board[r][c] = player
                break
            else:
                print("Cell is already occupied. Try again.")
        except Exception:
            print("Invalid input. Use format: row col (numbers 1-3).")


def ai_move(board: Board, player: str) -> None:
    _, move = minimax(board, player)
    if move:
        r, c = move
        board[r][c] = player
        print(f"AI ({player}) moves at row {r+1}, col {c+1}")


def play_game() -> None:
    board = create_board()
    human_player = ""
    ai_player = ""
    while human_player not in {"X", "O"}:
        human_player = input("Choose your symbol (X/O): ").upper()
    ai_player = "O" if human_player == "X" else "X"

    current = "X" 
    print_board(board)

    while True:
        if current == human_player:
            player_move(board, human_player)
        else:
            ai_move(board, ai_player)

        print_board(board)
        winner = check_winner(board)
        if winner:
            if winner == "Tie":
                print("It's a tie!")
            else:
                print(f"{winner} wins!")
            break

        current = ai_player if current == human_player else human_player


if __name__ == "__main__":
    play_game()