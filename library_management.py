import sqlite3
from enum import Enum
import argon2

hasher = argon2.PasswordHasher()

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
    reserved = "Reserved"
    returned = "Returned"


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

    # user registration and verification

    def get_hash(self, password):
        hashed_password = hasher.hash(password)
        return hashed_password

    def register(self):
        with database:
            c.execute("SELECT * FROM members WHERE id=:id", {"id": self.id})
            row = c.fetchone()
            if row:
                print("You have already an account. Please login!")
            else:
                c.execute(
                    "INSERT INTO members (id,name,email,password,role) VALUES (:id,:name,:email,:password,:role)",
                    {
                        "id": self.id,
                        "name": self.name,
                        "email": self.email,
                        "password": self.get_hash(self.password),
                        "role": self.role,
                    },
                )
                print("Registration is successful. Now you can log in to your account!")

    def verify(self, email, password):
        with database:
            c.execute(
                "SELECT email,password FROM members WHERE id =:id", {"id": self.id}
            )
            db_email, db_password = c.fetchone()
            if db_email == email:
                try:
                    hasher.verify(db_password, password)
                    return True
                except argon2.exceptions.VerifyMismatchError:
                    return False
            else:
                return False

    # user borrow and return book management

    def borrow_book(self, isbn, borrow_date):
        with database:
            c.execute("SELECT * FROM books where isbn =:isbn", {"isbn": isbn})
            book = c.fetchone()
            if book:
                c.execute(
                    "SELECT * FROM borrowed_books WHERE book_isbn = :book_isbn AND member_id = :member_id",
                    {"book_isbn": isbn, "member_id": self.id},
                )
                row = c.fetchone()
                if row:
                    print("The book is already borrowed by {}".format(self.name))
                else:

                    c.execute(
                        "SELECT copies FROM books WHERE isbn =:isbn", {"isbn": isbn}
                    )
                    row1 = c.fetchone()
                    copies = row1[0]
                    if copies > 0:
                        c.execute(
                            "UPDATE books SET copies=:copies WHERE isbn =:isbn",
                            {"copies": copies - 1, "isbn": isbn},
                        )
                        c.execute(
                            "INSERT INTO borrowed_books (book_isbn,member_id,borrow_date,status) VALUES (:book_isbn,:member_id,:borrow_date,:status)",
                            {
                                "book_isbn": isbn,
                                "member_id": self.id,
                                "borrow_date": borrow_date,
                                "status": BookStatus.reserved.value,
                            },
                        )
                        print("Book is successfully borrowed by {}".format(self.name))
                    else:
                        print("There are no available copies of this book!")
            else:
                print("Book doesn't exist in the library!")

    def return_book(self, isbn, return_date):
        with database:
            c.execute(
                "SELECT * FROM borrowed_books WHERE book_isbn = :book_isbn AND member_id = :member_id AND status =:status",
                {
                    "book_isbn": isbn,
                    "member_id": self.id,
                    "status": BookStatus.reserved.value,
                },
            )
            row = c.fetchone()
            if row:
                c.execute("SELECT copies FROM books WHERE isbn =:isbn ", {"isbn": isbn})
                copies = c.fetchone()[0]
                c.execute(
                    "UPDATE books SET copies=:copies WHERE isbn =:isbn",
                    {"copies": copies + 1, "isbn": isbn},
                )
                c.execute(
                    "UPDATE borrowed_books SET return_date = :return_date,status =:status WHERE book_isbn = :book_isbn AND member_id = :member_id",
                    {
                        "return_date": return_date,
                        "status": BookStatus.returned.value,
                        "book_isbn": isbn,
                        "member_id": self.id,
                    },
                )
                print("Book is successfully returned by {}".format(self.name))

    def show_books_transaction(self):
        with database:
            c.execute(
                "SELECT * FROM borrowed_books WHERE member_id = :member_id",
                {"member_id": self.id},
            )
        print(c.fetchall())


