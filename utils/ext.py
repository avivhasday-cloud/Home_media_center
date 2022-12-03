import logging
from torrent_downloader import TorrentDownloader
import configurations


LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s')
# LOGGER.setLevel(logging.INFO)

TORRENT_DOWNLOADER = TorrentDownloader(configurations.BaseConfig.SERVER_URL, configurations.BaseConfig.USER,
                                       configurations.BaseConfig.PASSWORD, configurations.BaseConfig.TORRENTS_RELATIVE_OUTPUT_PATH, LOGGER)