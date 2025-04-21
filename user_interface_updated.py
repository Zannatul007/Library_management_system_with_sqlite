from library_management import *
from auth import *
import datetime


def get_int():
    while True:
        try:
            return int(input(("> ")))
        except ValueError:
            print("Not a valid number")


def take_date(date):
    format = "%Y-%m-%d"
    x = datetime.datetime.strptime(date, format)
    return x


def get_date():
    while True:
        try:
            date = input()
            return take_date(date)
        except ValueError:
            print("Invalid format of time")


while True:
    print("1. Login")
    print("2. Register")
    print("3. Exit")
    print("Select option: ")
    ip = get_int()

    if ip == 1:
        user = login()
        # print(user)
        if user is not None:
            if user.role == 1:
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

                    print("Select a number from 1 to 12:  ")
                    admin_choice = get_int()

                    if admin_choice == 1:
                        print("ADDING BOOK")

                        book_title = input("Enter book title: ")
                        book_author = input("Enter book author: ")
                        book_genre = input("Enter book genre: ")
                        print("Enter no of copies: ")
                        book_copies = get_int()
                        book = Book(book_title, book_author, book_genre, book_copies)
                        user.add_book(book)
                    elif admin_choice == 2:
                        print("REMOVING BOOK")
                        load_books()
                        print("Enter a book ISBN")
                        print("Enter 0 for go back :")
                        book_isbn = get_int()
                        if book_isbn == 0:
                            continue

                        user.delete_book(book_isbn)
                    elif admin_choice == 3:
                        print("UPDATING BOOK")
                        load_books()
                        print("Enter a book isbn: ")
                        print("Enter 0 for go back")
                        book_isbn = get_int()
                        if book_isbn == 0:
                            continue
                        title = input("Press enter or type title: ")
                        copies = input("Press enter or no of copies: ")
                        if copies != "":
                            copies = int(copies)
                        user.update_book(book_isbn, title, copies)
                        print("Updation is successful")
                    elif admin_choice == 4:
                        print("SEARCHING BOOK")
                        title = input("Press enter or type title: ")
                        user.search_book(title)

                    elif admin_choice == 5:
                        print("ADDING MEMBER")
                        user = register()

                    elif admin_choice == 6:
                        load_members()
                        print("REMOVING MEMBER")
                        print("Enter 0 for go back")
                        print("Enter user id for removing member: ")
                        u_id = get_int()
                        if u_id == 0:
                            continue

                        user.delete_member(u_id)

                    elif admin_choice == 7:
                        load_members()
                        print("UPDATING MEMBER")
                        print("Enter user id: ")
                        u_id = get_int()
                        name = input("Enter press or type user name: ")
                        email = input("Enter press or type user email: ")
                        user.update_member(u_id, name, email)
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

            elif user.role == "Member":
                while True:
                    print("1: Borrow book")
                    print("2: Return book")
                    print("3: Show book transactions")
                    print("4: Logout")

                    print("Select your choice: ")
                    user_choice = get_int()

                    if user_choice == 1:
                        load_books()
                        print("BORROWING BOOK")
                        print("Enter book ISBN you want to borrow: ")
                        book_id = get_int()
                        print("Enter borrow date(YYYY-MM-DD): ")
                        borrow_date = get_date()
                        user.borrow_book(book_id, borrow_date)
                    elif user_choice == 2:
                        user.show_books_transaction()
                        print("RETURNING BOOK")
                        print("Enter book ISBN you want to return: ")
                        book_id = get_int()
                        return_date = datetime.datetime.now()
                        user.return_book(book_id, return_date)
                    elif user_choice == 3:
                        print("SHOW ALL TRANSACTIONS")
                        user.show_books_transaction()
                    elif user_choice == 4:
                        break
        # else:
        #     print("Invalid")
    if ip == 2:
        user = register()
    if ip == 3:
        break
