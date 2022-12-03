import time
from queue import Queue
from threading import Thread
from typing import List

from torrent_downloader import TorrentDownloader
from utils.common import CommonUtils


class TorrentManager:

    def __init__(self, download_torrent_queue: Queue, finished_torrents_queue: Queue, torrent_downloader_details: List[str], logger):
        self.download_torrent_queue = download_torrent_queue
        self.finished_torrents_queue = finished_torrents_queue
        self.finished_torrents_thread = Thread(target=self.run_finished_torrents_thread)
        self.download_torrent_thread = Thread(target=self.run_download_thread)
        self.torrent_downloader = TorrentDownloader(*torrent_downloader_details, logger=logger)
        self.logger = logger

    def add_to_download_queue(self, item: dict):
        return CommonUtils.add_to_queue(self.download_torrent_queue, item)

    def pause_torrent(self, torrent_details: dict) -> bool:
        return self.torrent_downloader.pause_downloading_torrent(torrent_details)

    def resume_torrent(self, torrent_details: dict) -> bool:
        return self.torrent_downloader.resume_downloading_torrent(torrent_details)

    def remove_torrent(self, torrent_details: dict) -> bool:
        return self.torrent_downloader.remove_torrent_and_its_contents(torrent_details)

    def get_torrent_details(self, filter_keyword: str = None) -> List[dict]:
        return self.torrent_downloader.get_torrents_details(filter_keyword)

    def run(self):
        CommonUtils.run_threads([self.finished_torrents_thread, self.download_torrent_thread])
        self.logger.info("download_torrent_thread is running")
        self.logger.info("finished_torrents_thread is running")

    def run_download_thread(self):
        while True:
            try:
                torrent_dict = self.download_torrent_queue.get(timeout=20)
            except Exception:
                continue
            if torrent_dict:
                torrent_name = torrent_dict['name']
                self.logger.info(f"Getting torrent : {torrent_name} from Queue")
                self.logger.info(f"Number of torrents in queue: {len(self.download_torrent_queue.queue)}")
                self.torrent_downloader.download_torrent_from_magnet_link(torrent_dict)

    def run_finished_torrents_thread(self):
        while True:
            torrents = self.torrent_downloader.get_filtered_torrents("completed")
            if len(torrents) > 0:
                for torrent in torrents:
                    try:
                        CommonUtils.add_to_queue(self.finished_torrents_queue, torrent)
                    except Exception:
                        self.logger.error(f"Failed to Add {torrent['name']} to finished torrents queue")
            else:
                self.logger.info("There is no finished torrents at the moment, waiting 5 mins")
                time.sleep(60 * 5)
