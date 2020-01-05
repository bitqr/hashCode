
class Solution:

    def __init__(self, indices: [int]):
        self.types = indices

    def write(self, file_name: str):
        with open(file_name, 'w') as file:
            file.write(str(len(self.types)) + '\n')
            for index in self.types:
                file.write(str(index) + ' ')
            file.close()