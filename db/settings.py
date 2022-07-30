from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, registry
from sqlalchemy import MetaData

from db.entities import TweetInformation

from datetime import datetime

from sqlalchemy import Column, Table
from sqlalchemy import Integer, String

engine = create_engine(
    # r'sqlite:///C:\Users\Daneksandrov\Desktop\
    # twitter_parser\twitter_posts_parser\test.db',
    # echo=False)
    r'sqlite:///test.db',
    echo=False)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
# metadata.create_all(engine)

last_load = Table(
    'last_load',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('time_of_load', String, nullable=False,
           default=str(datetime.utcnow())),
    Column('tweet_id', Integer, nullable=False),
)

if __name__ == '__main__':
    metadata.create_all(engine)