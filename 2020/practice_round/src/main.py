from instance import Instance
from solver import Solver
from solution import Solution

inputs_array = ['a_example.in', 'b_small.in', 'c_medium.in', 'd_quite_big.in', 'e_also_big.in']
outputs_array = ['a_example.out', 'b_small.out', 'c_medium.out', 'd_quite_big.out', 'e_also_big.out']

instance_index = 0

file_name = '../inputs/' + inputs_array[instance_index]

instance = Instance(file_name)
print(instance.to_string())

solver = Solver(instance)

found = solver.solve()

solution = Solution(found)
solution.write('../outputs/' + outputs_array[instance_index])