from assets.movie import Movie


class Series(Movie):

    def __init__(self,
                 _id: str = None,
                 name: str = None,
                 directory_path: str = None,
                 subtitles: [str] = None,
                 directory_size: str = None,
                 genres: [str] = None,
                 list_of_episodes: [str] = None):
        super(Series, self).__init__(_id, name, directory_path, subtitles, directory_size, genres)
        self.list_of_episodes = list_of_episodes

    def get_list_of_episodes(self):
        return self.list_of_episodes

