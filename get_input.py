import datetime
from models import Member, session

menus = {
        'main_menu': ['Memeber', 'Librarian', 'Exit'],
        'lib_main': ['About members', 'About books','Exit'],
        'member_main': ['View all books', 'Search for a book', 'Exit'],
        'member_book_sub': ['Loan book', 'Return book', 'Return to main menu'],
        'lib_member_main': ['Add member', 'View all members', 'Search for a member', 'Return to main menu'],
        'lib_member_sub': ['Edit member', 'Delete member', 'Return to main menu'],
        'lib_book_main': ['Add Book', 'View all books', 'Search for a book', 'Book Analysis', 'Return to main menu'],
        'lib_book_sub': ['Edit book', 'Delete book', 'Return to main menu']
        }


def menu(menu_list):
    while True:
        for index, item in enumerate(menu_list, 1):
            print(f'{index}. {item}')
        choice = input('Choose a number: ')
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


def clean_phone():
    while True:
        phone = input('Phone number(eg: 5022002222)? ')
        if phone.isdigit() and len(phone) == 10:
            return phone
        else:
            print('Please enter a valid phone number, try again: ')
            continue


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
        id_choice = input('What is the id? ')
        if id_choice not in id_options:
             print('Choose a number in the options, try again.')
             continue
        else:
            return int(id_choice)


def get_member_id():
    while True:
        id = input('What is the your member id? ')
        if Member.get(int(id))==None:
             print('This id is not exist, try again')
             continue
        else:
            return int(id)