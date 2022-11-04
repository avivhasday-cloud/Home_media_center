import logging
import os.path
from queue import Queue
from qbittorrent import Client
from threading import Thread


class TorrentDownloader:
    def __init__(self, server_url: str, user: str, password: str, output_dir: str, logger: logging = None):
        self.torrent_client = Client(server_url)
        self.torrent_client.login(user, password)
        self.output_dir = output_dir
        self.logger = logger
        self.download_torrent_queue = Queue()
        self.download_torrent_thread = Thread(target=self.download_torrent_from_magnet_link)
        self.download_torrent_thread.start()

    def add_to_download_torrent_queue(self, torrent_dict: dict):
        try:
            self.download_torrent_queue.put(torrent_dict)
            self.logger.info(f"Added {torrent_dict['name']} to download torrent queue")
        except Exception as e:
            self.logger.error(f"Failed to Add {torrent_dict['name']} to download torrent queue")
            self.logger.error(e)


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

    def download_torrent_from_magnet_link(self):
        while True:
            try:
                torrent_dict = self.download_torrent_queue.get(timeout=20)
                torrent_name = torrent_dict['name']
                self.logger.info(f"Getting torrent : {torrent_name} from Queue")
                self.logger.info(f"Number of torrents in queue: {len(self.download_torrent_queue.queue)}")
            except Exception:
                continue
            try:
                torrent_dir = os.path.join(self.output_dir, torrent_name)
                self.torrent_client.download_from_link(torrent_dict["torrent_magnet_link"], save_path=torrent_dir)
            except Exception as e:
                self.logger.error(f"Failed to start download torrent {torrent_name}")
                self.logger.error(e)



    def get_torrents_details(self, filter_keyword: str) -> [dict]:
        torrents = self.torrent_client.torrents(filter=filter_keyword)
        torrent_details_list = list()
        for torrent in torrents:
            torrent_details = {
                "torrent_name": torrent['name'],
                "hash": torrent['hash'],
                "num_of_seeds": torrent['num_seeds'],
                "file_size":self.get_size_format(torrent['total_size']),
                "download_speed": self.get_size_format(torrent['dlspeed'])
            }
            torrent_details_list.append(torrent_details)
        return torrent_details_list

    def wait_for_thread_to_finish(self):
        self.download_torrent_thread.join()
        self.logger.info(f"Download torrent thread has finished")
