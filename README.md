Sudoku Solver – Optimized Constraint-Based Engine

This project provides a fast and reliable Sudoku solver built with constraint propagation and MRV (Minimum Remaining Values) heuristics. It includes puzzle parsing, solution counting, and a high-performance backtracking engine that maintains row, column, and box constraints in constant time. The solver is designed to handle everything from simple puzzles to advanced, highly constrained boards.


---

Features

🧩 Efficient Solving

Uses MRV to always choose the most constrained empty cell.

Minimizes branching, resulting in significantly faster solve times.


⚡ Optimized Constraints

Tracks row, column, and 3×3 box usage with sets for O(1) membership checks.

Ensures violations are detected immediately during both initialization and search.


🔍 Solution Analysis

Count all solutions with optional early stopping (max_solutions) for uniqueness testing.

Useful for puzzle generation or verifying puzzle difficulty.


📥 Puzzle Input

Accepts standard 81-character strings using digits for filled cells and ., _, or - for empty cells.

Ignores whitespace for flexible formatting.


📤 Pretty Printing

Displays the Sudoku board in a clean, grid-styled format for readability.



---

Usage Example

from sudoku import Sudoku, read_puzzle_from_string

puzzle_str = (
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

board = read_puzzle_from_string(puzzle_str)
sdk = Sudoku(board)

print("Original puzzle:")
sdk.print()

print("\nCounting solutions (stops at 2):")
print(sdk.count_solutions(max_solutions=2))

print("\nSolving...")
if sdk.solve():
    sdk.print()


---

Project Structure

sudoku/
│
├── sudoku.py        # Main solver implementation
├── README.md        # Project documentation
└── examples/        # Optional sample puzzles


---

Error Handling

Input validation catches illegal characters or malformed puzzles.

Initial boards containing rule violations raise a descriptive ValueError.



---

Requirements

Python 3.8+

No external dependencies



---

License

This project is released under the MIT License.
Feel free to modify, distribute, and use it in your own applications.
