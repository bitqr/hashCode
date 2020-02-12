from instance import Instance
from solver import Solver
from solution import Solution

if __name__ == '__main__':
    inputs_array = ['a_example.in', 'b_small.in', 'c_medium.in', 'd_quite_big.in', 'e_also_big.in']
    outputs_array = ['a_example.out', 'b_small.out', 'c_medium.out', 'd_quite_big.out', 'e_also_big.out']

    instance_index = 0

    file_name = '../input/' + inputs_array[instance_index]

    instance = Instance(file_name)
    print(instance.to_string())

    solver = Solver(instance)

    # found = solver.solve()
    # found = solver.greedy()
    found = solver.dynamic_programming_method()
    print(found)

    solution = Solution(instance, found)
    print("Score =", solution.compute_score())
    solution.write('../output/' + outputs_array[instance_index])
