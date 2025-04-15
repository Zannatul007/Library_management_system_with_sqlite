from library_management import *


book1 = Book(1, "CS", "Zannatul", "CSE", 20)
book2 = Book(2, "DS", "Zannatul Fardaush", "CSE", 30)
book3 = Book(3, "DS", "Zannatul Fardaush", "CSE", 30)
# print(book1)
admin = Admin(1, "Zane", "zane@gmail.com", "cs123")
# # print(admin)
# # admin.add_book(book1)
# # admin.add_book(book3)
# # admin.add_book(book2)
# # admin.update_book(book1, title="DBMS")
# # admin.update_book(book2, copies=40)

# # # admin.delete_book(book1)
# # admin.search_book(author="Zannatul Fardaush")
# # admin.search_book(isbn=1)

# # print(admin.show_books())

# member1 = User(2, "Zane zahaan", "zane@gmail.com", "cs1234")
# member2 = User(3, "Zane zahaan tripty", "zane@gmail.com", "cs1234cs")
# # print(member2)
# # admin.add_member(member1)
# # admin.add_member(member2)
# # admin.delete_member(member1)
# # admin.update_member(member1, name="Zane DOE")
# # admin.update_member(member1, name="Zane DOE Tripty", email="zanedoe@email.com")
# # admin.show_members()

# member1.borrow_book(book1, "15-apr-25")
# member1.return_book(book2, "123")
# member2.borrow_book(book1, "123")
# member1.return_book(book1, "15-may-25")
# # member1.return_book(book1, "20-apr-25")
# # member2.borrow_book(book1,"12-apr-25")
# member1.show_borrowed_books()

# print(admin.show_books())


member1 = User(2, "Zane zahaan", "zane@gmail.com", "cs1234")
member2 = User(3, "Zane zahaan tripty", "zane@gmail.com", "cs1234cs")

b4 = Book(4, "C", "D", "CD", 20)
b5 = Book(5, "C1", "D1", "C1D1", 20)
# admin.add_book(b5)
member1.borrow_book(b4, "14-dec-2024")
member1.return_book(b5, "20-dec-2024")

member1.show_borrowed_books()
admin.show_books()
