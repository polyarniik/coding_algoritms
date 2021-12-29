from abc import ABC, abstractmethod


class BaseCoderDecoder(ABC):
    @abstractmethod
    def decode(self):
        pass

    @abstractmethod
    def encode(self):
        pass
