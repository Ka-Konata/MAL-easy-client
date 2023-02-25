import json, requests
from datetime import datetime, date
from myanimelist.cogs.errors import *


class Fields:
    class anime:
        def all():
            return ['id', 'title', 'main_picture', 'alternative_titles', 'start_date', 'end_date', 'synopsis', 'mean', 'rank', 'popularity', 'num_list_users', 'num_scoring_users', 'nsfw', 'genres', 'media_type', 'status', 'num_episodes', 'start_season', 'source', 'average_episode_duration', 'rating', 'studios', 'statistics', 'list_status']
        def basic():
            return ['id', 'title', 'main_picture', 'mean', 'rank', 'popularity', 'status', 'num_episodes', 'list_status']

    class manga:
        def all():
            return ['id', 'title', 'main_picture', 'alternative_titles', 'start_date', 'end_date', 'synopsis', 'mean', 'rank', 'popularity', 'num_list_users', 'num_scoring_users', 'nsfw', 'genres', 'created_at', 'updated_at', 'media_type', 'status', 'num_chapters', 'num_volumes', 'statistics', 'list_status']
        def basic():
            return ['id', 'title', 'main_picture', 'mean', 'rank', 'popularity', 'status', 'num_chapters', 'num_volumes', 'list_status']


class Conection:
    header               :dict = dict()
    usable_status_animes :dict = dict()
    usable_status_mangas :dict = dict()
    usable_orders_animes :dict = dict()
    usable_orders_mangas :dict = dict()
    mal_api              :str  = str()
    jikan_api            :str  = str()


class ListStatus:
    def __init__(self, data: dict, type:str) -> None:
        self.status               :str  = get_value(data, 'status')
        self.score                :int  = get_value(data, 'score')
        self.updated_at           :date = get_value(data, 'updated_at', 'datetime')
        self.start_date           :date = get_value(data, 'start_date', 'datetime')
        #if type == 'anime':
        self.num_episodes_watched :int  = get_value(data, 'num_episodes_watched')
        self.is_rewatching        :bool = get_value(data, 'is_rewatching')
        #elif type == 'manga':
        self.num_volumes_read     :int  = get_value(data, 'num_volumes_read')
        self.num_chapters_read    :int  = get_value(data, 'num_chapters_read')
        self.is_rereading         :bool = get_value(data, 'is_rereading')


class Statistics:
    def __init__(self, data: dict) -> None:
        self.animes :AnimesStatic = AnimesStatic(get_value(data, 'anime'))
        self.mangas :MangasStatic = MangasStatic(get_value(data, 'manga'))


class AnimesStatic:
    def __init__(self, data: dict) -> None:
        self.days_watched     :float = get_value(data, 'days_watched')
        self.mean_score       :float = get_value(data, 'mean_score')
        self.watching         :int   = get_value(data, 'watching')
        self.completed        :int   = get_value(data, 'completed')
        self.on_hold          :int   = get_value(data, 'on_hold')
        self.dropped          :int   = get_value(data, 'dropped')
        self.plan_to_watch    :int   = get_value(data, 'plan_to_watch')
        self.total_entries    :int   = get_value(data, 'total_entries')
        self.rewatched        :int   = get_value(data, 'rewatched')
        self.episodes_watched :int   = get_value(data, 'episodes_watched')


class MangasStatic:
    def __init__(self, data: dict) -> None:
        self.days_read     :float = get_value(data, 'days_read')
        self.mean_score    :float = get_value(data, 'mean_score')
        self.reading       :int   = get_value(data, 'reading')
        self.completed     :int   = get_value(data, 'completed')
        self.on_hold       :int   = get_value(data, 'on_hold')
        self.dropped       :int   = get_value(data, 'dropped')
        self.plan_to_read  :int   = get_value(data, 'plan_to_read')
        self.total_entries :int   = get_value(data, 'total_entries')
        self.reread        :int   = get_value(data, 'reread')
        self.chapters_read :int   = get_value(data, 'chapters_read')
        self.volumes_read  :int   = get_value(data, 'volumes_read')


class MalObj:
    def __init__(self, data: dict) -> None:
        self.id                       :int   = get_value(data, 'id')
        self.title                    :str   = get_value(data, 'title')
        self.image                    :str   = get_value(get_value(data, 'main_picture'), 'large')
        self.start_date               :date  = get_value(data, 'start_date', 'datetime')
        self.end_date                 :date  = get_value(data, 'end_date', 'datetime')
        self.synopsis                 :str   = get_value(data, 'synopsis')
        self.mean                     :float = get_value(data, 'mean')
        self.rank                     :int   = get_value(data, 'rank')
        self.popularity               :int   = get_value(data, 'popularity')
        self.num_list_users           :int   = get_value(data, 'num_list_users')
        self.num_scoring_users        :int   = get_value(data, 'num_scoring_users')
        self.nsfw                     :str   = get_value(data, 'nsfw')
        self.media_type               :str   = get_value(data, 'media_type')
        self.status                   :str   = get_value(data, 'status')
        self.alternative_titles       :list  = get_value(get_value(data, 'alternative_titles'), 'synonyms')
        self.en_title                 :str   = get_value(get_value(data, 'alternative_titles'), 'en')
        self.ja_title                 :str   = get_value(get_value(data, 'alternative_titles'), 'ja')

        genres = get_value(data, 'genres')
        self.genres:list = None
        if genres != None:
            self.genres:list = list()
            for genre in genres:
                self.genres.append(genre['name'])


