from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, func

engine = create_engine('postgresql://postgres:2345@127.0.0.1:5431/flask_db')
Session = sessionmaker(bind=engine)

Base = declarative_base(bind=engine)


class Advertisements(Base):

    __tablename__ = 'advertisements'

    id = Column(Integer, primary_key=True, autoincrement=True)

    owner = Column(String, nullable=True, unique=True)
    header = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    creation_time = Column(DateTime, server_default=func.now())



Base.metadata.create_all()
