import sqlite3

database = sqlite3.connect("library_management.sqlite")
c = database.cursor()
c.execute(
    "CREATE TABLE IF NOT EXISTS books (isbn INT PRIMARY KEY,title TEXT NOT NULL,author TEXT NOT NULL,genre TEXT NOT NULL,copies INT NOT NULL)"
)
c.execute(
    "CREATE TABLE IF NOT EXISTS members(id INT PRIMARY KEY,name TEXT NOT NULL,email TEXT NOT NULL,role TEXT NOT NULL)"
)


class Book:
    def __init__(self, isbn: int, title, author, genre, no_copies: int):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.genre = genre
        self.copies = no_copies

    def __str__(self):
        return " ISBN: {}\n Title: {}\n Author: {}\n Genre: {}\n Copies: {}".format(
            self.isbn, self.title, self.author, self.genre, self.copies
        )


class User:
    def __init__(self, u_id, u_name, u_email, u_role="Member"):
        self.id = u_id
        self.name = u_name
        self.email = u_email
        self.role = u_role
        self.borrowed_books = {}

    def __str__(self):
        return " ID: {}\n Name: {}\n Email: {}\n Role: {}".format(
            self.id, self.name, self.email, self.role
        )

    def borrow_book(self):
        pass

    def return_book(self):
        pass


class Admin(User):
    def __init__(self, u_id, u_name, u_email, u_role="Admin"):
        super().__init__(u_id, u_name, u_email, u_role)
        self.members = []
        self.books = []

    # Book management
    def add_book(self, book):
        with database:
            c.execute(
                "INSERT INTO books (isbn,title,author,genre,copies) VALUES(:isbn,:title,:author,:genre,:copies)",
                {
                    "isbn": book.isbn,
                    "title": book.title,
                    "author": book.author,
                    "genre": book.genre,
                    "copies": book.copies,
                },
            )

    def update_book(self, book, title=None, copies=None):
        if title:
            with database:
                c.execute(
                    "UPDATE books SET title = :title WHERE isbn= :isbn",
                    {"title": title, "isbn": book.isbn},
                )
        if copies:
            with database:
                c.execute(
                    "UPDATE books SET copies=:copies WHERE isbn= :isbn",
                    {"copies": copies, "isbn": book.isbn},
                )

    def delete_book(self, book):
        with database:
            c.execute("DELETE FROM books WHERE isbn = :isbn", {"isbn": book.isbn})

    def search_book(self, isbn=None, title=None, author=None):
        if isbn:
            with database:
                c.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn})
            print(c.fetchone())
        if title:
            with database:
                c.execute("SELECT * FROM books WHERE title = :title", {"title": title})
            print(c.fetchone())
        if author:
            with database:
                c.execute(
                    "SELECT * FROM books WHERE author = :author", {"author": author}
                )
            print(c.fetchall())

    def show_books(self):
        with database:
            c.execute("SELECT * FROM books")
        return c.fetchall()

    # Member management
    def add_member(self):
        pass

    def update_member(self):
        pass

    def delete_member(self):
        pass


class Library:
    def __init__(self):
        pass
