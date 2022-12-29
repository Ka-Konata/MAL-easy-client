import asyncio
import myanimelist
from decouple import config

mal = myanimelist.Connect(config('CLIENT-ID'))

async def main():
    #username = await mal.get.username()
    #for item in search:
    #print(username)
    
    """search = await mal.get.user(username='Ka_Knata', full=True)
    print(f'''
        {search.id} {type(search.id)}
        {search.username} {type(search.username)}
        {search.url} {type(search.url)}
        {search.image} {type(search.image)}
        {search.last_online} {type(search.last_online)}
        {search.gender} {type(search.gender)}
        {search.joined} {type(search.joined)}
        {myanimelist.indent(search.favorites)} {type(search.favorites)}
        {search.statistics} {type(search.statistics)}
    ''')"""

    """search = await mal.get.anime_list('Ka_Knata', limit=1, fields=myanimelist.Fields.anime.basic())
    for item in search:
        print(f'''
        0:  {item.num_episodes}
        1:  {item.id} {type(item.id)}
        2:  {item.title} {type(item.title)}
        3:  {item.image} {type(item.image)}
        4:  {item.start_date} {type(item.start_date)}
        5:  {item.end_date} {type(item.end_date)}
        6:  {item.synopsis} {type(item.synopsis)}
        7:  {item.mean} {type(item.mean)}
        8:  {item.rank} {type(item.rank)}
        9:  {item.popularity} {type(item.popularity)}
        0:  {item.num_list_users} {type(item.num_list_users)}
        1:  {item.num_scoring_users} {type(item.num_scoring_users)}
        2:  {item.nsfw} {type(item.nsfw)}
        3:  {item.media_type} {type(item.media_type)}
        4:  {item.status} {type(item.status)}
        5:  {item.source} {type(item.source)}
        6:  {item.rating} {type(item.rating)}
        7:  {item.average_episode_duration} {type(item.average_episode_duration)}
        8:  {item.start_year} {type(item.start_year)}
        9:  {item.start_season} {type(item.start_season)}
        0:  {item.alternative_titles} {type(item.alternative_titles)}
        1:  {item.en_title} {type(item.en_title)}
        2:  {item.ja_title} {type(item.ja_title)}
        3:  {item.genres} {type(item.genres)}
        4:  {item.studios} {type(item.studios)}

        {item.list_status.status} {type(item.list_status.status)}
        {item.list_status.score} {type(item.list_status.score)}
        {item.list_status.updated_at} {type(item.list_status.updated_at)}
        {item.list_status.start_date} {type(item.list_status.start_date)}

        anime
        {item.list_status.num_episodes_watched} {type(item.list_status.num_episodes_watched)}
        {item.list_status.is_rewatching} {type(item.list_status.is_rewatching)}

        manga
        {item.list_status.num_volumes_read} {type(item.list_status.num_volumes_read)}
        {item.list_status.num_chapters_read} {type(item.list_status.num_chapters_read)}
        {item.list_status.is_rereading} {type(item.list_status.is_rereading)}
''')"""

    """item = await mal.get.manga('56805', fields=myanimelist.Fields.manga.basic())
    
    print(f'''
        0:  {item.num_chapters}
        0:  {item.num_volumes}
        1:  {item.id} {type(item.id)}
        2:  {item.title} {type(item.title)}
        3:  {item.image} {type(item.image)}
        4:  {item.start_date} {type(item.start_date)}
        5:  {item.end_date} {type(item.end_date)}
        6:  {item.synopsis} {type(item.synopsis)}
        7:  {item.mean} {type(item.mean)}
        8:  {item.rank} {type(item.rank)}
        9:  {item.popularity} {type(item.popularity)}
        0:  {item.num_list_users} {type(item.num_list_users)}
        1:  {item.num_scoring_users} {type(item.num_scoring_users)}
        2:  {item.nsfw} {type(item.nsfw)}
        3:  {item.media_type} {type(item.media_type)}
        4:  {item.status} {type(item.status)}
        5:  {item.alternative_titles} {type(item.alternative_titles)}
        6:  {item.en_title} {type(item.en_title)}
        7:  {item.ja_title} {type(item.ja_title)}
''')

    #search = await mal.search.manga('Komi-san')
    #for anime in search:
    #    print(f'{anime.id} - {anime.title}')

    #anime = await mal.get.manga('Komi-san wa, Comyushou desu.')
    #print(f'{anime.id} {anime.title}')"""

asyncio.run(main())
