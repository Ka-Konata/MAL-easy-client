import asyncio
from myanimelist.cogs.errors import *
from myanimelist.cogs.classes import *


class Get:
    '''Contain commands to get especific datas'''
    def __init__(self, args: Conection) -> None:
        self.connection = args


    async def anime(self, id: int, fields:list = Fields.anime.basic()) -> Anime:
        '''
        Get an anime by id
        Uses: MyAnimeList API
        
        :param int id: The anime you want to get

        :returns: The anime you are looking for, if found
        :returns: None if not found
        :rtype: Anime
        '''
        fields_query = 'fields='
        c = 0
        for field in fields:
            fields_query = fields_query + field 
            if c < len(fields) - 1:
                fields_query = fields_query + ','
            c += 1

        url = self.connection.mal_api + f'/anime/{id}?{fields_query}'
        res = get_json(requests.get(url, headers=self.connection.header))

        return Anime({'node': res}) if res != None else res


    async def manga(self, id: int, fields:list = Fields.manga.basic()) -> Manga:
        '''
        Get a manga by id
        Uses: MyAnimeList API
        
        :param int id: The manga you want to get

        :returns: The manga you are looking for, if found
        :returns: None if not found
        :rtype: Manga 
        '''
        fields_query = 'fields='
        c = 0
        for field in fields:
            fields_query = fields_query + field 
            if c < len(fields) - 1:
                fields_query = fields_query + ','
            c += 1

        url = self.connection.mal_api + f'/manga/{id}?{fields_query}'
        print(url)
        res = get_json(requests.get(url, headers=self.connection.header))

        return Manga({'node': res}) if res != None else res


    async def user(self, username: str, full: bool = False) -> User:
        '''
        Get a user profile 
        Uses: Jikan API
        
        :param str username: The username you want to get (must be 3 characters or more)
        :param str full: Inform whether you want the full user profile user or not

        :returns: The user\'s profile
        :returns: None if not found
        :rtype: User 
        '''
        if  len(username) < 3:
            return None
            
        url = self.connection.jikan_api + f'/users/{username}/full' if full else self.connection.jikan_api + f'/users/{username}'
        res = get_json(requests.get(url))
        try:
            res = User(res['data'])
            return res
        except:
            return None


    async def username(self, id: int = None) -> str:
        '''
        Get username by id
        Uses: Jikan API
        
        :param int id: The username you want to get

        :returns: The username
        :returns: None if not found
        :rtype: str 
        '''
        if id == 0:
            print(str(id))
            return None
            
        url = self.connection.jikan_api + f'/users/userbyid/{id}'
        res = get_json(requests.get(url))
        try:
            res = User(res['data']).username
            return res
        except:
            return None


    async def anime_list(self, username: str, status: str = None, sort: str = 'anime_title', fields:list = Fields.anime.basic(), limit: int = 20) -> list[Anime]:
        '''
        Get a someone\'s anime list
        Uses: MyAnimeList API
        
        :param str username: The owner of the list you want
        :param str status: Returns only animes with this status
        :param str ordedby: The way the list will be sorted
        :param int limit: Limit size of anime list

        :returns: A list of all results found
        :rtype: list[User] 
        '''
        test_param(status, self.connection.usable_status_animes, UnknownStatusGiven)
        test_param(sort, self.connection.usable_orders_animes, UnknownSortGiven)
        if limit > 1000 or limit == 0:
            raise LimitExceeded(limit)

        fields_query = 'fields='
        for field in fields:
            fields_query = fields_query + ',' + field

        query = f'sort={sort}&limit={limit}&{fields_query}'
        query = query + f'&status={status}' if status != None else query
        url = self.connection.mal_api + f'/users/{username}/animelist?{query}'

        res = get_json(requests.get(url, headers=self.connection.header))
        print(indent(res))
        res = get_list(res['data'], 'anime') if res != None else res

        return res


    async def manga_list(self, username: str, status: str = None, sort: str = 'manga_title', fields:list = Fields.manga.basic(), limit: int = 20) -> list[Manga]:
        '''
        Get a someone\'s manga list
        Uses: MyAnimeList API
        
        :param str username: The owner of the list you want
        :param str status: Returns only mangas with this status
        :param str ordedby: The way the list will be sorted
        :param int limit: Limit size of manga list

        :returns: A list of all results found
        :rtype: list[User] 
        '''
        test_param(status, self.connection.usable_status_mangas, UnknownStatusGiven)
        test_param(sort, self.connection.usable_orders_mangas, UnknownSortGiven)
        if limit > 1000 or limit == 0:
            raise LimitExceeded(limit)

        fields_query = 'fields='
        for field in fields:
            fields_query = fields_query + ',' + field

        query = f'sort={sort}&limit={limit}&{fields_query}'
        query = query + f'&status={status}' if status != None else query
        url = self.connection.mal_api + f'/users/{username}/mangalist?{query}'

        res = get_json(requests.get(url, headers=self.connection.header))
        res = get_list(res['data'], 'manga') if res != None else res

        return res 