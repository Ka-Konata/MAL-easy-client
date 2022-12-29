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
>>> anime_list = await mal.get.anime_list(\'Username\')
>>> print(anime_list[0].title)

Avaiable commands
\n`search.user()` - Search for an user
\n`search.anime()` - Search for an anime
\n`search.manga()` - Search fo a manga
\n`get.user()` - Get an user profile
\n`get.username()` - Get username by id
\n`get.anime_list()` - Get an user anime list
\n`get.manga_list()` - Get an user manga list
'''

from myanimelist.cogs.client import *