import logging
import os
from flask import Flask, request
from config import Config
from torrent_downloader import TorrentDownloader
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config.from_object('config.ServerConfig')
logger = logging
logger.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
torrent_downloader = TorrentDownloader(Config.SERVER_URL, Config.USER, Config.PASSWORD, Config.OUTPUT_PATH, logger)

@app.route('/download_torrent', methods=['POST'])
def download_torrent():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        uploaded_file.save(file_path)
        logger.info(f"Uploaded {filename} to {app.config['UPLOAD_PATH']}")
        torrent_downloader.add_to_download_torrent_queue(file_path)
        torrent_downloader.wait_for_thread_to_finish()




if __name__ == '__main__':
    app.run()