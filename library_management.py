import sqlite3
from enum import Enum

database = sqlite3.connect("library_management.sqlite")
c = database.cursor()
c.execute(
    "CREATE TABLE IF NOT EXISTS books (isbn INT PRIMARY KEY,title TEXT NOT NULL,author TEXT NOT NULL,genre TEXT NOT NULL,copies INT NOT NULL)"
)
c.execute(
    "CREATE TABLE IF NOT EXISTS members(id INT PRIMARY KEY,password TEXT NOT NULL,name TEXT NOT NULL,email TEXT NOT NULL,role TEXT NOT NULL)"
)

c.execute(
    "CREATE TABLE IF NOT EXISTS borrowed_books(book_isbn INT NOT NULL, member_id INT NOT NULL,borrow_date TEXT,return_date TEXT,status TEXT NOT NULL,FOREIGN KEY (book_isbn) REFERENCES books(isbn),FOREIGN KEY (member_id) REFERENCES members(id))"
)


class BookStatus(Enum):
    available = "Available"
    reserved = "Reserved"
    returned = "Returned"
    not_available = "Not available"


class Book:
    def __init__(self, isbn: int, title, author, genre, no_copies: int):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.genre = genre
        self.copies = no_copies
        # self.status = BookStatus.available

    def __str__(self):
        return " ISBN: {}\n Title: {}\n Author: {}\n Genre: {}\n Copies: {}".format(
            self.isbn, self.title, self.author, self.genre, self.copies
        )


class User:
    def __init__(self, u_id, u_name, u_email, u_pass, u_role="Member"):
        self.id = u_id
        self.name = u_name
        self.email = u_email
        self.password = u_pass
        self.role = u_role

    def __str__(self):
        return " ID: {}\n Name: {}\n Email: {}\n Role: {}".format(
            self.id, self.name, self.email, self.role
        )

    def borrow_book(self, book, borrow_date):
        with database:
            c.execute(
                "SELECT * FROM borrowed_books WHERE book_isbn = :book_isbn AND member_id = :member_id",
                {"book_isbn": book.isbn, "member_id": self.id},
            )
            row = c.fetchone()
            if row:
                print("The book is already borrowed by {}".format(self.name))
            else:
                c.execute(
                    "SELECT copies FROM books WHERE isbn =:isbn", {"isbn": book.isbn}
                )
                row1 = c.fetchone()
                copies = row1[0]
                if copies > 0:
                    c.execute(
                        "UPDATE books SET copies=:copies WHERE isbn =:isbn",
                        {"copies": copies - 1, "isbn": book.isbn},
                    )
                    c.execute(
                        "INSERT INTO borrowed_books (book_isbn,member_id,borrow_date,status) VALUES (:book_isbn,:member_id,:borrow_date,:status)",
                        {
                            "book_isbn": book.isbn,
                            "member_id": self.id,
                            "borrow_date": borrow_date,
                            "status": BookStatus.reserved.value,
                        },
                    )

    def return_book(self, book, return_date):
        with database:
            c.execute(
                "SELECT * FROM borrowed_books WHERE book_isbn = :book_isbn AND member_id = :member_id",
                {"book_isbn": book.isbn, "member_id": self.id},
            )
            row = c.fetchone()
            if row:
                c.execute(
                    "SELECT copies FROM books WHERE isbn =:isbn ", {"isbn": book.isbn}
                )
                copies = c.fetchone()[0]
                c.execute(
                    "UPDATE books SET copies=:copies WHERE isbn =:isbn",
                    {"copies": copies + 1, "isbn": book.isbn},
                )
                c.execute(
                    "UPDATE borrowed_books SET return_date = :return_date,status =:status WHERE book_isbn = :book_isbn AND member_id = :member_id",
                    {
                        "return_date": return_date,
                        "status": BookStatus.returned.value,
                        "book_isbn": book.isbn,
                        "member_id": self.id,
                    },
                )

                print("The book is already borrowed by {}".format(self.name))
            else:
                print("Book is not borrowed")

    def show_borrowed_books(self):
        with database:
            c.execute("SELECT * FROM borrowed_books")
        print(c.fetchall())


class Admin(User):
    def __init__(self, u_id, u_name, u_email, u_pass, u_role="Admin"):
        super().__init__(u_id, u_name, u_email, u_pass, u_role)

    # Book management
    def add_book(self, book):
        with database:
            c.execute(
                "SELECT * FROM books WHERE  title =:title AND author =:author",
                {"title": book.title, "author": book.author},
            )
            row = c.fetchone()
            if row:
                print("Book is already exist in the library")
            else:
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
            c.execute(
                "SELECT * FROM books WHERE  title =:title AND author =:author",
                {"title": book.title, "author": book.author},
            )
            row = c.fetchone()
            if row is None:
                print("Book doesn't exist in the library")
            else:
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
        print(c.fetchall())

    # Member management
    def add_member(self, user):
        with database:
            c.execute(
                "SELECT * FROM members WHERE  name = :name AND email =:email",
                {"name": user.name, "email": user.email},
            )
            row = c.fetchone()
            if row:
                print("User is already exist in the library")
            else:
                c.execute(
                    "INSERT INTO members (id,name,email,password,role) VALUES(:id,:name,:email,:password,:role)",
                    {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "password": user.password,
                        "role": user.role,
                    },
                )

    def update_member(self, user, name=None, email=None, password=None):
        if name:
            with database:
                c.execute(
                    "UPDATE members SET name= :name WHERE id= :id",
                    {"name": name, "id": user.id},
                )
        if email:
            with database:
                c.execute(
                    "UPDATE members SET email= :email WHERE id= :id",
                    {"email": email, "id": user.id},
                )
        if password:
            with database:
                c.execute(
                    "UPDATE members SET password= :password WHERE id= :id",
                    {"password": password, "id": user.id},
                )

    def delete_member(self, user):
        with database:
            c.execute(
                "SELECT * FROM members WHERE  name = :name AND email =:email",
                {"name": user.name, "email": user.email},
            )
            row = c.fetchone()
            if row is None:
                print("User doesn't exist in the library")
            else:
                c.execute("DELETE FROM members WHERE id = :id", {"id": user.id})

    def show_members(self):
        with database:
            c.execute("SELECT * FROM members")
        print(c.fetchall())


class Library:
    def __init__(self, name):
        self.name = name

    def show_all_books(self):
        with database:
            c.execute("SELECT * FROM books")
        print(c.fetchall())

    def show_all_members(self):
        with database:
            c.execute("SELECT * FROM members")
        print(c.fetchall())

    def show_all_borrowed_books(self):
        with database:
            c.execute("SELECT * FROM borrowed_books")
        print(c.fetchall())
