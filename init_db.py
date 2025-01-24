from database import engine,Base
from models import User,Choice
 
Base.metadata.create_all(bind = engine)