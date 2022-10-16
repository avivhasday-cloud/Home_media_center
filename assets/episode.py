from assets.base_asset import BaseAsset


class Episode(BaseAsset):

    def __init__(self,
                 _id: str = None,
                 name: str = None,
                 directory_path: str = None,
                 series_id: str = None):
        super(Episode, self).__init__(_id, name, directory_path)
        self.series_id = series_id

    def get_series_id(self):
        return self.series_id
