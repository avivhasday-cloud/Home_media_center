from assets.base_asset import BaseAsset


class Series(BaseAsset):

    def __init__(self,
                 _id: str = None,
                 name: str = None,
                 directory_path: str = None,
                 directory_size: str = None,
                 genres: [str] = None,
                 list_of_episodes: [str] = None):
        super(Series, self).__init__(_id, name, directory_path)
        self.list_of_episodes = list_of_episodes
        self.directory_size = directory_size
        self.genres = genres

    def get_directory_size(self):
        return self.directory_size

    def get_genres(self):
        return self.genres

    def get_list_of_episodes(self):
        return self.list_of_episodes

    def __repr__(self):
        return f"Series: {self.name}"

