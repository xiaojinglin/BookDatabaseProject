from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///books.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Book(Base):

    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    date_published = Column(Date)
    price = Column(Float)

    def __repr__(self):
        return f'<Book:(title={self.title}, author={self.author}, published date={self.date_published}, price={self.price})>'

if __name__ == '__main__':
    Base.metadata.create_all(engine)