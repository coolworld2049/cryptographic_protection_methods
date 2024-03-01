from abc import ABC, abstractmethod


class AbstractCipher(ABC):

    @abstractmethod
    def encrypt(self, text):
        pass

    @abstractmethod
    def decrypt(self, text):
        pass
