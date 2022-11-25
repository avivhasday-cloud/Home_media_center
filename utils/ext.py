import logging
from torrent_downloader import TorrentDownloader
import configurations


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
TORRENT_DOWNLOADER = TorrentDownloader(configurations.BaseConfig.SERVER_URL, configurations.BaseConfig.USER,
                                       configurations.BaseConfig.PASSWORD, configurations.BaseConfig.OUTPUT_PATH, LOGGER)