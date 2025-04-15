from library_management import *

book1 = Book(1, "CS", "Zannatul", "CSE", 20)
book2 = Book(2, "DS", "Zannatul Fardaush", "CSE", 30)
book3 = Book(3, "DS", "Zannatul Fardaush", "CSE", 30)
print(book1)
member = User("1", "Zannatul", "Zannatul@gmail.com")
print(member)
admin = Admin("2", "zannatul", "zannatulgmail.com")
print(admin)
# admin.add_book(book1)
# admin.add_book(book3)
# admin.add_book(book2)
admin.update_book(book1, title="DBMS")
admin.update_book(book2, copies=40)

# admin.delete_book(book1)
admin.search_book(author="Zannatul Fardaush")
admin.search_book(isbn=1)

print(admin.show_books())
