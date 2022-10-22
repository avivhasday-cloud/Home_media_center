from assets.base_asset import BaseAsset


class Episode(BaseAsset):

    def __init__(self,
                 _id: str = None,
                 name: str = None,
                 directory_path: str = None,
                 subtitles: [str] = None,
                 series_id: str = None):
        super(Episode, self).__init__(_id, name, directory_path)
        self.subtitles = subtitles
        self.series_id = series_id

    def get_subtitles(self):
        return self.subtitles

    def get_series_id(self):
        return self.series_id
