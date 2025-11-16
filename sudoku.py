# Developed by phoenix marie. — Further improved & optimized

from __future__ import annotations
import sys
from typing import List, Optional, Set, Tuple


Board = List[List[int]]  # -1 denotes empty


class Sudoku:
    def __init__(self, board: Board):
        self.board = board

        # Constraints tracked as sets for O(1) membership checks
        self.rows = [set() for _ in range(9)]
        self.cols = [set() for _ in range(9)]
        self.boxes = [set() for _ in range(9)]

        # Pre-load constraints
        for r in range(9):
            for c in range(9):
                v = board[r][c]
                if v != -1:
                    if not self._safe_to_place(r, c, v):
                        raise ValueError("Initial board violates Sudoku rules")
                    self._add(r, c, v)

    # -------------------
    # Constraint handling
    # -------------------

    def _box_index(self, r: int, c: int) -> int:
        return (r // 3) * 3 + (c // 3)

    def _safe_to_place(self, r: int, c: int, v: int) -> bool:
        box = self._box_index(r, c)
        return (
            v not in self.rows[r] and
            v not in self.cols[c] and
            v not in self.boxes[box]
        )

    def _add(self, r: int, c: int, v: int):
        self.rows[r].add(v)
        self.cols[c].add(v)
        self.boxes[self._box_index(r, c)].add(v)

    def _remove(self, r: int, c: int, v: int):
        self.rows[r].remove(v)
        self.cols[c].remove(v)
        self.boxes[self._box_index(r, c)].remove(v)

    # -------------------
    # Utility operations
    # -------------------

    def possible_values(self, r: int, c: int) -> Set[int]:
        if self.board[r][c] != -1:
            return set()
        used = self.rows[r] | self.cols[c] | self.boxes[self._box_index(r, c)]
        return {v for v in range(1, 10) if v not in used}

    def find_best_cell(self) -> Tuple[Optional[int], Optional[int]]:
        """MRV heuristic: find empty cell with fewest possibilities."""
        best = None
        best_count = 10
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == -1:
                    poss = self.possible_values(r, c)
                    if not poss:
                        return r, c
                    if len(poss) < best_count:
                        best = (r, c)
                        best_count = len(poss)
                        if best_count == 1:
                            return best
        return best if best else (None, None)

    # -------------------
    # Solving
    # -------------------

    def solve(self) -> bool:
        r, c = self.find_best_cell()
        if r is None:
            return True

        for v in sorted(self.possible_values(r, c)):
            if self._safe_to_place(r, c, v):
                self.board[r][c] = v
                self._add(r, c, v)

                if self.solve():
                    return True

                self._remove(r, c, v)
                self.board[r][c] = -1

        return False

    # -------------------
    # Counting solutions
    # -------------------

    def count_solutions(self, max_solutions: int = 0) -> int:
        count = [0]

        def dfs():
            r, c = self.find_best_cell()
            if r is None:
                count[0] += 1
                return max_solutions > 0 and count[0] >= max_solutions

            for v in self.possible_values(r, c):
                if self._safe_to_place(r, c, v):
                    self.board[r][c] = v
                    self._add(r, c, v)

                    stop = dfs()
                    self._remove(r, c, v)
                    self.board[r][c] = -1
                    if stop:
                        return True
            return False

        dfs()
        return count[0]

    # -------------------
    # Misc
    # -------------------

    def print(self):
        sep = "+-------+-------+-------+"
        print(sep)
        for r in range(9):
            row = "| "
            for c in range(9):
                v = self.board[r][c]
                row += (str(v) if v != -1 else ".") + " "
                if (c + 1) % 3 == 0:
                    row += "| "
            print(row)
            if (r + 1) % 3 == 0:
                print(sep)


# -------------------
# Parsing utilities
# -------------------

def read_puzzle_from_string(s: str, empty_char=".") -> Optional[Board]:
    s = "".join(ch for ch in s if not ch.isspace())
    if len(s) != 81:
        print(f"Error: expected 81 chars, got {len(s)}", file=sys.stderr)
        return None

    board = [[-1] * 9 for _ in range(9)]
    valid = True
    for i, ch in enumerate(s):
        r, c = divmod(i, 9)
        if ch in "123456789":
            board[r][c] = int(ch)
        elif ch == empty_char or ch in "._-":
            board[r][c] = -1
        else:
            print(f"Invalid char '{ch}' at index {i}", file=sys.stderr)
            valid = False

    return board if valid else None


# -------------------
# Example (optional)
# -------------------

if __name__ == "__main__":
    puzzle = (
        "39.215..."
        ".6...2.8."
        "....79.4."
        "..5.8...6"
        ".8..3..5."
        "6...1.2.."
        ".2.6....4"
        ".4.3...9."
        "...159.73"
    )

    b = read_puzzle_from_string(puzzle)
    sdk = Sudoku(b)

    print("Original:")
    sdk.print()

    print("\nCounting solutions:")
    print("Solutions:", sdk.count_solutions(max_solutions=2))

    print("\nSolving...")
    if sdk.solve():
        sdk.print() 
