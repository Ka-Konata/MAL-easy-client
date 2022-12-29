import asyncio
from myanimelist.cogs.errors import *
from myanimelist.cogs.classes import *

class Search:
    '''Contain commands to search for a couple type os datas'''
    def __init__(self, args: Conection) -> None:
        self.connection = args


    async def user(self, username: str, full: bool = False) -> MalList[User]:
        '''
        Search someone\'s profile
        Uses: Jikan API

        NOTE: When searching with the correct username, this function will return a list containing only 1 item (the profile you are looking for). Otherwise, it returns a list of many possible profile matches. This happens because the JIKAN API does not return a search result if the username is correct.

        NOTE: In case you just want to get the profile right. uses the below function (returns None even if the username is incorrect or no profile is found)
        >>> user = await mal.search.user(\'username\').first()

        The below function from `get` module also do something like this, but better:
        >>> user = await mal.get.user('username') 
        
        :param str username: The one you want to search for
        :param str full: Shoult it return full user's profile or not (NOTE: only works if the user is found)

        :returns: if the username is correct -> A list with only 1 item (the result)
        :returns: if its incorrect -> A list with all matched results
        :returns: if not found -> None
        :rtype: list[User] 
        '''

        try:
            url = self.connection.jikan_api + f'/users?q={username}'
            res = get_json(requests.get(url))
            print(indent(res))
            res = get_list(res['data'], 'user')
            if len(res) == 0:
                raise requests.exceptions.HTTPError

        except requests.exceptions.HTTPError:
            url = self.connection.jikan_api + f'/users/{username}/full' if full else self.connection.jikan_api + f'/users/{username}'
            res = get_json(requests.get(url))
            if res == None:
                print('NOT FOUND')
                res = MalList()
            else:
                res = get_list([res['data']], 'user')

        #(res if len(res) != 0 else None)
        return res 


    async def anime(self, title: str, limit: int = 20) -> list[Anime]:
        '''
        Search for an anime
        Uses: MyAnimeList API
        
        :param str title: The anime you want to search for (must heve 3 caracteres or more)
        :param int limit: Max result list range

        :returns: A list with all matched results
        :rtype: list[Anime] 
        '''

        if len(title) < 3:
            return None

        query = f'q={title}&limit={limit}&fields=id,title,mean,num_episodes'
        url = self.connection.mal_api + f'/anime?{query}'

        res = get_json(requests.get(url, headers=self.connection.header))
        res = get_list(res['data'], 'anime') if res != None else res

        return res


    async def manga(self, title: str, limit: int = 20) -> list[Manga]:
        '''
        Search for a manga
        Uses: MyAnimeList API
        
        :param str title: The manga you want to search for (must heve 3 caracteres or more)
        :param int limit: Max result list range

        :returns: A list with all matched results
        :rtype: list[Manga] 
        '''
        
        if len(title) < 3:
            return None

        query = f'q={title}&limit={limit}&fields=id,title,mean,num_episodes'
        url = self.connection.mal_api + f'/manga?{query}'

        res = get_json(requests.get(url, headers=self.connection.header))
        res = get_list(res['data'], 'manga') if res != None else res

        return res
