from typing import List
from requests import get
from loguru import logger
from bs4 import BeautifulSoup
from composition import Composition


SRC = 'https://amdm.ru/search/'


@logger.catch
def find_conposition(key_world: str) -> List[Composition] | None:
    params = {'q': key_world}
    res = get(SRC, params=params)
    
    logger.info(f'find = {key_world}')
    logger.info(f'response status = {res.status_code}')
    
    compositions: List[Composition] = []
    if res:
        html = BeautifulSoup(res.text, 'html.parser')
        td_compositions = html.find_all('td', {'class': 'artist_name'})
        
        for i_compositions in td_compositions:
            a = i_compositions.find_all('a')            # а - ссылки на исполнителя и песню  
            artist = a[0].text                          # имя исполнителя
            composition = a[1].text                     # название композиции
            link = a[1].get('href')                     # ссылка на текст 
            compositions.append(Composition(link=link, artist=artist, title=composition))
            
        logger.success(f'compositions: {len(compositions)}')
        
        return compositions
    logger.warning(f'response status != 200')    
    
        
if __name__ == '__main__':
    res = find_conposition('Мне насрать на мое лицо')
    if res is None:
        raise SystemExit()
    logger.debug('compositions:')
    for i in res:
        print(f'\t{i.artist} - {i.title}({i.link})')