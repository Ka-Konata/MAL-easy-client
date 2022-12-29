import requests, json, urllib
from myanimelist.cogs.errors import *
from myanimelist.cogs.classes import *
from myanimelist.cogs.methods.get import *
from myanimelist.cogs.methods.search import *


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

        test = requests.get('https://api.myanimelist.net/v2/anime?q=Death Note', headers=self.header)
        if test.status_code == 404 or test.status_code == 400:
            raise Unauthorized

        self.get = Get(self) 
        self.search = Search(self)
