from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

url = "postgresql://postgres:0000@localhost/PizzaDelivery"
engine = create_engine(url , echo = True)

Base = declarative_base()

Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()