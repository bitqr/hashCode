class Library:

    def __init__(self, i: int, nb_books_in_lib: int, sign_up_duration: int, books_per_day: int, books: [int]):
        self.nb_books_in_lib = nb_books_in_lib
        self.sign_up_duration = sign_up_duration
        self.books_per_day = books_per_day
        self.books = books
        self.id = i

    def to_string(self) -> str:
        s = f"\nLibrary #{self.id}:\n"
        s += f"Nb books: {self.nb_books_in_lib}\nSign-up: {self.sign_up_duration}\nBooks per day: {self.books_per_day}"
        s += "\nBook ids: "
        for book in self.books:
            s += str(book) + " "
        return s
