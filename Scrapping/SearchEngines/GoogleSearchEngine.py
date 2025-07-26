import configparser
from SearchEngines.BaseSearchEngine import BaseSearchEngine

class GoogleSearchEngine(BaseSearchEngine):
    """A class representing the Google Search Engine."""
    def __init__(self, config_path="config.ini"):
        self._config = configparser.ConfigParser()
        self._config.read(config_path)
        name = self._config.get("Google", "name", fallback="Google")
        url = self._config.get("Google", "url")
        super().__init__(name, url)

    def GetQueryParams(self) -> dict[str, str]:
        return {
            'key': self._config.get("Google", "api_key"),
            'cx': self._config.get("Google", "search_engine_id"),
        }