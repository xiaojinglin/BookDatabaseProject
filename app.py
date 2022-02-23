from models import (engine, session,
                    Base, Book)


if __name__ == '__main__':
    Base.metadata.create_all(engine)