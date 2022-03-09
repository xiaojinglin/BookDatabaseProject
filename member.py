import time

from get_input import clean_phone, get_id, menu,menus
from models import session, Member


def add_member():
    print('Add a New Member')
    first_name = input('First Name: ')
    last_name = input('Last Name: ')
    phone = clean_phone()
    Member.add(first_name,last_name,phone)
    print('member added!')
    time.sleep(1.5)


def update_member(the_member):
    member = {'First name': the_member.first_name,
                   'Last Name': the_member.last_name,
                   'phone': the_member.phone}

    for key, value in member.items():
        print(f'Current {key}: {value}')
        choice = input(f'Enter "e" to edit {key} or "k" to keep the old {key}: ')
        if choice == 'k':
            continue
        elif choice == 'e':
            print(f'Enter the new value')
            if key == 'phone':
                the_member.phone = clean_phone()
            elif key == 'First Name':
                the_member.first_name = input(f'{key}:')
            else:
                the_member.last_name = input(f'{key}:')
    session.commit()

def search_member():
    id_options = []
    for id in session.query(Member.id):
        id_options.append(str(id.id))
    id_choice = get_id(id_options)
    the_member = Member.get(id_choice)
    print(the_member)
    sub_choice = menu(menus['lib_member_sub'])
    if sub_choice == '1':
        update_member(the_member)
        print('Member updated!')
    elif sub_choice == '2':
        session.delete(the_member)
        session.commit()
        print('Member deleted!')
    time.sleep(1.5)