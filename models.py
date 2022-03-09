from sqlalchemy import (create_engine, Column,
                         Integer, String, Date, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine('sqlite:///library.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column('Title',String)
    author = Column('Author', String)
    published_date = Column('Published', Date)
    price = Column('Price', Integer)
    member_id = Column('MemberId', Integer)

    def __repr__(self):
        return f'<Title: {self.title}, Author: {self.author}, Published: {self.published_date}, Price: ${self.price/100}>'
    
    @staticmethod
    def get(id):
        return session.query(Book).filter(Book.id==id).first()

    @staticmethod
    def add(title, author, date, price):
        book_in_db = session.query(Book).filter(Book.title==title, 
                                        Book.author==author, 
                                        Book.published_date==date,
                                        Book.price==price).count()
        if book_in_db == 0:
                    new_book = Book(title=title, author=author, published_date=date, price=price)
                    session.add(new_book)
                    session.commit()


class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True)
    first_name = Column('FirstName', String)
    last_name = Column('LastName', String)
    phone = Column('Phone', String)

    def __repr__(self):
        return f'<Member Id: {self.id}, First Name: {self.first_name}, Last Name: {self.last_name}, Phone: {self.phone}>'
    
    @staticmethod
    def get(id):
        return session.query(Member).filter(Member.id==id).first()

    @staticmethod
    def add(first_name, last_name, phone):
        member_in_db = session.query(Member).filter(Member.first_name==first_name, 
                                        Member.last_name==first_name, 
                                        Member.phone==phone).count()
        if member_in_db == 0:
                    new_member = Member(first_name=first_name, last_name=first_name, phone=phone)
                    session.add(new_member)
                    session.commit()