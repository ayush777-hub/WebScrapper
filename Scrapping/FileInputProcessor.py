from InputProcessor import InputProcessor
from Models.FileInput import FileInput
from Models.Input import Input

class FileInputProcessor(InputProcessor):
    def ProcessInput(self, input: Input) -> list[str]:
        if not isinstance(input, FileInput):
            raise TypeError("Expected input of type FileInput")
        
        file_input: FileInput = input  # type cast for type hinting
        data = file_input.get_data()
        return data.splitlines()