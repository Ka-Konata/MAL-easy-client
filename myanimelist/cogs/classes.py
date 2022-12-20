import json, requests
from myanimelist.cogs.errors import *


class ListStatus:
    def __init__(self, data: dict) -> None:
        self.status               = get_value(data, 'status')
        self.score                = get_value(data, 'score')
        self.updated_at           = get_value(data, 'updated_at')

        # if type == 'anime':
        self.num_episodes_watched = get_value(data, 'num_episodes_watched')
        self.is_rewatching        = get_value(data, 'is_rewatching')

        # elif type == 'manga':
        self.num_volumes_read  = get_value(data, 'num_volumes_read')
        self.num_chapters_read = get_value(data, 'num_chapters_read')
        self.is_rereading      = get_value(data, 'is_rereading')


class Statistics:
    def __init__(self, data: dict) -> None:
        self.animes = self.AnimesStatic(get_value(data, 'anime'))
        self.mangas = self.AnimesStatic(get_value(data, 'manga'))


    class AnimesStatic:
        def __init__(self, data: dict) -> None:
            self.days_watched     = get_value(data, 'days_watched')
            self.mean_score       = get_value(data, 'mean_score')
            self.watching         = get_value(data, 'watching')
            self.completed        = get_value(data, 'completed')
            self.on_hold          = get_value(data, 'on_hold')
            self.dropped          = get_value(data, 'dropped')
            self.plan_to_watch    = get_value(data, 'plan_to_watch')
            self.total_entries    = get_value(data, 'total_entries')
            self.rewatched        = get_value(data, 'rewatched')
            self.episodes_watched = get_value(data, 'episodes_watched')


    class MangasStatic:
        def __init__(self, data: dict) -> None:
            self.days_read     = get_value(data, 'days_read')
            self.mean_score    = get_value(data, 'mean_score')
            self.reading       = get_value(data, 'reading')
            self.completed     = get_value(data, 'completed')
            self.on_hold       = get_value(data, 'on_hold')
            self.dropped       = get_value(data, 'dropped')
            self.plan_to_read  = get_value(data, 'plan_to_read')
            self.total_entries = get_value(data, 'total_entries')
            self.reread        = get_value(data, 'reread')
            self.chapters_read = get_value(data, 'chapters_read')
            self.volumes_read  = get_value(data, 'volumes_read')


class MalObj:
    def __init__(self, data: dict) -> None:
        self.id:str       = get_value(data, 'id')
        self.title        = get_value(data, 'title')
        self.image        = get_value(get_value(data, 'main_picture'), 'large')
        self.mean         = get_value(data, 'mean')


class Anime(MalObj):
    def __init__(self, data: dict) -> None:
        anime  = get_value(data, 'node')
        list_status = get_value(data, 'list_status')

        super().__init__(anime)
        self.num_episodes = get_value(anime, 'num_episodes')
        self.list_status = ListStatus(list_status) if list_status else None


class Manga(MalObj):
    def __init__(self, data: dict) -> None:
        manga  = get_value(data, 'node')
        list_status = get_value(data, 'list_status')

        super().__init__(manga)
        self.num_chapters = get_value(manga, 'num_chapters')
        self.list_status = ListStatus(list_status) if list_status else None


class User:
    def __init__(self, data: dict) -> None:
        self.mal_id      = get_value(data, 'mal_id')
        self.username    = get_value(data, 'username')
        self.url         = get_value(data, 'url')
        self.image       = get_value(get_value(data, 'images'), 'jpg')
        self.last_online = get_value(data, 'last_online')
        self.gender      = get_value(data, 'gender')
        self.joined      = get_value(data, 'joined')
        self.favorites   = get_value(data, 'favorites')
        self.statistics  = Statistics(get_value(data, 'statistics'))

        
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
    else:
        raise UnknownListType(type)
    return content


def get_value(data: dict, key: str) -> dict:
    try:
        return data[key]
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
