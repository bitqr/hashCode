from instance import Instance
from solver import Solver
from solution import Solution

if __name__ == '__main__':
    inputs_array = []
    outputs_array = []

    instance_index = 0

    file_name = '../input/' + inputs_array[instance_index]

    instance = Instance(file_name)
    print(instance.to_string())

    solver = Solver(instance)

    found = solver.solve()

    print(found)

    solution = Solution(instance, found)
    print("Score =", solution.compute_score())
    solution.write('../output/' + outputs_array[instance_index])
