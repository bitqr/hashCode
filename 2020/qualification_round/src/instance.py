from library import Library


class Instance:

    def __init__(self, file_name: str):
        pass
        with open(file_name, 'r') as file:
            x = file.read()
            file_split = x.splitlines()
            self.nb_books = int(file_split[0].split(' ')[0])
            self.nb_libraries = int(file_split[0].split(' ')[1])
            self.nb_days = int(file_split[0].split(' ')[2])
            self.scores = []
            for i in range(0, self.nb_books):
                self.scores.append(int(file_split[1].split(' ')[i]))
            self.libs = []
            for i in range(0, self.nb_libraries):
                book_nb = int(file_split[2+2*i].split(' ')[0])
                sign_up = int(file_split[2+2*i].split(' ')[1])
                book_per_day = int(file_split[2+2*i].split(' ')[2])
                books = [int(j) for j in file_split[3+2*i].split(' ')]
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
