import os
from dimacs_generator import generate_sudoku_clauses

def save_as_dimacs(clauses, num_vars, file_path):
    """ Save clauses in DIMACS format to a file."""
    with open(file_path, 'w') as f:
        f.write(f"p cnf {num_vars} {len(clauses)}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")

def create_sudoku_puzzles(grid_sizes, num_puzzles_per_size, output_dir):
    """Generate and save Sudoku puzzles in CNF format."""
    os.makedirs(output_dir, exist_ok=True)
    
    for grid_size in grid_sizes:
        for puzzle_num in range(1, num_puzzles_per_size + 1):
            print(f"Generating {grid_size}x{grid_size} Sudoku puzzle {puzzle_num}...")
            
            clauses = generate_sudoku_clauses(grid_size)
            num_vars = grid_size * grid_size * grid_size
            
            file_name = f"sudoku_{grid_size}x{grid_size}_{puzzle_num}.cnf"
            file_path = os.path.join(output_dir, file_name)
            
            # Save clauses as DIMACS file
            save_as_dimacs(clauses, num_vars, file_path)
            print(f"Saved to {file_path}")

if __name__ == "__main__":
    grid_sizes = [4, 9, 16]
    num_puzzles_per_size = 10
    output_dir = "sudoku_puzzles"

    create_sudoku_puzzles(grid_sizes, num_puzzles_per_size, output_dir)
    print("All Sudoku puzzles generated!")
