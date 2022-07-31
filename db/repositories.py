from typing import Optional

from db.entities import TweetInformation
from db.settings import last_load
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import registry, sessionmaker

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
