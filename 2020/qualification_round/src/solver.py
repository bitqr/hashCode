from instance import Instance
from library import Library
from solution import Solution
import random


def neighbourhood(libs: [Library]) -> [Library]:
    result = list(libs)
    old_index = random.choice(range(0, len(result)))
    new_index = random.choice(range(0, len(result)))
    result.insert(new_index, result.pop(old_index))
    return result


def shuffle(libs: [Library]) -> [Library]:
    result = list(libs)
    old_index = random.choice(range(0, len(result)))
    intermediate_index = random.choice(range(0, len(result)))
    new_index = random.choice(range(0, len(result)))
    result.insert(intermediate_index, result.pop(old_index))
    result.insert(new_index, result.pop(intermediate_index))
    result.insert(new_index, result.pop(old_index))
    return result


class Solver:

    def __init__(self, instance: Instance):
        self.instance = instance
        self.book_to_libs = dict()
        self.pre_process()

    def solve(self) -> Solution:
        libs = self.instance.libs
        book_to_scan = dict()
        for lib in libs:
            book_to_scan[lib.id] = lib.books
        return Solution(libs, book_to_scan)

    def solve_greedy(self) -> Solution:
        libs = sorted(self.instance.libs,
                      key=lambda x: (self.instance.compute_lib_score(x)*x.books_per_day)/x.sign_up_duration,
                      reverse=True)
        return self.order_to_sol(libs)

    def solve_greedy_finer(self) -> Solution:
        init_libs = list(self.instance.libs)
        final_libs = list()
        books_to_scan = dict()
        already_scanned_books = dict()
        # Current score of each lib, pre-computed
        lib_to_scores = dict()
        for lib in init_libs:
            lib_to_scores[lib] = self.compute_current_lib_score(already_scanned_books, lib)
        while len(init_libs) > 0:
            lib = max(init_libs, key=lambda x: lib_to_scores[x])
            init_libs.remove(lib)
            for book in lib.books:
                if not already_scanned_books.get(book):
                    if not books_to_scan.get(lib.id):
                        books_to_scan[lib.id] = list()
                    books_to_scan[lib.id].append(book)
                    already_scanned_books[book] = True
                    # Only update other libs having the same books
                    for related_lib in self.book_to_libs[book]:
                        lib_to_scores[related_lib] = lib_to_scores[related_lib] - self.instance.scores[book]
            # Only add a lib if it has some uncovered books
            if books_to_scan.get(lib.id):
                final_libs.append(lib)
        # Just scan the most valuable books first
        for book in books_to_scan.keys():
            books_to_scan[book] = sorted(books_to_scan[book], key=lambda x: self.compute_book_importance(book),
                                         reverse=True)
        return Solution(final_libs, books_to_scan)

    def compute_book_importance(self, book: int) -> int:
        return 100*self.instance.scores[book]

    def compute_current_lib_score(self, already_scanned_books: dict, lib: Library):
        result = 0
        for book in lib.books:
            if not already_scanned_books.get(book):
                result += self.instance.scores[book]
        return result*lib.books_per_day/lib.sign_up_duration

    def compute_similarity_score(self, lib: Library):
        result = 0
        for other_lib in self.instance.libs:
            if other_lib.id != lib.id:
                result += len((set(lib.books) & set(other_lib.books)))
        return result

    def pre_process(self):
        for lib in self.instance.libs:
            for book in lib.books:
                if not self.book_to_libs.get(book):
                    self.book_to_libs[book] = list()
                self.book_to_libs[book].append(lib)

    def order_to_sol(self, libs: [Library]) -> Solution:
        already_scanned_books = dict()
        books_to_scan = dict()
        useless_libs = list()
        for lib in libs:
            for book in lib.books:
                if not already_scanned_books.get(book):
                    if not books_to_scan.get(lib.id):
                        books_to_scan[lib.id] = list()
                    books_to_scan[lib.id].append(book)
                    already_scanned_books[book] = True
            if not books_to_scan.get(lib.id):
                useless_libs.append(lib.id)
        final_lib = [lib for lib in libs if lib.id not in useless_libs]
        # Just scan the most valuable books first
        for book in books_to_scan.keys():
            books_to_scan[book] = sorted(books_to_scan[book], key=lambda x: self.instance.scores[x], reverse=True)
        return Solution(final_lib, books_to_scan)

    def local_search(self, iter_count: int, file_name: str, initial_tolerance: int, converge_shuffle: int) -> Solution:
        tolerance = initial_tolerance
        convergence = 0
        global_convergence = 0
        # Initial solution
        current_sol = self.load_solution(file_name)
        current_score = current_sol.compute_score(self.instance)
        best_score = current_score
        best_sol = current_sol
        current_lib_list = list(current_sol.libs)
        i = 0
        while global_convergence < 10000:
            new_sol = self.order_to_sol(neighbourhood(current_lib_list))
            new_score = new_sol.compute_score(self.instance)
            print(f"It #{i}:\tCurrent score: {current_score} -- New score: {new_score} "
                  f"-- Best score: {best_score} -- convergence: {convergence} -- global conv: {global_convergence}")
            if new_score > current_score:
                convergence = 0
            else:
                convergence += 1
            if new_score >= current_score or current_score - new_score < tolerance:
                current_score = new_score
                current_sol = new_sol
                current_lib_list = current_sol.libs
            if new_score > best_score:
                global_convergence = 0
                print(f"New Best Sol!!")
                best_score = new_score
                best_sol = new_sol
            else:
                global_convergence += 1
                tolerance *= 0.9
            if convergence == converge_shuffle:
                convergence = 0
                current_lib_list = shuffle(current_lib_list)
                current_sol = self.order_to_sol(current_lib_list)
                current_score = current_sol.compute_score(self.instance)
            i += 1
        return best_sol

    def load_solution(self, file_name: str) -> Solution:
        with open(file_name, 'r') as file:
            libs = list()
            books_to_scan = dict()
            x = file.read()
            file_split = x.splitlines()
            nb_libs = int(file_split[0])
            line_counter = 1
            for lib in range(0, nb_libs):
                couple = file_split[line_counter].split(' ')
                lib_id = int(couple[0])
                # Append the right library
                libs.append(self.instance.libs[lib_id])
                nb_books_to_scan = int(couple[1])
                line_counter += 1
                book_indices = file_split[line_counter].split(' ')
                books_to_scan[lib_id] = list()
                for b in range(0, nb_books_to_scan):
                    books_to_scan[lib_id].append(int(book_indices[b]))
                line_counter += 1
            return Solution(libs, books_to_scan)
