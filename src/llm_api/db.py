from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///test.db") #TODO: 오라클로 교체 필요
session = sessionmaker(bind = engine)