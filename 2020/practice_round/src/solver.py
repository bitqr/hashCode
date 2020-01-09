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
        t = self.instance.max_types-1
        c = self.instance.max_slices
        while t >= 0:
            if self.sub_problems_decision[(t, c)]:
                result.append(t)
                c -= self.instance.slices_per_type[t]
            t = t-1
        return sorted(result)