class Admin(User):
    def __init__(self, u_id, u_name, u_email, u_pass, u_role="Admin"):
        super().__init__(u_id, u_name, u_email, u_pass, u_role)

    # Book management
    def add_book(self, book):
        with database:
            c.execute(
                "SELECT * FROM books WHERE  isbn =:isbn",
                {"isbn": book.isbn},
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
                print("Book is successfully added to the library!")

    def update_book(self, isbn, title=None, copies=None):
        with database:
            c.execute(
                "SELECT * FROM books WHERE  isbn =:isbn",
                {"isbn": isbn},
            )
            row = c.fetchone()
        if row:
            if title:
                with database:
                    c.execute(
                        "UPDATE books SET title = :title WHERE isbn= :isbn",
                        {"title": title, "isbn": isbn},
                    )
            if copies:
                with database:
                    c.execute(
                        "UPDATE books SET copies=:copies WHERE isbn= :isbn",
                        {"copies": copies, "isbn": isbn},
                    )
        else:
            print("Book doesn't exist in the library!")

    def delete_book(self, isbn):
        with database:
            c.execute(
                "SELECT * FROM books WHERE  isbn =:isbn",
                {"isbn": isbn},
            )
            row = c.fetchone()
            if row:

                c.execute("DELETE FROM books WHERE isbn = :isbn", {"isbn": isbn})
                print("Book is deleted successfully!")
            else:
                print("Book doesn't exist in the library!")

    def search_book(self, isbn=None, title=None, author=None):
        if isbn:
            with database:
                c.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn})
            print("Book details of ISBN {}".format(isbn))
            print(c.fetchone())
        if title:
            with database:
                c.execute("SELECT * FROM books WHERE title = :title", {"title": title})
            print("Book details of title {}".format(title))
            print(c.fetchone())
        if author:
            with database:
                c.execute(
                    "SELECT * FROM books WHERE author = :author", {"author": author}
                )
            print("All books of author {}".format(author))
            print(c.fetchall())

    def show_books(self):
        with database:
            c.execute("SELECT * FROM books")
        print(c.fetchall())

    # Member management
    def add_member(self, user):
        with database:
            c.execute(
                "SELECT * FROM members WHERE  id =:id",
                {"id": user.id},
            )
            row = c.fetchone()
            if row:
                print("User already exists in the library")
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
                print("User is successfully added to the library!")

    def update_member(self, u_id, name=None, email=None, password=None):
        with database:
            c.execute("SELECT * FROM members WHERE id =:id", {"id": u_id})
            row = c.fetchone()
        if row:
            if name:
                with database:
                    c.execute(
                        "UPDATE members SET name= :name WHERE id= :id",
                        {"name": name, "id": u_id},
                    )
            if email:
                with database:
                    c.execute(
                        "UPDATE members SET email= :email WHERE id= :id",
                        {"email": email, "id": u_id},
                    )
            if password:
                with database:
                    c.execute(
                        "UPDATE members SET password= :password WHERE id= :id",
                        {"password": password, "id": u_id},
                    )
        else:
            print("User doesn't exist in the library!")

    def delete_member(self, u_id):

        with database:
            c.execute("SELECT * FROM members WHERE id =:id", {"id": u_id})
            row = c.fetchone()
            if row:
                c.execute("DELETE FROM members WHERE id = :id", {"id": u_id})
                print("User is removed successfully!")
            else:
                print("User doesn't exist in the library!")

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

    def show_all_books_transactions(self):
        with database:
            c.execute("SELECT * FROM borrowed_books")
        print(c.fetchall())

    def show_most_borrowed_books(self):
        with database:
            c.execute(
                "SELECT books.title,books.isbn,COUNT(borrowed_books.book_isbn) as no_of_times_borrowed"
                " FROM books"
                " LEFT JOIN borrowed_books"
                " ON borrowed_books.book_isbn = books.isbn"
                " GROUP BY books.isbn"
                " ORDER BY no_of_times_borrowed DESC LIMIT 1"
            )
        print(c.fetchall())
