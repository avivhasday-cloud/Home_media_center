import os.path


class BaseAsset:

    def __init__(self, _id: str = None, name: str = None, directory_path: str = None):
        self._id = _id
        self.name = name
        self.directory_path = directory_path

    def get_id(self) -> str:
        return self._id

    def get_name(self) -> str:
        return self.name

    def get_directory_path(self) -> str:
        return self.directory_path

    def get_asset_full_path(self) -> str:
        return os.path.join(self.get_directory_path(), self.get_name())

    def to_dict(self) -> dict:
        return {key: value for key, value in self.__dict__.items()}

    def __repr__(self):
        return f"BaseAsset: {self.name}"
