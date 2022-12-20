import requests, json, asyncio, urllib
from myanimelist.cogs.errors import *
from myanimelist.cogs.classes import *

class Conection:
    header = dict()
    usable_status_animes = dict()
    usable_status_mangas = dict()
    usable_orders_animes = dict()
    usable_orders_mangas = dict()
    mal_api = str()
    jikan_api = str()


class Connect(Conection):
    '''
    Set up a client connected to both API\'s

    :param str client_id: Your client_id
    '''
    def __init__(self, client_id: str) -> None:
        super().__init__()
        self.header = {
            'X-MAL-CLIENT-ID': client_id
        }
        self.usable_status_animes = [
            None,
            'watching',
            'completed',
            'on_hold',
            'dropped',
            'plan_to_watch'
        ]
        self.usable_status_mangas = [
            None,
            'reading',
            'completed',
            'on_hold',
            'dropped',
            'plan_to_read'
        ]
        self.usable_orders_animes = [
            'list_score',
            'list_updated_at',
            'anime_title',
            'anime_start_date',	
            'anime_id'
        ]
        self.usable_orders_mangas = [
            'list_score',
            'list_updated_at',
            'manga_title',
            'manga_start_date',	
            'manga_id'
        ]
        self.mal_api = 'https://api.myanimelist.net/v2'
        self.jikan_api = 'https://api.jikan.moe/v4'

        self.get = self.Get(self) 
        self.search = self.Search(self)

        test = requests.get('https://api.myanimelist.net/v2/anime?q=Death Note', headers=self.header)
        if test.status_code == 404 or test.status_code == 400:
            raise Unauthorized


    class Get:
        '''Contain commands to get especific datas'''
        def __init__(self, args: Conection) -> None:
            self.connection = args


        async def anime(self, id: int) -> Anime:
            '''
            Get an anime
            Uses: MyAnimeList API
            
            :param int id: The anime you want to get

            :returns: A list with all results found
            :rtype: Anime 
            '''
            query = f'fields=id,title,mean,num_episodes'
            url = self.connection.mal_api + f'/anime/{id}?{query}'
            res = get_json(requests.get(url, headers=self.connection.header))

            return Anime({'node': res}) if res != None else res


        async def manga(self, id: int) -> Anime:
            '''
            Get an manga
            Uses: MyAnimeList API
            
            :param int id: The manga you want to get

            :returns: A list with all results found
            :rtype: Manga 
            '''
            query = f'fields=id,title,mean,num_chapters'
            url = self.connection.mal_api + f'/manga/{id}?{query}'
            res = get_json(requests.get(url, headers=self.connection.header))

            return Manga({'node': res}) if res != None else res


        async def user(self, username: str = None, full: bool = False) -> User:
            '''
            Get an manga
            Uses: Jikan API

            NOTE: Getting by id will return only username and url
            
            :param str username: The user that you want to get (must heve 3 caracteres or more)
            :param str full: Shoul it return full user's profile or not

            :returns: A list with all results found
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


        async def anime_list(self, username: str, status: str = None, orderedby: str = 'anime_title', limit: int = 20) -> MalList[User]:
            '''
            Get a someone\'s anime list
            Uses: MyAnimeList API
            
            :param str username: The owner of the list you want
            :param str status: Only return animes with this status
            :param str ordedby: Order list with this rule
            :param int limit: Max result list range

            :returns: A list with all results found
            :rtype: list[User] 
            '''
            test_param(status, self.connection.usable_status_animes, UnknownStatusGiven)
            test_param(orderedby, self.connection.usable_orders_animes, UnknownOrderedbyGiven)

            query = f'sort={orderedby}&limit={limit}&fields=id,title,mean,num_episodes,list_status'
            query = query + f'&status={status}' if status != None else query
            url = self.connection.mal_api + f'/users/{username}/animelist?{query}'

            res = get_json(requests.get(url, headers=self.connection.header))
            res = get_list(res['data'], 'anime') if res != None else res

            return res


        async def manga_list(self, username: str, status: str = None, orderedby: str = 'manga_title', limit: int = 20) -> list[Manga]:
            '''
            Get a someone\'s manga list
            Uses: MyAnimeList API
            
            :param str username: The owner of the list you want
            :param str status: Only return mangas with this status
            :param str ordedby: Order list with this rule
            :param int limit: Max result list range

            :returns: A list with all results found
            :rtype: list[Manga] 
            '''

            test_param(status, self.connection.usable_status_mangas, UnknownStatusGiven)
            test_param(orderedby, self.connection.usable_orders_mangas, UnknownOrderedbyGiven)

            query = f'sort={orderedby}&limit={limit}&fields=id,title,mean,num_chapters,list_status'
            query = query + f'&status={status}' if status != None else query
            url = self.connection.mal_api + f'/users/{username}/mangalist?{query}'

            res = get_json(requests.get(url, headers=self.connection.header))
            res = get_list(res['data'], 'manga') if res != None else res

            return res


    class Search:
        '''Contain commands to search for a couple type os datas'''
        def __init__(self, args: Conection) -> None:
            self.connection = args


        async def user(self, username: str, full: bool = False) -> list[User]:
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


"""
#url = 'users/PicaPauVelocista/animelist?fields=id,title,mean,list_status,num_episodes'
url = 'https://api.jikan.moe/v4/users/Ka_Knata/full'

#response = requests.get(url, headers = {
#    'X-MAL-CLIENT-ID': CLIENT_ID
#    })
"""
