from library import Library


class Instance:

    def __init__(self, file_name: str):
        with open(file_name, 'r') as file:
            x = file.read()
            file_split = x.splitlines()
            self.nb_books = int(file_split[0].split(' ')[0])
            self.nb_libraries = int(file_split[0].split(' ')[1])
            self.nb_days = int(file_split[0].split(' ')[2])
            self.scores = []
            items = file_split[1].split(' ')
            for i in range(0, self.nb_books):
                self.scores.append(int(items[i]))
            self.libs = []
            for i in range(0, self.nb_libraries):
                items = file_split[2+2*i].split(' ')
                book_nb = int(items[0])
                sign_up = int(items[1])
                book_per_day = int(items[2])
                books_indices = file_split[3+2*i].split(' ')
                books = [int(j) for j in books_indices]
                self.libs.append(Library(i, book_nb, sign_up, book_per_day, books))

    def to_string(self) -> str:
        s = "Instance:\n"
        s += f"Nb books: {self.nb_books}\nNb Libs: {self.nb_libraries}\nNb days: {self.nb_days}"
        s += "\nBook scores: "
        for score in self.scores:
            s += str(score) + " "
        s += "\n"
        for lib in self.libs:
            s += lib.to_string() + "\n"
        return s

    def compute_lib_score(self, lib: Library) -> int:
        result = 0
        for book in lib.books:
            result += self.scores[book]
        return result

