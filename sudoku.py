# Developed by phoenix marie.

import sys
from pprint import pprint
import math # Unused in current 9x9 implementation, but kept from previous versions
import copy # Needed for copy_board and count_solutions

def find_next_empty(puzzle):
    """
    Finds the next empty cell (represented by -1) in the puzzle.

    Args:
        puzzle (list[list[int]]): The 9x9 Sudoku board.

    Returns:
        tuple[int, int] | tuple[None, None]: The (row, col) of the next empty cell,
                                            or (None, None) if the board is full.
    """
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == -1:
                return r, c
    return None, None

def is_valid(puzzle, guess, row, col):
    """
    Checks if placing 'guess' at puzzle[row][col] is valid according to Sudoku rules.
    Assumes the cell puzzle[row][col] is currently empty or being checked.

    Args:
        puzzle (list[list[int]]): The 9x9 Sudoku board.
        guess (int): The number (1-9) to check.
        row (int): The row index of the cell.
        col (int): The column index of the cell.

    Returns:
        bool: True if the guess is valid, False otherwise.
    """
    # Check row (excluding the cell itself if it wasn't guaranteed empty)
    for c_idx in range(9):
        if puzzle[row][c_idx] == guess and c_idx != col: # Ensure we don't compare the cell with itself if pre-filled
             return False

    # Check column (excluding the cell itself)
    for r_idx in range(9):
        if puzzle[r_idx][col] == guess and r_idx != row:
            return False

    # Check 3x3 square (excluding the cell itself)
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3
    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess and (r, c) != (row, col):
                return False

    return True

