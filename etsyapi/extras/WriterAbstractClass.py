from abc import ABC, abstractmethod

class WriterAbstractClass(ABC):

    def __init__(self, fp):
        self.fpointer = p
        super.__init__()

    @abstractmethod
    def write_headers(self, headers):
        pass

    @abstractmethod
    def write_row(self, row_data):
        pass

