from requests import get
from loguru import logger
from bs4 import BeautifulSoup
from composition import Composition


@logger.catch
def get_composition(composition: Composition) -> str | None:
    res = get(composition.link)
    html = BeautifulSoup(res.text, 'html.parser')
    logger.success(f'{composition.title} - text received')
    return html.pre.text


if __name__ == '__main__':
    from find_composition import find_conposition
    compositions = find_conposition('Мне насрать на мое лицо')
    print(get_composition(compositions[0]))
