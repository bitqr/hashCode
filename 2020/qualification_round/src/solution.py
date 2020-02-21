from library import Library
from instance import Instance


class Solution:

    def __init__(self, libs: [Library], books_to_scan):
        self.libs = libs
        self.books_to_scan = books_to_scan
        self.shipment = dict()

    def write(self, file_name: str):
        with open(file_name, 'w') as file:
            file.write(str(len(self.libs)) + '\n')
            for lib in self.libs:
                file.write(str(lib.id) + ' ')
                file.write(str(len(self.books_to_scan[lib.id])) + '\n')
                for i in self.books_to_scan[lib.id]:
                    file.write(str(i)+" ")
                file.write("\n")
            file.close()

    def compute_score(self, instance: Instance):
        result = 0
        day = 0
        for lib in self.libs:
            day += lib.sign_up_duration
            counter_per_day = 0
            day_offset = 0
            for book in self.books_to_scan[lib.id]:
                if counter_per_day < lib.books_per_day:
                    counter_per_day += 1
                else:
                    counter_per_day = 1
                    day_offset += 1
                if day + day_offset < instance.nb_days:
                    result += instance.scores[book]
                    if not self.shipment.get(day+day_offset):
                        self.shipment[day+day_offset] = list()
                    self.shipment[day+day_offset].append(book)
        return result
