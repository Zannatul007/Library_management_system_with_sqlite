from library_management import *


b1 = Book(1, "CS", "Zannatul", "CSE", 20)
b2 = Book(2, "CS2", "Zannatul", "CSE", 30)
b3 = Book(3, "CS3", "Zannatul", "CSE", 40)
b4 = Book(4, "CS4", "Zannatul", "CSE", 50)

admin = Admin(1, "Sabbir", "Sabbir@gmail.com", "Sabbir127")
m1 = User(2, "Munna", "Munna@gmail.com", "Munna127")
m2 = User(3, "Biplob", "Biplob@gmail.com", "Biplob127")

admin.add_book(b1)
admin.add_book(b2)
admin.add_book(b3)
admin.add_book(b4)

# admin.show_books()

m1.borrow_book(b1, "15-apr-25")
m1.borrow_book(b2, "16-apr-25")
m1.return_book(b1, "15-jan-25")
# m1.show_borrowed_books()
# admin.show_books()

library = Library("XYZ")
library.show_all_books()
library.show_all_borrowed_books()
library.show_all_members()
