from instance import Instance
from library import Library
from solution import Solution


class Solver:

    def __init__(self, instance: Instance):
        self.instance = instance

    def solve(self) -> Solution:
        libs = self.instance.libs
        book_to_scan = dict()
        for lib in libs:
            book_to_scan[lib.id] = lib.books
        return Solution(libs, book_to_scan)
