from assets.base_asset import BaseAsset


class Subtitles(BaseAsset):

    def __init__(self,
                 _id: str = None,
                 name: str = None,
                 directory_path: str = None,
                 movie_id: str = None):
        super(Subtitles, self).__init__(_id, name, directory_path)
        self.movie_id = movie_id

    def get_movie_id(self):
        return self.movie_id
