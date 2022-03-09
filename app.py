from models import (engine, session,
                    Base, Book, Member)
from get_input import menus, menu, get_member_id
from book import add_book, search_book, book_analysis, add_csv, view_books
from member import add_member, search_member


def lib_member_main():
    app_running = True
    while app_running:
        choice = menu(menus['lib_member_main'])
        if choice == '1':
            add_member()
        elif choice == '2':
            for member in session.query(Member):
                print(member)
            input('\nPress enter to return to the main menu')
        elif choice == '3':
            search_member()
        else:
            print('Goodbye')
            app_running = False


def lib_book_main():
    app_running = True
    while app_running:
        choice = menu(menus['lib_book_main'])
        if choice == '1':
            add_book()
        elif choice == '2':
            view_books()
            input('\nPress enter to return to the main menu')
        elif choice == '3':
            search_book()
        elif choice == '4':
            book_analysis()
        else:
            print('Goodbye')
            app_running = False


def lib_main():
    while True:
        choice = menu(menus['lib_main'])
        if choice == '1':
            lib_member_main()
        elif choice == '2':
            lib_book_main()
        else:
            exit()


def member_main(member_id):
    while True:
        choice = menu(menus['member_main'])
        if choice == '1':
            view_books()
        elif choice == '2':
            search_book(member_id)
        else:
            exit()

def app():
    app_running = True
    while app_running:
        choice = menu(menus['main_menu'])
        if choice == '1':
            member_id = get_member_id()
            member_main(member_id)
        elif choice == '2':
            lib_main()
        else:
            app_running = False

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    Member.add('John','Doe','5022222222')
    Member.add('Tim','Doe','5022222233')
    app()