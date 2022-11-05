import logging
import os
from flask import Flask, request, render_template, url_for, redirect
from config import Config
from torrent_downloader import TorrentDownloader
from werkzeug.utils import secure_filename


app = Flask(__name__, static_url_path='')
app.config.from_object('config.ServerConfig')
logger = logging
logger.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
torrent_downloader = TorrentDownloader(Config.SERVER_URL, Config.USER, Config.PASSWORD, Config.OUTPUT_PATH, logger)


@app.route('/', methods=["GET"])
def index():
    torrent_details_list = torrent_downloader.get_torrents_details("downloading")
    return render_template('table.html', title="Homepage", data=torrent_details_list, headers=list(torrent_details_list.keys()))


@app.route('/download_torrent', methods=["GET", 'POST'])
def download_torrent():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_path = os.path.join(app.config['UPLOAD_PATH'], filename)
            uploaded_file.save(file_path)
            logger.info(f"Uploaded {filename} to {app.config['UPLOAD_PATH']}")
            torrent_downloader.add_to_download_torrent_queue(file_path)
    return render_template('download_torrent.html', title="Download torrent")


if __name__ == '__main__':
    app.run("0.0.0.0", port=5001, debug=True)
