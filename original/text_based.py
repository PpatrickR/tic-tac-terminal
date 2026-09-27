import random
import sys
from typing import List, Optional, Tuple

# Board management
class Board:
    def __init__(self):
        # Initialize a 3x3 grid of empty spaces
        self.grid: List[List[str]] = [[" "]*3 for _ in range(3)]

    def display(self):
        # Print current board with row/col labels
        print("\n   1   2   3")
        for i, row in enumerate(self.grid, start=1):
            print(f"{i}  " + " | ".join(row))
            if i < 3:
                print("  ---+---+---")
        print()

    def mark(self, row: int, col: int, symbol: str) -> bool:
        # Place symbol if cell is empty
        if self.grid[row][col] == " ":
            self.grid[row][col] = symbol
            return True
        return False

    def check_winner(self) -> Optional[str]:
        lines = []
        # Rows, columns, diagonals
        lines.extend(self.grid)
        lines.extend([[self.grid[r][c] for r in range(3)] for c in range(3)])
        lines.append([self.grid[i][i] for i in range(3)])
        lines.append([self.grid[i][2-i] for i in range(3)])
        for line in lines:
            if line[0] != " " and all(cell == line[0] for cell in line):
                return line[0]
        return None

    def is_full(self) -> bool:
        return all(cell != " " for row in self.grid for cell in row)

# AI logic
def random_move(board: Board) -> Tuple[int, int]:
    empties = [(r, c) for r in range(3) for c in range(3) if board.grid[r][c] == " "]
    return random.choice(empties)

def minimax(board: Board, depth: int, is_maximizing: bool, symbol: str) -> int:
    opponent = "O" if symbol == "X" else "X"
    winner = board.check_winner()
    if winner == symbol:
        return 1
    if winner == opponent:
        return -1
    if board.is_full():
        return 0

    if is_maximizing:
        best = -sys.maxsize
        for r in range(3):
            for c in range(3):
                if board.grid[r][c] == " ":
                    board.grid[r][c] = symbol
                    score = minimax(board, depth+1, False, symbol)
                    board.grid[r][c] = " "
                    best = max(best, score)
        return best
    else:
        worst = sys.maxsize
        for r in range(3):
            for c in range(3):
                if board.grid[r][c] == " ":
                    board.grid[r][c] = opponent
                    score = minimax(board, depth+1, True, symbol)
                    board.grid[r][c] = " "
                    worst = min(worst, score)
        return worst

def minimax_move(board: Board, symbol: str) -> Tuple[int, int]:
    best_score = -sys.maxsize
    best_move = (0, 0)
    for r in range(3):
        for c in range(3):
            if board.grid[r][c] == " ":
                board.grid[r][c] = symbol
                score = minimax(board, 0, False, symbol)
                board.grid[r][c] = " "
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
    return best_move

# Command-line interface
def get_move_input(player: str) -> Tuple[int, int]:
    while True:
        try:
            coords = input(f"Player {player}, enter row and column (e.g. 2 3): ").split()
            if len(coords) != 2:
                raise ValueError
            r, c = map(int, coords)
            if r not in [1,2,3] or c not in [1,2,3]:
                raise ValueError
            return r-1, c-1
        except ValueError:
            print("Invalid input. Please enter two numbers between 1 and 3 separated by a space.")

def select_mode() -> Tuple[str, Optional[str]]:
    print("Select game mode:")
    print("1) Player vs Player")
    print("2) Player vs Computer (Easy)")
    print("3) Player vs Computer (Hard)")
    choice = input("Enter 1, 2, or 3: ").strip()
    return {
        "1": ("P", None),
        "2": ("C", "easy"),
        "3": ("C", "hard")
    }.get(choice, ("P", None))

def main():
    board = Board()
    opponent_type, ai_level = select_mode()
    current = "X"
    board.display()

    while True:
        if opponent_type == "C" and current == "O":
            # AI turn
            if ai_level == "easy":
                r, c = random_move(board)
            else:
                r, c = minimax_move(board, "O")
            print(f"Computer places O at {r+1}, {c+1}")
        else:
            r, c = get_move_input(current)

        if not board.mark(r, c, current):
            print("Cell occupied, try again.")
            continue

        board.display()
        winner = board.check_winner()
        if winner:
            print(f"Game Over! {winner} wins!")
            break
        if board.is_full():
            print("Game Over! It's a draw.")
            break

        current = "O" if current == "X" else "X"

if __name__ == "__main__":
    main()