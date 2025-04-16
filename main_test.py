from library_management import *


b1 = Book(1, "CS", "Zannatul", "CSE", 20)
b2 = Book(2, "CS2", "Zannatul", "CSE", 30)
b3 = Book(3, "CS3", "Zannatul", "CSE", 40)
b4 = Book(4, "CS4", "Zannatul", "CSE", 50)

admin = Admin(1, "Sabbir", "Sabbir@gmail.com", "Sabbir127")
m1 = User(2, "Munna", "Munna@gmail.com", "Munna127")
m2 = User(3, "Biplob", "Biplob@gmail.com", "Biplob127")
m1.register()
print(m1.verify("Munna@gmail.com", "Munna127"))

admin.add_book(b1)
admin.add_book(b2)
admin.add_book(b3)
admin.add_book(b4)

admin.show_books()

admin.add_member(m1)
admin.add_member(m2)

admin.show_members()
m1.borrow_book(1, "---")
m1.borrow_book(2, "---")
m1.borrow_book(3, "---")
m2.borrow_book(1, "---")
library = Library("XYZ")

library.show_most_borrowed_books()


# admin.update_book(1,"DS")
# book_isbn = input("Press enter or type a book isbn: ")
# print(book_isbn)
# title = input("Press enter or type title: ")
# copies = input("Press enter or no of copies: ")
# if book_isbn is not "":
#     book_isbn = int(book_isbn)
# if copies is not "":
#     copies = int(copies)

# admin.delete_book(6)
# admin.delete_book(1)
# admin.show_books()

# book_isbn = int(input("Enter a book isbn: "))
# title = input("Press enter or type title: ")
# copies = input("Press enter or no of copies: ")
# if copies is not "":
#     copies = int(copies)
# admin.update_book(book_isbn, title, copies)
# admin.show_books()

# admin.search_book(2)

# book_isbn = input("Press enter or type a book isbn: ")
# title = input("Press enter or type title: ")
# author = input("Press enter or type author name: ")
# if book_isbn is not "":
#     book_isbn = int(book_isbn)
# admin.search_book(book_isbn, title, author)

# m1.register()
# print(m1.verify("Munna@gmail.com", "Munna127"))
# m1.borrow_book(2, "15-apr-24")
# m1.return_book(2, "18-Apr-24")
# m1.show_books_transaction()
# admin.add_member(m2)
# m2.borrow_book(2, "15-apr-25")
# m2.return_book(2, "25-apr-25")
# m2.show_books_transaction()

# admin.show_books()


# m1.borrow_book(1, "15-apr-25")
# m1.borrow_book(2, "16-apr-25")
# m1.return_book(1, "15-jan-25")
# m2.borrow_book(1, "15-june-2025")

# admin.add_member(m1)
# admin.add_member(m2)
# # m1.show_borrowed_books()
# # admin.show_books()

# library = Library("XYZ")
# print("ALL BOOKS")
# library.show_all_books()
# print("ALL BORROWED BOOKS")
# library.show_all_borrowed_books()
# print("ALL Members")
# library.show_all_members()
# print("SHOW MOST BORROWED BOOKS")
# library.show_most_borrowed_books()
# import hashlib

# hash_object = hashlib.sha512()
# hash_object.update(b"Hello world")
# hex_digit = hash_object.hexdigest()
# print(hex_digit)


# print(hex_digit == hex_digit)
import argon2

# password = b"Zannatul123"
# hasher = argon2.PasswordHasher()
# hashed_password = hasher.hash(password)
# print(hashed_password)


# new_pass = b"Zannatul123"
# hasher.verify(hashed_password,new_pass)
# print("pass word correct")
