class SATSolver:
    def __init__(self, clauses, num_vars):
        self.clauses = clauses
        self.num_vars = num_vars
        self.assignment = {}

    def solve(self):
        return self.dpll()

    def dpll(self):
        if all(self.is_satisfied(clause) for clause in self.clauses):
            return True
        if any(self.is_unsatisfied(clause) for clause in self.clauses):
            return False
        var = self.choose_variable()
        self.assignment[var] = True
        if self.dpll():
            return True
        self.assignment[var] = False
        if self.dpll():
            return True
        del self.assignment[var]
        return False

    def is_satisfied(self, clause):
        return any(self.assignment.get(abs(lit), lit > 0) == (lit > 0) for lit in clause)

    def is_unsatisfied(self, clause):
        return all(self.assignment.get(abs(lit), lit > 0) != (lit > 0) for lit in clause)

    def choose_variable(self):
        for clause in self.clauses:
            for lit in clause:
                if abs(lit) not in self.assignment:
                    return abs(lit)
        return None

    def get_solution(self):
        return [f"{var if self.assignment[var] else -var} 0" for var in sorted(self.assignment.keys())]
