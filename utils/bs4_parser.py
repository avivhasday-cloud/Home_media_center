from bs4 import BeautifulSoup
from utils.common import Fields


class BS4Parser:

    HTML_PARSER = "html.parser"

    @staticmethod
    def parse_table_content_to_dict(html_page_text: str) -> [dict]:
        soup = BeautifulSoup(html_page_text, BS4Parser.HTML_PARSER)
        table = soup.find("table", {"class": "tablelist2"})
        rows = table.findAll("tr", {"class": "table2ta"})
        table_content_list = list()
        for row in rows:
            row_list = list()
            cells = row.findAll("td", "tlista")
            for cell in cells[1::]:
                for item in cell.contents:
                    if item in ['\n', '', ' '] or item.name == "span":
                        continue
                    elif item.name == "a":
                        row_list.extend([value for value in item.attrs.values()])
                    else:
                        row_list.append(item.text)

            row_list.append("")
            row_dict = dict(zip(Fields.BROWSE_TORRENTS_HEADERS, row_list))
            table_content_list.append(row_dict)
        return table_content_list

    @staticmethod
    def extract_magnet_link_from_movie_page(row_dict: dict, movie_page_content: str):
        soup = BeautifulSoup(movie_page_content, BS4Parser.HTML_PARSER)
        table = soup.find("table", {"class": "tlista"})
        download_row = table.findAll("tr")[0]
        cell = download_row.find("td", {"class": "tlista"})
        a_tag = cell.findAll("a")[-1]
        row_dict["torrent_magnet_link"] = a_tag.attrs["href"]
