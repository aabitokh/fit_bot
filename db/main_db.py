import os
from db.base import Base, engine
from sqlalchemy.orm import sessionmaker
from models.db_models import Training_session

Session = sessionmaker(bind=engine)

def create_db() -> None:
    Base.metadata.create_all(engine)
    print("Database and tables created.")

def init_app() -> None:
    db_is_created = os.path.exists('main_db.sqlite')
    if not db_is_created:
        print("Database does not exist. Creating...")
        create_db()
    else:
        print("Database already exists.")