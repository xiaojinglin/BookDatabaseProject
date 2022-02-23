from models import (engine, session,
                    Base, Book)
import csv
import datetime
import re


def menu():
    menu = ['1. Add Book', '2. View all books', '3. Search for a book', '4. Book Analysis', '5. Exit']
    while True:
        print('PROGRAMMING BOOKS')
        for m in menu:
            print(m)
        choice = input('What would you like to do? ')
        if choice not in ['1', '2', '3', '4', '5']:
            print('Choose a number between 1 to 5.')
            continue
        else:
            return choice


def clean_date(date_str):
    datetime_pub = datetime.datetime.strptime(date_str,'%B %d, %Y')
    return datetime_pub.date()


def clean_price(price_str):
    price_float = float(price_str)
    return int(price_float  * 100)


def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            title = row[0]
            author = row[1]
            date = clean_date(row[2])
            price = clean_price(row[3])
            book_in_db = session.query(Book).filter(Book.title==title, 
                                       Book.author==author, 
                                       Book.published_date==date,
                                       Book.price==price).count()
            if book_in_db == 0:
                new_book = Book(title=title, author=author, published_date=date, price=price)
                session.add(new_book)
        session.commit()
            


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            pass #add()
        elif choice == '2':
            pass #view()
        elif choice == '3':
            pass #search()
        elif choice == '4':
            pass #analysis()
        else:
            print('Goodbye')
            app_running = False

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # app()
    add_csv()
    for book in session.query(Book):
        print(book)