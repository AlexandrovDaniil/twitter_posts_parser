from datetime import date
from typing import Optional

from attr import dataclass


@dataclass
class TweetInformation:
	id: Optional[int] = None
	tweet_id: int = None
	time_of_load: str = None



