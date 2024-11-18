import time
from sat_solver import SATSolver
from dimacs_generator import generate_sudoku_clauses, save_dimacs

def run_experiment():
    num_puzzles = 5
    sudoku_results = []
    hypersudoku_results = []

    sudoku_clauses = generate_sudoku_clauses()
    hypersudoku_clauses = generate_sudoku_clauses()  # Extend to hypersudoku if needed

    for i in range(num_puzzles):
        print(f"Running puzzle {i + 1}...")
        
        # Sudoku
        start_time = time.time()
        sudoku_solver = SATSolver(sudoku_clauses, 729)
        sudoku_solver.solve()
        sudoku_time = time.time() - start_time
        sudoku_results.append(sudoku_time)

        # Hypersudoku
        start_time = time.time()
        hypersudoku_solver = SATSolver(hypersudoku_clauses, 729)
        hypersudoku_solver.solve()
        hypersudoku_time = time.time() - start_time
        hypersudoku_results.append(hypersudoku_time)

        print(f"Sudoku time: {sudoku_time:.2f}s, Hypersudoku time: {hypersudoku_time:.2f}s")

    print("\nResults:")
    for i in range(num_puzzles):
        print(f"Puzzle {i + 1}: Sudoku = {sudoku_results[i]:.2f}s, Hypersudoku = {hypersudoku_results[i]:.2f}s")

if __name__ == "__main__":
    run_experiment()



#Run the Experiment
# Open a terminal or command prompt.
# Navigate to the folder containing these files.
# Run the experiment script:
#   python experiment.py
# Observe the results printed in the terminal. It will display the runtime for each Sudoku and Hypersudoku puzzle.