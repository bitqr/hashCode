from instance import Instance
from solver import Solver

if __name__ == '__main__':
    inputs_array = ['a_example.txt', 'b_read_on.txt', 'c_incunabula.txt', 'd_tough_choices.txt', 'e_so_many_books.txt',
                    'f_libraries_of_the_world.txt']
    outputs_array = ['a_example.out', 'b_read_on.out', 'c_incunabula.out', 'd_tough_choices.out', 'e_so_many_books.out',
                     'f_libraries_of_the_world.out']

    instance_index = 1

    for instance_index in range(0, 6):

        file_name = '../input/' + inputs_array[instance_index]

        instance = Instance(file_name)

        solver = Solver(instance)

        print("Start solving...")
        solution = solver.solve_greedy()

        score = solution.compute_score(instance)
        print(f"Solution score = {score}")
        solution.write('../output/' + outputs_array[instance_index])
