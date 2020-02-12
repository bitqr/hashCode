from instance import Instance


class Solver:

    def __init__(self, instance: Instance):
        self.instance = instance
        self.sub_problems = dict()
        self.sub_problems_decision = dict()

    def solve(self) -> [int]:
        """Silly solving method"""
        current_capacity = self.instance.max_slices
        result = []
        for index in range(0, self.instance.max_types):
            if current_capacity >= self.instance.slices_per_type[index]:
                result.append(index)
                current_capacity -= self.instance.slices_per_type[index]
            if current_capacity == 0:
                return result
        return result

    def greedy(self) -> [int]:
        """Sorting pizza types by decreasing order of slices"""
        current_capacity = self.instance.max_slices
        sorted_list = sorted(range(self.instance.max_types),
                             key=self.instance.slices_per_type.__getitem__,
                             reverse=True)
        result = []
        for index in sorted_list:
            if current_capacity >= self.instance.slices_per_type[index]:
                result.append(index)
                current_capacity -= self.instance.slices_per_type[index]
            if current_capacity == 0:
                return result
        return sorted(result)

    def get_sub_problem_value(self, type_index: int, max_slices_capacity: int) -> int:
        if self.sub_problems.get((type_index, max_slices_capacity)) is not None:
            return self.sub_problems.get((type_index, max_slices_capacity))
        # Not found. Compute the value for the first time
        # Base case
        if type_index == 0:
            self.sub_problems[(type_index, max_slices_capacity)] = self.instance.slices_per_type[0] if \
                self.instance.slices_per_type[0] <= max_slices_capacity else 0
            self.sub_problems_decision[(type_index, max_slices_capacity)] = \
                (self.sub_problems[(type_index, max_slices_capacity)] != 0)
            return self.sub_problems[(type_index, max_slices_capacity)]
        # Recursive case
        slices_count_at_index = self.instance.slices_per_type[type_index]
        if slices_count_at_index <= max_slices_capacity:
            self.sub_problems[(type_index, max_slices_capacity)] = \
                max(self.get_sub_problem_value(type_index-1, max_slices_capacity),
                    self.get_sub_problem_value(type_index-1, max_slices_capacity-slices_count_at_index)
                    + slices_count_at_index)
            self.sub_problems_decision[(type_index, max_slices_capacity)] = \
                (self.sub_problems[(type_index, max_slices_capacity)] !=
                 self.get_sub_problem_value(type_index-1, max_slices_capacity))
            return self.sub_problems[(type_index, max_slices_capacity)]
        else:
            self.sub_problems[(type_index, max_slices_capacity)] = \
                self.get_sub_problem_value(type_index-1, max_slices_capacity)
            self.sub_problems_decision[(type_index, max_slices_capacity)] = False
            return self.sub_problems[(type_index, max_slices_capacity)]

    def dynamic_programming_optimal_value(self) -> int:
        return self.get_sub_problem_value(self.instance.max_types-1, self.instance.max_slices)

    def dynamic_programming_method(self) -> [int]:
        self.dynamic_programming_optimal_value()
        result = []
        types = self.instance.max_types-1
        capacity = self.instance.max_slices
        while types >= 0:
            if self.sub_problems_decision[(types, capacity)]:
                result.append(types)
                capacity -= self.instance.slices_per_type[types]
            types = types-1
        return sorted(result)

    def local_search(self) -> [int]:
        """Local search method, with simple neighbour, looking for the best swap"""
        current_solution = self.greedy()
        current_value = sum(list(map(lambda x: self.instance.slices_per_type[x], current_solution)))
        remaining_capacity = self.instance.max_slices - current_value
        local_optimum = False
        while not local_optimum:
            best_in, best_out = -1, -1
            delta = 0
            for index_to_insert in [x for x in range(0, self.instance.max_types) if x not in current_solution]:
                for index_to_remove in current_solution:
                    # Check if the swap is feasible
                    if remaining_capacity + self.instance.slices_per_type[index_to_remove] >= \
                     self.instance.slices_per_type[index_to_insert]:
                        # Check if the delta is sufficient
                        if self.instance.slices_per_type[index_to_insert] - \
                         self.instance.slices_per_type[index_to_remove] > delta:
                            best_in, best_out = index_to_insert, index_to_remove
                            delta = self.instance.slices_per_type[index_to_insert] - \
                                self.instance.slices_per_type[index_to_remove]
            if best_in == -1:
                local_optimum = True
            else:
                # Update current solution
                current_solution.remove(best_out)
                current_solution.append(best_in)
                current_value += delta
                remaining_capacity -= delta
                if remaining_capacity == 0:
                    return sorted(current_solution)
            print("Current solution value:", current_value)
            print("Remaining capacity:", remaining_capacity)
        return sorted(current_solution)
