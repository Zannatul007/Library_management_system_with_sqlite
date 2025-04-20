from library_management import *
from auth import *

while True:
    print("1: Login as a user")
    print("2: Login as an admin")
    print("3: Register")
    print("4: Exit")
    choice = int(input("Select your choice: "))
    if choice == 1:
        user = login()
        if user:
            while True:
                print("1: Borrow book")
                print("2: Return book")
                print("3: Show book transactions")
                print("4: Logout")

                user_choice = int(input("Select your choice: "))

                if user_choice == 1:
                    print("BORROWING BOOK")
                    book_id = int(input("Enter book id you want to borrow: "))
                    borrow_date = input("Enter borrow date: ")
                    user.borrow_book(book_id, borrow_date)
                elif user_choice == 2:
                    print("RETURNING BOOK")
                    book_id = int(input("Enter book id you want to return: "))
                    return_date = input("Enter return date: ")
                    user.return_book(book_id, return_date)
                elif user_choice == 3:
                    print("SHOW ALL TRANSACTIONS")
                    user.show_books_transaction()
                elif user_choice == 4:
                    break

    elif choice == 2:
        admin = login()
        if admin:
            library = Library()
            print("-----Welcome to the Library-----")
            while True:

                print("1: Add book")
                print("2: Remove Book")
                print("3: Update Book")
                print("4: Search Book")
                print("5: Add User")
                print("6: Remove User")
                print("7: Update User")
                print("8: Usage Report")
                print("9: Show books")
                print("10: Show member")
                print("11: Logout")

                admin_choice = int(input("Select a number from 1 to 12:  "))

                if admin_choice == 1:
                    print("ADDING BOOK")
                    book_isbn = int(input("Enter a book isbn: "))
                    book_title = input("Enter book title: ")
                    book_author = input("Enter book author: ")
                    book_genre = input("Enter book genre: ")
                    book_copies = int(input("Enter no of copies: "))
                    book = Book(
                        book_isbn, book_title, book_author, book_genre, book_copies
                    )
                    admin.add_book(book)
                elif admin_choice == 2:
                    print("REMOVING BOOK")
                    load_books()
                    book_isbn = int(input("Enter a book isbn: "))
                    admin.delete_book(book_isbn)
                elif admin_choice == 3:
                    print("UPDATING BOOK")
                    load_books()
                    book_isbn = int(input("Enter a book isbn: "))
                    title = input("Press enter or type title: ")
                    copies = input("Press enter or no of copies: ")
                    if copies != "":
                        copies = int(copies)
                    admin.update_book(book_isbn, title, copies)
                elif admin_choice == 4:
                    print("SEARCHING BOOK")
                    book_isbn = input("Press enter or type a book isbn: ")
                    title = input("Press enter or type title: ")
                    author = input("Press enter or type author name: ")
                    if book_isbn != "":
                        book_isbn = int(book_isbn)
                    admin.search_book(book_isbn, title, author)

                elif admin_choice == 5:
                    print("ADDING MEMBER")
                    user = register()
                    admin.add_member(user)

                elif admin_choice == 6:
                    load_members()
                    print("REMOVING MEMBER")
                    u_id = input("Enter user id: ")
                    admin.delete_member(u_id)

                elif admin_choice == 7:
                    load_members()
                    print("UPDATING MEMBER")
                    u_id = input("Enter user id: ")
                    name = input("Enter press or type user name: ")
                    email = input("Enter press or type user email: ")
                    admin.update_member(u_id, name, email)
                elif admin_choice == 8:
                    print("GENERATING REPORT")
                    library.usage_report()
                elif admin_choice == 9:
                    print("ALL BOOKS")
                    library.show_all_books()
                elif admin_choice == 10:
                    print("ALL USERS")
                    library.show_all_members()
                else:
                    break

    elif choice == 3:
        user = register()
    else:
        break
