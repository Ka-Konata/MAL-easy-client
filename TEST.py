import asyncio
import myanimelist
from decouple import config

mal = myanimelist.Connect(config('CLIENT-ID'))

async def main():
    search = await mal.get.user('')
    #for item in search:
    print(f'ID: {search.mal_id} {search.username}')
    
asyncio.run(main())
