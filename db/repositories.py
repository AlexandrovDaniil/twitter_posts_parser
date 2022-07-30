from typing import Optional

from sqlalchemy.orm import registry

from db.settings import last_load

from db.entities import TweetInformation
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, registry
from sqlalchemy import MetaData

from db.entities import TweetInformation

from datetime import datetime

from sqlalchemy import Column, Table
from sqlalchemy import Integer, String

#
# engine = create_engine(
#     # r'sqlite:///C:\Users\Daneksandrov\Desktop\
#     # twitter_parser\twitter_posts_parser\test.db',
#     # echo=False)
#     r'sqlite:///test.db',
#     echo=False)
#
#
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# metadata = MetaData()
# metadata.create_all(engine)
#
# last_load = Table(
#     'last_load',
#     metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('time_of_load', String, nullable=False,
#            default=str(datetime.utcnow())),
#     Column('tweet_id', Integer, nullable=False),
# )
#
mapper_registry = registry()
mapper_registry.map_imperatively(TweetInformation, last_load)


class LastLoadRepo:
    def __init__(self, session_maker):
        self.session_maker = session_maker

    @property
    def session(self):
        if not getattr(self, '__session__', None):
            self.__session__ = self.session_maker

        return self.__session__

    def update_information(self, tweet_id: int, date_of_create: str):
        tweet_information = self.session.query(TweetInformation).one_or_none()

        if not tweet_information:
            new_tweet_information = TweetInformation(
                tweet_id=tweet_id,
                time_of_load=date_of_create
            )
            self.session.add(new_tweet_information)
            self.session.commit()
        else:
            tweet_information.tweet_id = tweet_id
            tweet_information.time_of_load = date_of_create
            self.session.commit()

    def get_last_load(self) -> Optional[TweetInformation]:
        tweet_information = self.session.query(TweetInformation).one_or_none()

        return tweet_information
