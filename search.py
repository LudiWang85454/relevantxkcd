import re

import googlesearch

PATTERN = re.compile(r'^https?://xkcd.com/\d+/$')


def search(phrase):
    query = f'site:xkcd.com {str(phrase)}'
    first = -1
    last = links = 0
    while True:
        first += 1
        last += 1
        if links >= 10:
            return "I searched through 10 links and didn't find a match. Maybe there's not always a relevant xkcd."
        result = googlesearch.search(query, num=10, start=first, stop=last, pause=2.0)
        for page in result:
            links += 1
            if PATTERN.match(page):
                return f'The most relevant xkcd found for the phrase \"{phrase}\" is: {page}'