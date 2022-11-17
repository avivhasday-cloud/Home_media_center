import requests
from utils.bs4_parser import BS4Parser


class TorrentSiteAPI:

    BASE_URL = "https://www.rarbggo.to"
    SEARCH_ENDPOINT = "search/?search="
    GET_MOVIE_QUERY_PARAMS = "category=movies&order=leechers&by=DESC"

    @staticmethod
    def get_search_query_content(search_keyword: str) -> [dict]:
        url = f"{TorrentSiteAPI.BASE_URL}/{TorrentSiteAPI.SEARCH_ENDPOINT}{search_keyword}&{TorrentSiteAPI.GET_MOVIE_QUERY_PARAMS}"
        res = requests.get(url)
        table_content = BS4Parser.parse_table_content_to_dict(res.text)
        for item in table_content:
            movie_page = TorrentSiteAPI._get_movie_page_content(item["movie_link"])
            BS4Parser.extract_magnet_link_from_movie_page(item, movie_page)
            del item["movie_link"]
        return table_content

    @staticmethod
    def _get_movie_page_content(endpoint: str):
        url = f"{TorrentSiteAPI.BASE_URL}/{endpoint}"
        res = requests.get(url)
        return res.text


