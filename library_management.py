import sqlite3
from enum import Enum
import argon2


hasher = argon2.PasswordHasher()

database = sqlite3.connect("library_management.sqlite")
c = database.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS books (
    isbn INT PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT NOT NULL,
    copies INT NOT NULL,
    status TEXT NOT NULL)"""
)
c.execute(
    """CREATE TABLE IF NOT EXISTS members(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    admin BOOL)"""
)
c.execute(
    """CREATE TABLE IF NOT EXISTS borrowed_books(
    book_isbn INT NOT NULL,
      member_email TEXT NOT NULL,
      borrow_date TEXT,
      return_date TEXT,
      status TEXT NOT NULL,
      FOREIGN KEY (book_isbn) REFERENCES books(isbn),
      FOREIGN KEY (member_email) REFERENCES members(email))"""
)


class BookStatus(Enum):
    reserved = "Reserved"
    returned = "Returned"
    available = "Available"
    not_available = "Not available"


class Book:
    def __init__(self, isbn: int, title, author, genre, no_copies: int):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.genre = genre
        self.copies = no_copies
        self.status = BookStatus.available.value

    def __str__(self):
        return " ISBN: {}\n Title: {}\n Author: {}\n Genre: {}\n Copies: {}\n Status: {}".format(
            self.isbn, self.title, self.author, self.genre, self.copies, self.status
        )


class User:

    def __init__(self, u_name, u_email, u_pass, u_role="Member"):

        self.name = u_name
        self.email = u_email
        self.password = u_pass
        self.role = u_role

    def __str__(self):

        return " Name: {}\n Email: {}\n Role: {}".format(
            self.name, self.email, self.role
        )

    def borrow_book(self, isbn, borrow_date):

        with database:
            c.execute("SELECT * FROM books where isbn =:isbn", {"isbn": isbn})
            book = c.fetchone()
            if book:
                c.execute(
                    "SELECT * FROM borrowed_books WHERE book_isbn = :book_isbn AND member_email = :member_email)",
                    {"book_isbn": isbn, "member_email": self.email},
                )
                row = c.fetchone()
                if row:
                    print("The book is already borrowed")
                else:

                    c.execute(
                        "SELECT copies FROM books WHERE isbn =:isbn", {"isbn": isbn}
                    )
                    row1 = c.fetchone()
                    copies = row1[0]
                    if copies > 0:
                        new_copies = copies - 1
                        c.execute(
                            "UPDATE books SET copies=:copies WHERE isbn =:isbn",
                            {"copies": new_copies, "isbn": isbn},
                        )
                        c.execute(
                            "INSERT INTO borrowed_books (book_isbn,member_email,borrow_date,status) VALUES (:book_isbn,:member_email,:borrow_date,:status)",
                            {
                                "book_isbn": isbn,
                                "member_email": self.email,
                                "borrow_date": borrow_date,
                                "status": BookStatus.reserved.value,
                            },
                        )
                        print("Book is successfully borrowed")
                    else:
                        c.execute(
                            "UPDATE books SET status = :status WHERE isbn = :book_isbn",
                            {
                                "status": BookStatus.not_available.value,
                                "book_isbn": isbn,
                            },
                        )
                        print(c.fetchone())
                        print("There are no available copies of this book!")
            else:
                print("Book doesn't exist in the library!")

    def return_book(self, isbn, return_date):
        with database:
            c.execute(
                "SELECT * FROM borrowed_books WHERE book_isbn = :book_isbn AND member_email = :member_email AND status =:status",
                {
                    "book_isbn": isbn,
                    "member_email": self.email,
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
                    "UPDATE borrowed_books SET return_date = :return_date,status =:status WHERE book_isbn = :book_isbn AND member_email = :member_email",
                    {
                        "return_date": return_date,
                        "status": BookStatus.returned.value,
                        "book_isbn": isbn,
                        "member_email": self.email,
                    },
                )
                print("Book is successfully returned by {}".format(self.name))

    def show_books_transaction(self):
        with database:
            c.execute(
                "SELECT * FROM borrowed_books WHERE member_email = :member_email",
                {"member_email": self.email},
            )
            books = c.fetchall()
            for book in books:
                isbn, email, b_date, r_date, status = book
                print(
                    "ISBN: {}\nBorrow Date: {}\nReturn Date: {}\nStatus: {}\n".format(
                        isbn, b_date, r_date, status
                    )
                )


class Admin(User):
    def __init__(self, u_name, u_email, u_pass, u_role="Admin"):
        super().__init__(u_name, u_email, u_pass, u_role)

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
                    "INSERT INTO books (isbn,title,author,genre,copies,status) VALUES(:isbn,:title,:author,:genre,:copies,:status)",
                    {
                        "isbn": book.isbn,
                        "title": book.title,
                        "author": book.author,
                        "genre": book.genre,
                        "copies": book.copies,
                        "status": BookStatus.available.value,
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
            isbn, title, author, genre, copies, status = c.fetchone()
            new_book = Book(isbn, title, author, genre, copies)
            print(new_book)

        if title:
            with database:
                c.execute("SELECT * FROM books WHERE title = :title", {"title": title})
            print("Book details of title {}".format(title))
            isbn, title, author, genre, copies, status = c.fetchone()
            new_book = Book(isbn, title, author, genre, copies)
            print(new_book)
        if author:
            with database:
                c.execute(
                    "SELECT * FROM books WHERE author = :author", {"author": author}
                )
            print("All books of author {}".format(author))
            books = c.fetchall()
            for book in books:
                isbn, title, author, genre, copies, status = book
                new_book = Book(isbn, title, author, genre, copies)
                print(new_book)

    def show_books(self):
        with database:
            c.execute("SELECT * FROM books")
        print(c.fetchall())

    # Member management
    # def add_member(self):

    def update_member(self, u_id, name=None, email=None, password=None):
        load_members()
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
        load_members()
        with database:
            c.execute("SELECT * FROM members WHERE id =:id", {"id": u_id})
            row = c.fetchone()
            if row:
                c.execute("DELETE FROM members WHERE id = :id", {"id": u_id})
                print("User is removed successfully!")
            else:
                print("User doesn't exist in the library!")


class Library:

    def show_all_books(self):
        load_books()

    def show_all_members(self):
        load_members()

    def show_all_books_transactions(self):
        load_borrowed_books()

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
            mostly_borrowed_book = c.fetchone()[0]
        print("Mostly borrowed book is {}".format(mostly_borrowed_book))

    def show_most_active_user(self):
        with database:
            c.execute(
                "SELECT members.name,members.email,COUNT(borrowed_books.member_email) as active_user_counter"
                " FROM members"
                " LEFT JOIN borrowed_books"
                " ON members.email = borrowed_books.member_email"
                " GROUP BY members.email"
                " ORDER BY active_user_counter DESC LIMIT 1"
            )

            mostly_active_member = c.fetchone()[0]
        print("Mostly active member is {}".format(mostly_active_member))

    def total_no_books(self):
        with database:
            c.execute("SELECT SUM(copies) FROM books")
            print("Total no of books in library {}".format(c.fetchone()[0]))

    def total_no_users(self):
        with database:
            c.execute("SELECT id FROM members")
            print("Total no of members in library {}".format(len(c.fetchall())))

    def usage_report(self):
        self.total_no_books()
        self.total_no_users()
        self.show_most_borrowed_books()
        self.show_most_active_user()


def load_books():
    with database:
        c.execute("SELECT * FROM books")
        print("-" * 20)
        books = c.fetchall()
        for book in books:

            isbn, title, author, genre, no_copies, status = book
            new_book = Book(isbn, title, author, genre, no_copies)
            print(new_book)
            print("-" * 20)


def load_members():
    with database:
        c.execute("SELECT * FROM members")
        print("-" * 20)
        members = c.fetchall()
        for member in members:
            m_id, password, name, email, role = member
            if role:
                role = "Admin"
            else:
                role = "Member"
            new_member = User(name, email, password, role)
            print(" User id: {}".format(m_id))
            print(new_member)
            print("-" * 20)


def load_borrowed_books():
    with database:
        c.execute(
            """SELECT books.isbn, books.title, books.copies,borrowed_books.member_email, members.name
               FROM borrowed_books
               LEFT JOIN books ON books.isbn = borrowed_books.book_isbn
               LEFT JOIN members ON members.email = borrowed_books.member_email"""
        )
        borrowed_books = c.fetchall()
        print("-" * 20)
        for book in borrowed_books:
            print(
                " Book ISBN: {}\n Title: {}\n Available copies: {}\n Borrowed By: {} (email: {})".format(
                    book[0], book[1], book[2], book[4], book[3]
                )
            )
            print("-" * 20)


# load_books()
# library = Library()
# library.show_all_books()
# library.show_all_members()
# library.show_all_books_transactions()
