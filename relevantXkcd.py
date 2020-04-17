import asyncio
import random
import re
import webbrowser

from googlesearch import search

from newest_xkcd import latest_comic_num

url = "https://xkcd.com/"
searchType = input("Do you want to search by NUMBER, PHRASE, or RANDOM?").lower()

if searchType == "number":
    comicNumber = input("What is the number of the comic you want to search?")
    try:
        requested = int(comicNumber)
        latest = asyncio.run(latest_comic_num())
        if latest is None:
            print("Having trouble connecting to xkcd.com")
        elif latest < requested:
            print("That comic doesn't exist yet silly!")
        else:
            url = (f'{url}{comicNumber}')
            webbrowser.open_new(url)
    except:
        print("An error occured. Perhaps you didn't enter an integer, or you don't have a recognized web browser, or dark magic interfered. The world may never know.")
        webbrowser.open_new("https://xkcd.com/2200/")
elif searchType == "phrase":
    pattern = r"^https?://xkcd.com/\d+/$" # Matches url for an xkcd, with or without https
    referencePhrase = input("What is the relevant phrase?")
    num_results = input("How many xkcds would you like to search for?")
    query = ("site:xkcd.com " + str(referencePhrase))
    try:
        i = int(num_results)
        for result in search(query, num=20):
            if i <= 0:
                break
            if re.match(pattern, result) is not None: # Result matches pattern
                i -= 1
                webbrowser.open_new(result)
    except:
        print("An error occured. Perhaps you didn't enter an integer for the number of searches, or you don't have google, or maybe its all my fault and I really am a disappointment like my parents said.")
        webbrowser.open_new("https://xkcd.com/2200/")
elif searchType == "random":
    newest_comic = asyncio.run(latest_comic_num())
    comic_num = random.randint(1, newest_comic)
    random_url = (f"{url}{comic_num}")
    webbrowser.open_new(random_url)
else:
    webbrowser.open_new("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
