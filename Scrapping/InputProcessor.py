from abc import abstractmethod
from Models.Input import Input


class InputProcessor:
    @abstractmethod
    def ProcessInput(self, input: Input) -> list[str]:
        pass