class Anime(MalObj):
    def __init__(self, data: dict) -> None:
        anime  = get_value(data, 'node')
        list_status = get_value(data, 'list_status')

        super().__init__(anime)
        self.num_episodes             :int        = get_value(anime, 'num_episodes')
        self.source                   :str        = get_value(anime, 'source')
        self.rating                   :str        = get_value(anime, 'rating')
        self.average_episode_duration :int        = get_value(anime, 'average_episode_duration')
        self.start_year               :int        = get_value(get_value(anime, 'start_season'), 'year')
        self.start_season             :str        = get_value(get_value(anime, 'start_season'), 'season')
        self.list_status              :ListStatus = ListStatus(list_status, 'anime') if list_status else None
        
        studios = get_value(anime, 'studios')
        self.studios:list = None
        if studios != None:
            self.studios:list = list()
            for studio in studios:
                self.studios.append(studio['name'])


class Manga(MalObj):
    def __init__(self, data: dict) -> None:
        manga  = get_value(data, 'node')
        list_status = get_value(data, 'list_status')

        super().__init__(manga)
        self.num_chapters :int        = get_value(manga, 'num_chapters')
        self.num_volumes  :int        = get_value(manga, 'num_volumes')
        self.list_status  :ListStatus = ListStatus(list_status, manga) if list_status else None


class FavObj:
    def __init__(self, data: dict) -> None:
        self.id         :int = get_value(data, 'mal_id')
        self.url        :str = get_value(data, 'url')
        self.images     :str = get_value(get_value(get_value(data, 'images'), 'jpg'), 'image_url')
        self.title      :str = get_value(data, 'title')
        self.type       :str = get_value(data, 'type')
        self.start_year :int = get_value(data, 'start_year')


class People:
    def __init__(self, data: dict) -> None:
        self.id     :int = get_value(data, 'mal_id')
        self.url    :str = get_value(data, 'url')
        self.images :str = get_value(get_value(get_value(data, 'images'), 'jpg'), 'image_url')
        self.name   :str = get_value(data, 'name')


class Character:
    def __init__(self, data: dict) -> None:
        self.id :int = get_value(data, 'mal_id')
        self.url    :str = get_value(data, 'url')
        self.images :str = get_value(get_value(get_value(data, 'images'), 'jpg'), 'image_url')
        self.name   :str = get_value(data, 'name')


class Favorites:
    def __init__(self, data: dict) -> None:
        self.animes     :MalList = get_list(data['anime'], 'favobj')
        self.mangas     :MalList = get_list(data['manga'], 'favobj')
        self.peoples    :MalList = get_list(data['people'], 'people')
        self.characters :MalList = get_list(data['characters'], 'character')


class User:
    def __init__(self, data: dict) -> None:
        self.id          :int        = get_value(data, 'mal_id')
        self.username    :str        = get_value(data, 'username')
        self.url         :str        = get_value(data, 'url')
        self.image       :str        = get_value(get_value(get_value(data, 'images'), 'jpg'), 'image_url')
        self.last_online :date       = get_value(data, 'last_online', 'datetime')
        self.gender      :str        = get_value(data, 'gender')
        self.joined      :date       = get_value(data, 'joined', 'datetime')
        self.favorites   :Favorites  = Favorites(get_value(data, 'favorites'))
        self.statistics  :Statistics = Statistics(get_value(data, 'statistics'))


class MalList(list):
    def __init__(self) -> None:
        super().__init__()


    def first(self) -> MalObj:
        '''
        Get only the first item of the list

        WHY SHOULD I USE THIS? If this is inside a `search.user()` function then you might want to get None if the result is not accurate. 
        FOR EXAMPLE: Exists a profile with username "MyProfile", and you\'d search for "ThatProfile", the original `search.user()` function would return a list with all possible profiles matches, while `search.user().first()` will return None.
        NOTE: The function `get.user()` do the same thing, but better.
        
        :returns: if found -> The user\'s profile
        :returns: if not found -> None
        :rtype: list[User] 
        '''
        if len(self) == 1:
            return self[0]
        else:
            return None


def get_list(data: dict, type: str) -> MalList:
    content = MalList()

    if type == 'anime':
        for anime in data:
            content.append(Anime(anime))
    elif type == 'manga': 
        for manga in data:
            content.append(Manga(manga))
    elif type == 'user':
        for user in data:
            content.append(User(user))
    elif type == 'favobj':
        for obj in data:
            content.append(FavObj(obj))
    elif type == 'people':
        for people in data:
            content.append(People(people))
    elif type == 'character':
        for character in data:
            content.append(Character(character))
    else:
        raise UnknownListType(type)
    return content


def get_value(data: dict, key: str, converter:str = None) -> str:
    try:
        res = data[key]

        if converter != None and res != None:
            if converter == 'datetime':
                try:
                    res = datetime.strptime(res[:10], '%Y/%m/%d').date()
                except:
                    None

        return res
    except (KeyError, TypeError):
        return None


def get_json(response: requests.Response) -> dict:
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as Error:
        if response.status_code == 404:
            return None
        else:
            raise Error

    results = response.json()
    response.close()
    return results


def test_param(arg: str, source: list, exception: Exception) -> None:
    if not arg in source:
        raise exception(arg)


def indent(data):
    '''
    Return indented data for better vizualization
    
    params:
    (Any) data: data to be indented
    '''
    return json.dumps(data, indent=4)
