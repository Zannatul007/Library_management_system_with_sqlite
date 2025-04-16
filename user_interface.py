from library_management import *

while True:
    print("1: Login as a user")
    print("2: Login as an admin")
    print("3: Register")
    print("4: Exit")
    choice = int(input("Select your choice: "))
    if choice == 1:
        u_id = input("Enter your id: ")
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        user = User(u_id, name, email, password)
        if user.verify(email, password):
            while True:
                print("1: Borrow book")
                print("2: Return book")
                print("3: Show book transactions")
                print("4: Logout")

                user_choice = int(input("Select your choice: "))

                if user_choice == 1:
                    book_id = int(input("Enter book id you want to borrow: "))
                    user.borrow_book(book_id)
                elif user_choice == 2:
                    book_id = int(input("Enter book id you want to return: "))
                    user.return_book(book_id)
                elif user_choice == 3:
                    user.show_books_transaction()
                elif user_choice == 4:
                    break
        else:
            print("Incorrect password or email!!")

    elif choice == 2:
        u_id = input("Enter your id: ")
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        admin = Admin(u_id, name, email, password)
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
            print("9: Export csv")
            print("10: Show books")
            print("11: Show member")
            print("12: Logout")

            admin_choice = int(input("Select a number from 1 to 12:  "))

            if admin_choice == 1:
                book_isbn = int(input("Enter a book isbn: "))
                book_title = input("Enter book title: ")
                book_author = input("Enter book author: ")
                book_genre = input("Enter book genre: ")
                book_copies = int(input("Enter no of copies: "))
                book = Book(book_isbn, book_title, book_author, book_genre, book_copies)
                admin.add_book(book)
            elif admin_choice == 2:
                book_isbn = int(input("Enter a book isbn: "))
                admin.delete_book(book_isbn)
            elif admin_choice == 3:
                book_isbn = int(input("Enter a book isbn: "))
                title = input("Press enter or type title: ")
                copies = input("Press enter or no of copies: ")
                if copies is not "":
                    copies = int(copies)
                admin.update_book(book_isbn, title, copies)
            elif admin_choice == 4:
                book_isbn = input("Press enter or type a book isbn: ")
                title = input("Press enter or type title: ")
                author = input("Press enter or type author name: ")
                if book_isbn is not "":
                    book_isbn = int(book_isbn)
                admin.search_book(book_isbn, title, author)

            elif admin_choice == 5:
                u_id = input("Enter user id: ")
                name = input("Enter user name: ")
                email = input("Enter user email: ")
                password = input("Enter user password: ")
                user = User(u_id, name, email, password)
                admin.add_member(user)

            elif admin_choice == 6:
                u_id = input("Enter user id: ")
                admin.delete_member(u_id)

            elif admin_choice == 7:
                u_id = input("Enter user id: ")
                name = input("Enter press or type user name: ")
                email = input("Enter press or type user email: ")
                admin.update_member(u_id, name, email)
