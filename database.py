from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

url = "postgresql://postgres:0000@localhost/PizzaDelivery"
engine = create_engine(url , echo = True)

Base = declarative_base()

Session = sessionmaker()   