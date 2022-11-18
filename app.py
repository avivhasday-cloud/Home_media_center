import logging
import os
from flask import Flask, request, render_template, url_for, redirect
from config import Config
from torrent_downloader import TorrentDownloader
from utils.torrent_site_api import TorrentSiteAPI
from utils.bs4_parser import BS4Parser
from werkzeug.utils import secure_filename


app = Flask(__name__, static_url_path='')
app.config.from_object('config.ServerConfig')
logger = logging
logger.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
torrent_downloader = TorrentDownloader(Config.SERVER_URL, Config.USER, Config.PASSWORD, Config.OUTPUT_PATH, logger)


@app.route('/', methods=["GET"])
def index():
    torrent_details_list = torrent_downloader.get_torrents_details("downloading")
    return render_template('table.html', title="Homepage", headers=list(torrent_details_list[0].keys()), data=torrent_details_list)


@app.route("/browse_torrents", methods=["GET", "POST"])
def browse_torrents():
    headers = BS4Parser.TABLE_CELLS_KEYS[1::]
    torrents_table_list = None
    if request.method == 'POST':
        keyword_to_search = request.form.get("search", "")
        torrents_table_list = TorrentSiteAPI.get_search_query_content(keyword_to_search)
    return render_template('table.html', title="Homepage", headers=headers, data=torrents_table_list)


@app.route('/download_torrent/', methods=['POST'])
def download_torrent():
    torrent_data = request.form
    print(torrent_data)
    return render_template('download_torrent.html', title="Download torrent")


if __name__ == '__main__':
    app.run("0.0.0.0", port=5001, debug=True)
