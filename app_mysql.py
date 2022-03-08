import mysql.connector as mysql
import csv
import time
import datetime


myhost = "localhost"
myuser = "python"
mypass = "pythonmysql"

db = mysql.connect(host=myhost ,user=myuser,password=mypass,database="mydatabase")   
cur = db.cursor(buffered = True)
cur.execute("DROP TABLE IF EXISTS books")
sql_create = ''' CREATE TABLE IF NOT EXISTS books(
                                            id INT AUTO_INCREMENT PRIMARY KEY,
                                            title VARCHAR(255),
                                            author VARCHAR(255),
                                            publish_date DATE,
                                            price INT
                                            )'''
cur.execute(sql_create)

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

def add_book(title,author,date,price):
    sql = "SELECT * FROM books where title=%s"
    book = cur.execute(sql,(title,))
    if book==None:
        sql = "INSERT INTO books (title,author,publish_date,price) VALUES (%s,%s,%s,%s)"
        val = (title,author,date,price)
        cur.execute(sql,val)
        db.commit()


def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            title = row[0]
            author = row[1]
            date = clean_date(row[2])
            price = clean_price(row[3])
            add_book(title,author,date,price)


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
    print('Book added!')
    time.sleep(1.5)


def update(the_book):
    the_book = list(the_book)
    book = {'title': the_book[1],
            'author': the_book[2], 
            'published date': the_book[3].strftime('%B %d, %Y'),
            'price': the_book[4]/100}

    for key, value in book.items():
        print(f'Current {key}: {value}')
        choice = input(f'Enter "e" to edit {key} or "k" to keep the old {key}: ')
        if choice == 'k':
            continue
        elif choice == 'e':
            print(f'Enter the new value')
            if key == 'title':
               the_book[1] = input(f'{key}:')
            elif key == 'author':
                the_book[2] = input(f'{key}:')
            elif key == 'published date':
                the_book[3] = get_date()
            elif key == 'price':
                the_book[4] == get_price()
    sql = "UPDATE books SET title=%s, author=%s, publish_date=%s, price=%s WHERE id=%s "
    val = (the_book[1],the_book[2],the_book[3],the_book[4],the_book[0])
    cur.execute(sql,val)
    db.commit()

def search():
    id_options = []
    sql = "SELECT id FROM books"
    cur.execute(sql)
    for id in cur.fetchall():
        id_options.append(str(id[0]))
    id_choice = get_id(id_options)
    sql = "SELECT * FROM books WHERE id=%s"
    cur.execute(sql,(id_choice,))
    the_book = cur.fetchone()
    print(f'''{the_book[1]} by {the_book[2]}
            \rPublished: {the_book[3]}
            \rCurrent Price: ${the_book[4]/100}''')
    sub_choice = menu(menus['sub_menu'])
    if sub_choice == '1':
        update(the_book)
        print('Book updated!')
        time.sleep(1.5)
    elif sub_choice == '2':
        sql = "DELETE FROM books WHERE id=%s"
        cur.execute(sql,(id_choice,))
        db.commit()
        print('Book deleted!')
        time.sleep(1.5)


def analysis():
    cur.execute("SELECT * FROM books ORDER BY publish_date")
    books = cur.fetchall()
    print(books)
    oldest_book  = books[0]
    newest_book  = books[-1]
    total_books = cur.rowcount
    cur.execute("SELECT * FROM books WHERE title like '%python%'")
    print(f'''\n********BOOK ANALYSIS********
          \rOldest book: {oldest_book[1]}
          \rNewest book: {newest_book[2]}
          \rTotal Number of Books: {total_books}
          \rTotal Number of Python Books: {cur.rowcount}''')
    input('\nPress enter to return to the main menu')

def app():
    app_running = True
    print('PROGRAMMING BOOKS')
    while app_running:
        choice = menu(menus['main_menu'])
        if choice == '1':
            add()
        elif choice == '2':
            cur.execute("SELECT * FROM books")
            for book in cur.fetchall():
                print(f'{book[0]} | {book[1]} | {book[2]}')
            input('\nPress enter to return to the main menu')
        elif choice == '3':
            search()
        elif choice == '4':
            analysis()
        else:
            print('Goodbye')
            app_running = False


if __name__ == "__main__":
    add_csv()
    app()
    cur.close()
    