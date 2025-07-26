from Models.Input import Input

class FileInput(Input):
    def __init__(self, file_path: str):
        super().__init__(dataSource=file_path)
        self.file_path = file_path

    def get_data(self) -> str:
        with open(self.file_path, 'r') as file:
            return file.read()