from models import (engine, session,
                    Base, Book)

    
import csv
import time
import datetime
import re

menus = {'main_menu': ['Add Book', 'View all books', 'Search for a book', 'Book Analysis', 'Exit'],
        'sub_menu': ['Edit entry', 'Delete entry', 'Return to main menu']
        }


def menu(menu_list):
    while True:
        for index, item in enumerate(menu_list, 1):
            print(f'{index}. {item}')
        choice = input('What would you like to do? ')
        if choice.isdigit() and int(choice) in range(len(menu_list)+1):
            return choice
        else:
            print(f'Choose a number between 1 and {len(menu_list)}.')
            continue
            

def clean_date(date_str):
    datetime_pub = datetime.datetime.strptime(date_str,'%B %d, %Y')
    return datetime_pub.date()


def clean_price(price_str):
    price_float = float(price_str)
    return int(price_float  * 100)

def add_book(title, author, date, price):
    book_in_db = session.query(Book).filter(Book.title==title, 
                                       Book.author==author, 
                                       Book.published_date==date,
                                       Book.price==price).count()
    if book_in_db == 0:
                new_book = Book(title=title, author=author, published_date=date, price=price)
                session.add(new_book)


def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            title = row[0]
            author = row[1]
            date = clean_date(row[2])
            price = clean_price(row[3])
            add_book(title, author, date, price)
        session.commit()


def get_date():
    while True:
        try:
            enter = input('Published (Example: January 13, 2003): ')
            date = clean_date(enter)
        except ValueError:
            print('Invalid Input, try again.')
            continue
        else:
            return date


def get_price():
    while True:
        try:
            enter = input('Price (Example: 10.99): ')
            price = clean_price(enter)
        except ValueError:
            print('Invalid Input, try again.')
            continue
        else:
            return price


def get_id(id_options):
    id_str = ', '.join(id_options)   
    while True:
        print(f'Options: {id_str}')
        id_choice = input('What is the book\'s id? ')
        if id_choice not in id_options:
             print('Choose a number in the options, try again.')
             continue
        else:
            return int(id_choice)

def add():
    print('Add a New Book')
    title = input('Book Title: ')
    author = input('Author: ')
    date = get_date()
    price = get_price()
    add_book(title, author, date, price)
    session. commit()
    print('Book added!')
    time.sleep(1.5)


def update(the_book):
    book = {'Title': the_book.title,
            'Author': the_book.author, 
            'Published': the_book.published_date,
            'Price': the_book.price/100}

    for key, value in book.items():
        print(f'{key}: {value}')
        choice = input('Enter "e" to edit {key} or "k" to keep the old {key}: ')
        if choice == 'k':
            continue
        elif choice == 'e':
            print(f'Enter the new {key}')
            if key == 'Title':
                the_book.title = input(f'{key}:')
            elif key == 'Author':
                the_book.author = input(f'{key}:')
            elif key == 'Published':
                the_book.published_date = get_date()
            elif key == 'Price':
                the_book.price == get_price()

    session.commit()


def search():
    id_options = []
    for id in session.query(Book.id):
        id_options.append(str(id.id))
    id_choice = get_id(id_options)
    the_book = session.query(Book).filter(Book.id==id_choice).first()
    print(f'''{the_book.title} by {the_book.author}
            \rPublished: {the_book.published_date}
            \rCurrent Price: ${the_book.price/100}''')
    sub_choice = menu(menus['sub_menu'])
    if sub_choice == '1':
        update(the_book)
        print('Book edited!')
        time.sleep(1.5)
    elif sub_choice == '2':
        session.delete(the_book)
        session.commit()
        print('Book deleted!')
        time.sleep(1.5)


def app():
    app_running = True
    print('PROGRAMMING BOOKS')
    while app_running:
        choice = menu(menus['main_menu'])
        if choice == '1':
            add()
        elif choice == '2':
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author}')
            input('\nPress enter to return to the main menu')
        elif choice == '3':
            search()
        elif choice == '4':
            pass #analysis()
        else:
            print('Goodbye')
            app_running = False

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    
    add_csv()
    app()
    # for book in session.query(Book):
    #     print(book)
    # add()
    # search()