from typing import Optional

from attr import dataclass
from datetime import date


@dataclass
class TweetInformation:
	id: Optional[int] = None
	tweet_id: int = None
	time_of_load: str = None



