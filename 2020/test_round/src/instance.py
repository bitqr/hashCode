
class Instance:

    def __init__(self, file_name: str):
        with open(file_name, 'r') as file:
            x = file.read()
            file_split = x.splitlines()
            self.max_slices = int(file_split[0].split(' ')[0])
            self.max_types = int(file_split[0].split(' ')[1])
            self.slices_per_type = map(lambda item: int(item), file_split[1].split(' '))

    def to_string(self) -> str:
        result = f'Maximum {self.max_slices} slices and {self.max_types} types\n'
        for item in self.slices_per_type:
            result += f'{item} '
        return result
