import random

def generate_sudoku_cnf(puzzle, rules_file, output_file):
    """
    Generates a CNF file for a given Sudoku puzzle.

    :param puzzle: 2D list (9x9) of integers (0 for empty, 1-9 for known values).
    :param rules_file: Path to the file containing Sudoku rules in CNF.
    :param output_file: Path to the output CNF file.
    """
    # Load the Sudoku rules
    with open(rules_file, 'r') as rf:
        rules = rf.readlines()
    
    # Extract problem definition (p cnf line) and base rules
    p_line = rules[0]
    base_rules = rules[1:]
    
    # Add puzzle-specific constraints (unit clauses for known values)
    puzzle_clauses = []
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] != 0:
                # Translate (row, col, value) to a variable
                variable = 100 * (r + 1) + 10 * (c + 1) + puzzle[r][c]
                puzzle_clauses.append(f"{variable} 0\n")
    
    # Update the number of clauses
    total_clauses = len(base_rules) + len(puzzle_clauses)
    p_line = f"p cnf 999 {total_clauses}\n"
    
    # Write to the output file
    with open(output_file, 'w') as of:
        of.write(p_line)
        of.writelines(base_rules)
        of.writelines(puzzle_clauses)

def generate_complete_sudoku():
    """
    Generates a complete 9x9 Sudoku grid using a backtracking approach.
    :return: A 9x9 list of integers representing a complete Sudoku grid.
    """
    size = 9
    grid = [[0 for _ in range(size)] for _ in range(16)]

    def is_valid(num, row, col):
        # Check if num is valid at grid[row][col]
        for i in range(size):
            if grid[row][i] == num or grid[i][col] == num:
                return False
        sub_row, sub_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(sub_row, sub_row + 3):
            for j in range(sub_col, sub_col + 3):
                if grid[i][j] == num:
                    return False
        return True

    def solve():
        for row in range(size):
            for col in range(size):
                if grid[row][col] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    for num in numbers:
                        if is_valid(num, row, col):
                            grid[row][col] = num
                            if solve():
                                return True
                            grid[row][col] = 0
                    return False
        return True

    solve()
    return grid

def create_puzzle(grid, empty_cells):
    """
    Removes numbers from a completed Sudoku grid to create a puzzle.

    :param grid: A completed 9x9 Sudoku grid.
    :param empty_cells: Number of cells to empty.
    :return: A 9x9 list of integers representing the puzzle (0 for empty cells).
    """
    puzzle = [row[:] for row in grid]
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    for _ in range(empty_cells):
        if cells:
            r, c = cells.pop()
            puzzle[r][c] = 0
    return puzzle

def generate_random_sudoku(empty_cells=40):
    """
    Generates a random Sudoku puzzle with a specified number of empty cells.

    :param empty_cells: Number of empty cells in the puzzle (default 40).
    :return: A 9x9 list of integers representing the Sudoku puzzle.
    """
    complete_grid = generate_complete_sudoku()
    return create_puzzle(complete_grid, empty_cells)

# Example usage:
random_sudoku = generate_random_sudoku(empty_cells=60)
for row in random_sudoku:
    print(row)

# Generate a random Sudoku puzzle with 40 empty cells
# random_puzzle = generate_random_sudoku(empty_cells=40)

# Generate the CNF file for the random Sudoku puzzle
generate_sudoku_cnf(random_sudoku, "sudoku-rules-9x9.txt", "random-sudoku.cnf")
