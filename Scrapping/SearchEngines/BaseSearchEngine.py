from abc import abstractmethod


class BaseSearchEngine:
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url

    @abstractmethod
    def GetQueryParams(self) -> dict[str, str]:
        pass

