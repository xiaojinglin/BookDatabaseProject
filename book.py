import time
import csv

from models import session, Book
from get_input import (menu, menus, get_date, get_price,
                       get_id, clean_date, clean_price)


def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            title = row[0]
            author = row[1]
            date = clean_date(row[2])
            price = clean_price(row[3])
            Book.add(title, author, date, price)


def add_book():
    print('Add a New Book')
    title = input('Book Title: ')
    author = input('Author: ')
    date = get_date()
    price = get_price()
    Book.add(title, author, date, price)
    print('Book added!')
    time.sleep(1.5)


def update_book(the_book):
    book = {'title': the_book.title,
            'author': the_book.author, 
            'published date': the_book.published_date.strftime('%B %d, %Y'),
            'price': the_book.price/100}

    for key, value in book.items():
        print(f'Current {key}: {value}')
        choice = input(f'Enter "e" to edit {key} or "k" to keep the old {key}: ')
        if choice == 'k':
            continue
        elif choice == 'e':
            print(f'Enter the new value')
            if key == 'title':
                the_book.title = input(f'{key}:')
            elif key == 'author':
                the_book.author = input(f'{key}:')
            elif key == 'published date':
                the_book.published_date = get_date()
            elif key == 'price':
                the_book.price == get_price()
    session.commit()


def lib_search_sub(the_book):
    sub_choice = menu(menus['lib_book_sub'])
    if sub_choice == '1':
        update_book(the_book)
        print('Book updated!')
    elif sub_choice == '2':
        session.delete(the_book)
        session.commit()
        print('Book deleted!')


def member_search_sub(the_book,member_id):
    sub_choice = menu(menus['member_book_sub'])
    if sub_choice == '1':
        if the_book.member_id ==None:
            the_book.member_id = member_id
            print('Check out successfully!')
        else:
            print('This book is loaned')
    elif sub_choice == '2':
        if the_book.member_id == member_id:
            the_book.member_id =None                
            print('Book Returned!')
        else:
            print("You didn't borrow this book")


def search_book(member_id=None):
    id_options = []
    for id in session.query(Book.id):
        id_options.append(str(id.id))
    id_choice = get_id(id_options)
    the_book = Book.get(id_choice)
    print(f'''{the_book.title} by {the_book.author}
            \rPublished: {the_book.published_date}
            \rCurrent Price: ${the_book.price/100}''')
    if member_id == None:
        lib_search_sub(the_book)
    else:
        member_search_sub(the_book,member_id)
        session.commit()
    time.sleep(1.5)


def book_analysis():
    oldest_book  = session.query(Book).order_by(Book.published_date).first()
    newest_book  = session.query(Book).order_by(Book.published_date.desc()).first()
    total_books = session.query(Book).count()
    python_books = session.query(Book).filter(Book.title.like('%python%')).count()
    print(f'''\n********BOOK ANALYSIS********
          \rOldest book: {oldest_book}    
          \rNewest book: {newest_book}
          \rTotal Number of Books: {total_books}
          \rTotal Number of Python Books: {python_books}''')
    input('\nPress enter to return to the main menu')


def view_books():
    for book in session.query(Book):
        print(f'{book.id} | {book.title} | {book.author}')