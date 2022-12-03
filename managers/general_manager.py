import logging
from queue import Queue
from threading import Thread
from typing import List
from utils.common import CommonUtils
from managers.torrents_manager import TorrentManager


class GeneralManager:

    def __init__(self, torrent_downloader_details: List[str], logger: logging):
        self.download_torrent_queue = Queue()
        self.finished_torrents_queue = Queue()
        self.populate_db_thread = Thread(target=self.run_populate_db_thread)
        self.logger = logger
        self.torrent_manager = TorrentManager(self.download_torrent_queue, self.finished_torrents_queue, torrent_downloader_details, self.logger)

    def add_to_download_queue(self, item: dict):
        return self.torrent_manager.add_to_download_queue(item)

    def run(self):
        CommonUtils.run_threads([self.populate_db_thread])
        self.logger.info("Populate db thread is running")
        self.torrent_manager.run()

    def handle_torrent(self, torrent_details: dict, operation: str) -> bool:
        if operation == "pause":
            return_val = self.torrent_manager.pause_torrent(torrent_details)
        elif operation == "resume":
            return_val = self.torrent_manager.resume_torrent(torrent_details)
        elif operation == "remove":
            return_val = self.torrent_manager.remove_torrent(torrent_details)
        else:
            self.logger.error(f"Operation: {operation} isnt a valid operation to run on torrent")
            return_val = False
        return return_val

    def get_torrents_details(self, filter_keyword: str = None) -> List[dict]:
        return self.torrent_manager.get_torrent_details(filter_keyword)

    def run_populate_db_thread(self):
        while True:
            try:
                torrent = self.finished_torrents_queue.get(timeout=20)
                if torrent:
                    print(torrent)
                    break
            except Exception:
                continue