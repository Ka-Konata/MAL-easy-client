'''
MAL-easy-client
~~~~~~~~~~~~~~~
A simple python library witch allows you to handle with both MAL API and Jikan API on an easier way
\nQUICK START

Set up a client connected to both API\'s
>>> import myanimelist
>>> import asyncio
>>> mal = myanimelist.Connect(\'YOUR_CLIENT_ID\')

Search for an anime
>>> anime = await mal.search.anime(\'Anime Title\')
>>> print(anime[0].title)

...Or get user anime list
>>> anime_list = await mal.get.user_anime_list(\'Username\')
>>> print(anime_list[0].title)

Avaiable commands
>>> search.user()
>>> search.anime()
>>> search.manga()
>>> get.user_anime_list()
>>> get.user_manga_list()
'''

from myanimelist.cogs.client import *