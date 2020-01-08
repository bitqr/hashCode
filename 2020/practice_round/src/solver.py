from instance import Instance


class Solver:

    def __init__(self, instance: Instance):
        self.instance = instance

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
