from instance import Instance

class Solution:

    def __init__(self, instance: Instance, indices: [int]):
        self.types = indices
        self.instance = instance

    def write(self, file_name: str):
        with open(file_name, 'w') as file:
            file.write(str(len(self.types)) + '\n')
            for index in self.types:
                file.write(str(index) + ' ')
            file.close()

    def compute_score(self):
        result = 0
        for index in self.types:
            result += self.instance.slices_per_type[index]
        return result