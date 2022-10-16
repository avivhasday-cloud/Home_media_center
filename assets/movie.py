from assets.base_asset import BaseAsset


class Movie(BaseAsset):

    def __init__(self,
                 _id: str = None,
                 name: str = None,
                 directory_path: str = None,
                 subtitles: [str] = None,
                 directory_size: str = None,
                 genres: [str] = None):

        super(Movie, self).__init__(_id, name, directory_path)
        self.subtitles = subtitles
        self.directory_size = directory_size
        self.genres = genres

    def get_subtitles(self):
        return self.subtitles

    def get_directory_size(self):
        return self.directory_size

    def get_genres(self):
        return self.genres

    def __repr__(self):
        return f"Movie: {self.name}"
