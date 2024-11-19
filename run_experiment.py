import os
import time
import numpy as np
from collections import defaultdict
from CDCL import parse_cnf, CDCL
from DPLL import DPLL
from JW import JW

import json

# Files provided by the user
# cnf_files = [
#     "sudoku1.cnf",
#     "sudoku2.cnf",
#     "sudoku3.cnf",
#     "sudoku4.cnf",
#     "sudoku5.cnf" 
# ]

# Collect all CNF files from the "sudoku_puzzles" directory
cnf_folder = "sudoku_puzzles"
cnf_files = [os.path.join(cnf_folder, file) for file in os.listdir(cnf_folder) if file.endswith(".cnf")]

def save_results_to_file(results, file_path):
    with open(file_path, "w") as f:
        json.dump(results, f, indent=4)
    print(f"Results saved to {file_path}")

# Code to run the experiment for a given solver
def run_solver_experiment(solver_class, cnf_files, solver_name, num_runs=3, save_path="all_results.json"):
    results = defaultdict(lambda: defaultdict(list))
    
    for file_path in cnf_files:
        print(f"\n== Running solver {solver_name} on {file_path}...")
        
        for run_number in range(1, num_runs + 1):
            print(f"  Run {run_number} of {num_runs} for {file_path}...")
            
            try:
                # Parse CNF file
                clauses, num_vars = parse_cnf(file_path)
                
                # Initialize the solver
                solver = solver_class(clauses)
                
                # Start timer
                start_time = time.time()
                
                # Solve the problem
                result, assignments, evals, backtracks = solver.solve()
                
                # Time taken
                time_taken = time.time() - start_time
                
                # Store statistics
                results[file_path]["evaluations"].append(evals)
                results[file_path]["backtracks"].append(backtracks)
                results[file_path]["time_taken"].append(time_taken)
                results[file_path]["status"].append("SATISFIABLE" if result else "UNSATISFIABLE")
                
            except Exception as e:
                results[file_path]["error"].append(str(e))

            save_results_to_file(results, save_path)

    return results


# Running the experiment with all solvers
def run_experiment():
    solvers = [
        (CDCL, "CDCL"),
        (DPLL, "DPLL"),
        (JW, "JW")
    ]
    
    all_results = {}
    
    for solver_class, solver_name in solvers:
        print(f"\n======= Running experiments for solver: {solver_name}\n")
        results = run_solver_experiment(solver_class, cnf_files, solver_name)
        all_results[solver_name] = results
        print(f"Completed experiments for solver: {solver_name}\n")
    
    return all_results


# Display results and calculate statistics in this function
def display_results(results, filename="strategy_results.txt"):
    with open(filename, "w") as f:  # Open the file to save the results
        for solver_name, solver_results in results.items():
            f.write(f"Results for Solver: {solver_name}\n")
            print(f"Results for Solver: {solver_name}")
            
            for file_path, stats in solver_results.items():
                f.write(f"  {file_path}:\n")
                print(f"  {file_path}:")
                
                if "error" in stats:
                    f.write(f"    Error: {stats['error']}\n")
                    print(f"    Error: {stats['error']}")
                else:
                    evaluations = stats["evaluations"]
                    backtracks = stats["backtracks"]
                    time_taken = stats["time_taken"]
                    
                    # Calculate statistics
                    avg_evaluations = np.mean(evaluations) if evaluations else "N/A"
                    max_evaluations = np.max(evaluations) if evaluations else "N/A"
                    min_evaluations = np.min(evaluations) if evaluations else "N/A"
                    
                    avg_backtracks = np.mean(backtracks) if backtracks else "N/A"
                    max_backtracks = np.max(backtracks) if backtracks else "N/A"
                    min_backtracks = np.min(backtracks) if backtracks else "N/A"
                    
                    avg_time_taken = np.mean(time_taken) if time_taken else "N/A"
                    max_time_taken = np.max(time_taken) if time_taken else "N/A"
                    min_time_taken = np.min(time_taken) if time_taken else "N/A"
                    
                    satisfiable_percentage = (stats["status"].count("SATISFIABLE") / len(stats["status"])) * 100
                    
                    # Write results to file and print them
                    f.write(f"    Avg Evaluations: {avg_evaluations}\n")
                    f.write(f"    Max Evaluations: {max_evaluations}\n")
                    f.write(f"    Min Evaluations: {min_evaluations}\n")
                    f.write(f"    Avg Backtracks: {avg_backtracks}\n")
                    f.write(f"    Max Backtracks: {max_backtracks}\n")
                    f.write(f"    Min Backtracks: {min_backtracks}\n")
                    f.write(f"    Avg Time Taken: {avg_time_taken} sec\n")
                    f.write(f"    Max Time Taken: {max_time_taken} sec\n")
                    f.write(f"    Min Time Taken: {min_time_taken} sec\n")
                    f.write(f"    Satisfiable Percentage: {satisfiable_percentage:.2f}%\n\n")
                    
                    print(f"    Avg Evaluations: {avg_evaluations}")
                    print(f"    Max Evaluations: {max_evaluations}")
                    print(f"    Min Evaluations: {min_evaluations}")
                    print(f"    Avg Backtracks: {avg_backtracks}")
                    print(f"    Max Backtracks: {max_backtracks}")
                    print(f"    Min Backtracks: {min_backtracks}")
                    print(f"    Avg Time Taken: {avg_time_taken} sec")
                    print(f"    Max Time Taken: {max_time_taken} sec")
                    print(f"    Min Time Taken: {min_time_taken} sec")
                    print(f"    Satisfiable Percentage: {satisfiable_percentage:.2f}%\n")


if __name__ == "__main__":
    all_results = run_experiment()
    display_results(all_results)