def solve_sudoku(puzzle):
    """
    Solves the Sudoku puzzle using backtracking. Modifies the puzzle in place.
    Stops after finding the first solution.

    Args:
        puzzle (list[list[int]]): The 9x9 Sudoku board, with -1 representing empty cells.

    Returns:
        bool: True if a solution is found, False otherwise.
    """
    row, col = find_next_empty(puzzle)

    # Base case: If no empty cells are left, the puzzle is solved
    if row is None:
        return True

    # Try numbers 1 through 9
    for guess in range(1, 10):
        # Check validity using the refined is_valid function
        # Temporarily place guess to check validity in context
        original_value = puzzle[row][col] # Should be -1
        puzzle[row][col] = guess
        is_valid_placement = True
        # Check row
        if not all(puzzle[row].count(x) <= 1 for x in range(1, 10) if x in puzzle[row]): is_valid_placement = False
        # Check column
        if is_valid_placement and not all([puzzle[i][col] for i in range(9)].count(x) <= 1 for x in range(1, 10) if x in [puzzle[i][col] for i in range(9)]): is_valid_placement = False
        # Check box
        if is_valid_placement:
             row_start, col_start = (row // 3) * 3, (col // 3) * 3
             box_nums = [puzzle[r][c] for r in range(row_start, row_start + 3) for c in range(col_start, col_start + 3)]
             if not all(box_nums.count(x) <= 1 for x in range(1, 10) if x in box_nums): is_valid_placement = False

        puzzle[row][col] = original_value # Restore original value before recursive call check

        # If placing the guess is potentially valid (doesn't immediately break rules)
        # This check might be redundant if `find_next_empty` guarantees empty cell,
        # and `is_valid` handles checks correctly. Let's simplify based on original logic.
        # We use the is_valid function intended for placing into an empty cell.
        if is_valid(puzzle, guess, row, col): # Revert to original check
            puzzle[row][col] = guess  # Place the valid guess

            # Recursively call solve_sudoku
            if solve_sudoku(puzzle):
                return True

            # Backtrack: If the recursive call didn't lead to a solution, undo the guess
            puzzle[row][col] = -1

    # If no number from 1-9 works for this cell, the puzzle is unsolvable from the current state
    return False


# --- Previously Added Functions ---

def print_board(puzzle):
    """Prints the Sudoku board in a formatted grid. Represents -1 as '.'."""
    print("-" * 25)
    for i in range(9):
        if i % 3 == 0 and i != 0: print("-" * 25)
        row_str = "| "
        for j in range(9):
            if j % 3 == 0 and j != 0: row_str += "| "
            cell = puzzle[i][j]
            row_str += (str(cell) if cell != -1 else ".") + " "
        print(row_str + "|")
    print("-" * 25)

def is_board_valid(puzzle):
    """Checks if the entire board configuration is valid (no duplicates in rows/cols/boxes), ignoring -1."""
    # Check Rows
    for r in range(9):
        seen = set()
        for c in range(9):
            num = puzzle[r][c]
            if num != -1:
                if num in seen: return False
                seen.add(num)
    # Check Columns
    for c in range(9):
        seen = set()
        for r in range(9):
            num = puzzle[r][c]
            if num != -1:
                if num in seen: return False
                seen.add(num)
    # Check 3x3 Squares
    for box_r in range(3):
        for box_c in range(3):
            seen = set()
            for r in range(box_r * 3, box_r * 3 + 3):
                for c in range(box_c * 3, box_c * 3 + 3):
                    num = puzzle[r][c]
                    if num != -1:
                        if num in seen: return False
                        seen.add(num)
    return True

def count_empty(puzzle):
    """Counts the number of empty cells (-1) in the puzzle."""
    return sum(row.count(-1) for row in puzzle)

def read_puzzle_from_string(puzzle_string, empty_char='.'):
    """Creates a 9x9 puzzle board from an 81-character string."""
    if len(puzzle_string) != 81:
        print(f"Error: Puzzle string must be 81 chars. Found {len(puzzle_string)}.", file=sys.stderr)
        return None
    puzzle = [[-1 for _ in range(9)] for _ in range(9)]
    valid_input = True
    for i, char in enumerate(puzzle_string):
        row, col = i // 9, i % 9
        if '1' <= char <= '9':
            puzzle[row][col] = int(char)
        elif char != empty_char:
            print(f"Error: Invalid char '{char}' at index {i}.", file=sys.stderr)
            valid_input = False
            # Continue parsing to find all errors, but will return None
    if not valid_input: return None

    if not is_board_valid(puzzle):
         print("Warning: Loaded puzzle has initial rule violations.", file=sys.stderr)
         # Return the board anyway, maybe the user wants to fix it or analyze
    return puzzle

# --- Newly Added Functions ---

def copy_board(puzzle):
    """
    Creates a deep copy of the puzzle board.

    Args:
        puzzle (list[list[int]]): The 9x9 Sudoku board.

    Returns:
        list[list[int]]: A new independent copy of the board.
    """
    return copy.deepcopy(puzzle)

def _count_solutions_helper(puzzle, count_list):
    """Recursive helper for count_solutions. Modifies puzzle in place."""
    row, col = find_next_empty(puzzle)

    # Base case: A solution is found
    if row is None:
        count_list[0] += 1
        # Stop if we only need to know if there's more than one solution (optimization)
        # if count_list[0] >= 2:
        #    return True # Indicate found > 1
        return False # Continue searching

    # Try numbers 1 through 9
    for guess in range(1, 10):
        if is_valid(puzzle, guess, row, col):
            puzzle[row][col] = guess

            if _count_solutions_helper(puzzle, count_list):
                 # If the helper returns True (e.g., optimization triggered), propagate upwards
                 # puzzle[row][col] = -1 # Backtrack state if needed before propagating True
                 return True

            # Backtrack whether solution was found or not, to explore other branches
            puzzle[row][col] = -1

            # Optimization: If we already found 2, stop searching this branch
            # if count_list[0] >= 2:
            #     return True

    # Finished exploring all guesses for this cell
    return False # Indicate search should continue if calling function needs it

def count_solutions(puzzle):
    """
    Counts the total number of unique solutions for the given Sudoku puzzle.
    Warning: Can be very slow for puzzles with many solutions.

    Args:
        puzzle (list[list[int]]): The 9x9 Sudoku board.

    Returns:
        int: The number of solutions found (0, 1, 2, ...).
    """
    # Work on a copy to avoid modifying the original puzzle
    board_copy = copy_board(puzzle)
    # Use a list to pass the count by reference through recursion
    solution_count = [0]
    _count_solutions_helper(board_copy, solution_count)
    return solution_count[0]

def get_possible_values(puzzle, row, col):
    """
    Returns a set of valid numbers (1-9) that can be placed in the cell (row, col).
    Returns an empty set if the cell is already filled.

    Args:
        puzzle (list[list[int]]): The 9x9 Sudoku board.
        row (int): The row index.
        col (int): The column index.

    Returns:
        set[int]: A set of possible valid numbers for the cell.
    """
    if puzzle[row][col] != -1:
        return set() # Cell is already filled

    possible = set()
    for guess in range(1, 10):
        if is_valid(puzzle, guess, row, col):
            possible.add(guess)
    return possible

def puzzle_to_string(puzzle, empty_char='.'):
    """
    Converts a 9x9 puzzle board back into an 81-character string.

    Args:
        puzzle (list[list[int]]): The 9x9 Sudoku board.
        empty_char (str, optional): Character to use for empty cells (-1). Defaults to '.'.

    Returns:
        str: The 81-character string representation.
    """
    flat_list = []
    for r in range(9):
        for c in range(9):
            num = puzzle[r][c]
            flat_list.append(str(num) if num != -1 else empty_char)
    return "".join(flat_list)


# --- Main Execution Block ---

if __name__ == '__main__':
    # Example puzzle known to have a unique solution
    example_board_string = "39.-15..-..-..2.-..-.5.--.-719.8.-.5.-.68..--2.6---3.---.-.---.--45.-----.---67.1.5.4.1.9----2.-."
    example_board = read_puzzle_from_string(example_board_string.replace('.', '-'), empty_char='-')

    if example_board:
        print("Original Puzzle:")
        board_copy_for_solving = copy_board(example_board) # Keep original intact
        print_board(board_copy_for_solving)
        print(f"Initial empty cells: {count_empty(board_copy_for_solving)}")
        print(f"Is initial board state valid? {is_board_valid(board_copy_for_solving)}")

        # Demonstrate get_possible_values for the first empty cell found
        r_empty, c_empty = find_next_empty(board_copy_for_solving)
        if r_empty is not None:
             possible = get_possible_values(board_copy_for_solving, r_empty, c_empty)
             print(f"\nPossible values for cell ({r_empty}, {c_empty}): {possible}")
        else:
             print("\nBoard is already full (or appears so).")


        # Count solutions (on a separate copy)
        print("\nCounting solutions (this might take a moment)...")
        num_solutions = count_solutions(example_board) # Use original state
        print(f"Number of solutions found: {num_solutions}")


        # Solve the puzzle (modifies board_copy_for_solving)
        print("\nAttempting to find a solution...")
        if solve_sudoku(board_copy_for_solving):
            print("\nSolution found:")
            print_board(board_copy_for_solving)
            print(f"Final empty cells: {count_empty(board_copy_for_solving)}")
            print(f"Is solved board valid? {is_board_valid(board_copy_for_solving)}")

            # Convert solved board to string
            solved_string = puzzle_to_string(board_copy_for_solving, empty_char='.')
            print(f"\nSolved board as string: {solved_string}")
        else:
            print("No solution exists for the given puzzle.") # Should not happen for this example

    else:
        print("Failed to load puzzle from string.")

    # Example of a puzzle with multiple solutions (first row empty)
    print("\nTesting a puzzle with multiple solutions:")
    multi_sol_string = "-1-1-1-1-1-1-1-1-1" + \
                       "183675429" + \
                       "762194583" + \
                       "871532964" + \
                       "526489317" + \
                       "934716852" + \
                       "318967245" + \
                       "645251798" + \
                       "2978431.6" # Intentionally invalid last char '.' for testing read_puzzle error
                       # "2978431-6" Corrected last char
    multi_sol_string = multi_sol_string.replace("1.6","1-6") # fix error
    multi_board = read_puzzle_from_string(multi_sol_string, empty_char='-')
    if multi_board:
        print_board(multi_board)
        print("Counting solutions (this might take a moment)...")
        num_multi_solutions = count_solutions(multi_board)
        print(f"Number of solutions found: {num_multi_solutions}") # Should be > 1
    else:
         print("Failed to load multi-solution board (expected if error char wasn't fixed).")
 
