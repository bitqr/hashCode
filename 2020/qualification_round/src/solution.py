from library import Library


class Solution:

    def __init__(self, libs: [Library], book_to_scan: [[int]]):
        self.libs = libs
        self.book_to_scan = book_to_scan

    def write(self, file_name: str):
        with open(file_name, 'w') as file:
            file.write(str(len(self.libs)) + '\n')
            for lib in self.libs:
                file.write(str(lib.id) + ' ')
            file.close()

    def compute_score(self):
        pass
        # result = 0
        # for index in self.types:
        #    result += self.instance.slices_per_type[index]
        # return result
