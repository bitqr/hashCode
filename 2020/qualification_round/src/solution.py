from library import Library


class Solution:

    def __init__(self, libs: [Library], book_to_scan):
        self.libs = libs
        self.book_to_scan = book_to_scan

    def write(self, file_name: str):
        with open(file_name, 'w') as file:
            print(self.libs)
            file.write(str(len(self.libs)) + '\n')
            for lib in self.libs:
                file.write(str(lib.id) + ' ')
                file.write(str(len(self.book_to_scan[lib.id])) + '\n')
                for i in self.book_to_scan[lib.id]:
                    file.write(str(i)+" ")
                file.write("\n")
            file.close()

    def compute_score(self):
        pass
        # result = 0
        # for index in self.types:
        #    result += self.instance.slices_per_type[index]
        # return result
