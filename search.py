"""Stores function to search by phrase"""
import re

import googlesearch

PATTERN = re.compile(r'^https?://xkcd.com/\d+/$')


def search(phrase: str) -> str:
    """Searches google for `phrase` on site:xkcd.com"""
    query = f'site:xkcd.com {str(phrase)}'
    result = googlesearch.search(query, num=10, start=0, stop=10, pause=2.0)
    for page in result:
        # Make sure site is xkcd.com and not forums.xkcd.com or other hits
        if PATTERN.match(page):
            return f'The most relevant xkcd found for the phrase \"{phrase}\" is: {page}'
    return "I searched through 10 links and didn't find a match. Maybe there's not always a relevant xkcd."
