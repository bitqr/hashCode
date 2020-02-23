from instance import Instance
from solver import Solver

if __name__ == '__main__':
    inputs_array = ['a_example.txt', 'b_read_on.txt', 'c_incunabula.txt', 'd_tough_choices.txt', 'e_so_many_books.txt',
                    'f_libraries_of_the_world.txt']
    outputs_array = ['a_example.out', 'b_read_on.out', 'c_incunabula.out', 'd_tough_choices.out', 'e_so_many_books.out',
                     'f_libraries_of_the_world.out']

    start = 2
    end = 2

    overall_score = 0

    for instance_index in range(start, end+1):

        file_name = '../input/' + inputs_array[instance_index]
        initial_solution_path_name = '../output/' + outputs_array[instance_index]

        instance = Instance(file_name)

        solver = Solver(instance)

        print("Start solving...")
        solution = solver.local_search(1000, initial_solution_path_name, initial_tolerance=2000, converge_shuffle=500)
        # solution = solver.solve_greedy()
        # solution = solver.solve_greedy_finer()

        score = solution.compute_score(instance)
        print(f"Solution score = {score}")
        overall_score += score
        solution.write('../output/' + outputs_array[instance_index])

    print(f"\n\n\nOVERALL SCORE -------> {overall_score}")
