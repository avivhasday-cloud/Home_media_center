from assets.base_asset import BaseAsset


class Subtitles(BaseAsset):

    def __init__(self,
                 _id: str = None,
                 name: str = None,
                 directory_path: str = None,
                 asset_id: str = None):
        super(Subtitles, self).__init__(_id, name, directory_path)
        self.asset_id = asset_id

    def get_asset_id(self):
        return self.asset_id
