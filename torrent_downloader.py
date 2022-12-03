import logging
from qbittorrent import Client
from utils.common import Fields


class TorrentDownloader:

    def __init__(self, server_url: str, user: str, password: str, output_dir: str, logger: logging = None):
        self.torrent_client = Client(server_url)
        self.output_dir = output_dir
        self.user = user
        self.password = password
        self.logger = logger
        self.torrent_client.login(self.user, self.password)

    @staticmethod
    def get_size_format(b, factor: int = 1024, suffix: str = "B") -> str:
        """
        Scale bytes to its proper byte format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
            if b < factor:
                return f"{b:.2f}{unit}{suffix}"
            b /= factor
        return f"{b:.2f}Y{suffix}"

    def download_torrent_from_magnet_link(self, torrent_dict: dict):
        self.run_operation_on_torrent(torrent_dict['name'], "start downloading",
                                      lambda: self.torrent_client.download_from_link(torrent_dict["torrent_magnet_link"], save_path=self.output_dir))

    def resume_downloading_torrent(self, torrent: dict) -> bool:
        return self.run_operation_on_torrent(torrent["name"], "resume", lambda: self.torrent_client.resume(torrent["hash"]))

    def pause_downloading_torrent(self, torrent: dict) -> bool:
        return self.run_operation_on_torrent(torrent["name"], "pause", lambda: self.torrent_client.pause(torrent["hash"]))

    def remove_torrent_and_its_contents(self, torrent: dict) -> bool:
        return self.run_operation_on_torrent(torrent["name"], "remove", lambda: self.torrent_client.delete_permanently(torrent["hash"]))

    def run_operation_on_torrent(self, name: str, operation_name: str, func):
        try:
            func()
            return_value = True
        except Exception as e:
            self.logger.error(f"Failed to {operation_name} torrent {name}")
            self.logger.error(e)
            return_value = False
        return return_value

    def get_torrents_details(self, filter_keyword: str = None) -> [dict]:
        torrents = self.get_filtered_torrents(filter_keyword)
        torrent_details_list = list()
        for torrent in torrents:
            torrent_details = {key: None for key in Fields.TORRENT_DETAILS_HEADERS}
            torrent_details.update({
                "name": torrent['name'],
                "hash": torrent['hash'],
                "num_of_seeds": torrent['num_seeds'],
                "file_path": torrent["content_path"],
                "file_size": self.get_size_format(torrent['total_size']),
                "download_speed": self.get_size_format(torrent['dlspeed']),
                "state": torrent["state"]
            })
            torrent_details_list.append(torrent_details)
        return torrent_details_list

    def get_filtered_torrents(self, keyword: str = None):
        return self.torrent_client.torrents(filter=keyword)

