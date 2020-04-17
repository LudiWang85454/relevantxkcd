import re
import aiohttp

PATTERN = re.compile(r"Permanent link to this comic: https?://xkcd\.com/(?P<num>\d+)/")


async def _get_latest_source():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://xkcd.com') as request:
            return await request.text()


async def latest_comic_num():
    latest_source = await _get_latest_source()
    if latest_source is not None:
        permalink = re.search(PATTERN, str(latest_source))
        return int(permalink.group("num"))
    return None #No latest source, likely internet problems
