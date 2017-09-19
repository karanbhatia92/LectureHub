from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float

engine = create_engine('sqlite:///test.db', echo=True)
Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    user = Column(String, primary_key=True)
    user_type = Column(Integer)
    password = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

new_user = Users(user="shruti.p@gmail.com", user_type=0, password="pwd")
session.add(new_user)
session.commit()
