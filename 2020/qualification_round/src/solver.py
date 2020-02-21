from instance import Instance
from library import Library
from solution import Solution


def select_books_given_libraries_order(libs: [Library]) -> Solution:
    already_scanned_books = dict()
    books_to_scan = dict()
    for lib in libs:
        for book in lib.books:
            if not already_scanned_books.get(book):
                already_scanned_books[book] = True
                if not books_to_scan.get(lib.id):
                    books_to_scan[lib.id] = list()
                books_to_scan[lib.id].append(book)
    return Solution(libs, books_to_scan)


class Solver:

    def __init__(self, instance: Instance):
        self.instance = instance

    def solve(self) -> Solution:
        libs = self.instance.libs
        book_to_scan = dict()
        for lib in libs:
            book_to_scan[lib.id] = lib.books
        return Solution(libs, book_to_scan)

    def solve_greedy(self) -> Solution:
        libs = sorted(self.instance.libs, key=lambda x: (x.nb_books_in_lib+x.books_per_day)/x.sign_up_duration,
                      reverse=True)
        book_to_scan = dict()
        already_scanned_books = dict()
        useless_libs = list()
        for lib in libs:
            for book in lib.books:
                if not already_scanned_books.get(book):
                    if not book_to_scan.get(lib.id):
                        book_to_scan[lib.id] = list()
                    book_to_scan[lib.id].append(book)
                    already_scanned_books[book] = True
            if not book_to_scan.get(lib.id):
                useless_libs.append(lib.id)
        final_lib = [lib for lib in libs if lib.id not in useless_libs]
        return Solution(final_lib, book_to_scan)

    def compute_current_lib_score(self, already_scanned_books: dict, lib: Library):
        result = lib.nb_books_in_lib*lib.books_per_day/lib.sign_up_duration
        for book in lib.books:
            if not already_scanned_books.get(book):
                result += self.instance.scores[book]
        return result

    def compute_similarity_score(self, lib: Library):
        result = 0
        for other_lib in self.instance.libs:
            if other_lib.id != lib.id:
                result += len((set(lib.books) & set(other_lib.books)))
        return result
