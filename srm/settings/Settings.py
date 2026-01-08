import configparser
import os

from srm.exceptions.SettingsException import SettingsException


class Settings:
    def __init__(self, file_path: str):
        if not os.path.exists(file_path):
            raise SettingsException(f"Settings file not found: {file_path}")

        self.file_path = file_path
        self._config = configparser.ConfigParser()

        self._config.read(self.file_path)
        self._base_dir = os.path.dirname(os.path.dirname(self.file_path))

    @property
    def repository(self) -> str:
        return self._config["SETTINGS"].get("repository", "in_memory")

    @property
    def students_path(self) -> str:
        return self._config["SETTINGS"].get("students_path")

    @property
    def grades_path(self) -> str:
        return self._config["SETTINGS"].get("grades_path")

    @property
    def disciplines_path(self) -> str:
        return self._config["SETTINGS"].get("disciplines_path")





