from abc import abstractmethod


class Input:
    def __init__(self, dataSource: str):
        self.dataSource = dataSource

    @abstractmethod
    def get_data(self) -> str:
        pass
