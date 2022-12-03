from queue import Queue
from threading import Thread


class Fields:
    BROWSE_TORRENTS_HEADERS = ["movie_link", "name", "category", "secondary_category", "uploaded_date", "size", "seeders", "leechers", "uploader", "torrent_magnet_link"]
    TORRENT_DETAILS_HEADERS = ['name', 'hash', 'num_of_seeds', 'file_path', 'file_size', 'download_speed', 'state']


class CommonUtils:

    @staticmethod
    def run_threads(threads: [Thread]):
        for thread in threads:
            thread.start()

    @staticmethod
    def add_to_queue(_queue: Queue, item: dict):
        try:
            _queue.put(item)
            return_val = True
        except Exception as e:
            return_val = False
        return return_val