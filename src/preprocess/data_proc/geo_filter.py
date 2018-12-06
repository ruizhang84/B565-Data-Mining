from typing import Dict, Tuple, Union, Generator, Any
from data_proc import states

def _get_location_from_tweet(tweet : Dict[str, Any]) -> Union[str, bool]:
    if 'user' not in tweet or 'location' not in tweet['user']:
        return False
    # we're safe now
    return tweet['user']['location']

def _location_heuristics(location : str) -> bool:
    return (any((location.endswith(', ' + state_abbr) for state_abbr in states.keys())) or
            any((state in location for state in states.values())))

def geo_filter(tweets : Tuple[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
    for tweet in tweets:
        # applying location heuristics
        location = _get_location_from_tweet(tweet)
        if location and _location_heuristics(str(location)):
            yield tweet
