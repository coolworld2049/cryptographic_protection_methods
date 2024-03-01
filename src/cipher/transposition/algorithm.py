import string
from typing import Literal


class TranspositionCipher:
    def __init__(self, block_size: int = 5, padding_str: str = "о"):
        self.__block_size = block_size
        self.__padding_str = padding_str

    @staticmethod
    def prepare_text(text: str):
        result = (
            text.lower()
            .replace(" ", "")
            .translate(str.maketrans("", "", string.punctuation))
        )
        return result

    def __pad_text(self, text: str):
        remainder = len(text) % self.__block_size
        if remainder != 0:
            text += self.__padding_str * (self.__block_size - remainder)
        return text

    def __apply_transposition(self, text, action: Literal["encrypt", "decrypt"]):
        text = self.prepare_text(text)
        text = self.__pad_text(text)
        result = []
        for i in range(0, len(text), self.__block_size):
            block = text[i : i + self.__block_size]
            result.insert(-i, block[::-1])
        result_text = " ".join(result)
        return result_text

    def encrypt(self, plaintext):
        return self.__apply_transposition(plaintext, action="encrypt")

    def decrypt(self, ciphertext):
        plaintext = self.__apply_transposition(ciphertext, action="decrypt")
        plaintext = plaintext.rstrip(self.__padding_str)
        return plaintext


transposition_cipher = TranspositionCipher()

original_text = "пусть будет так, как мы хотели"
encrypted_text = transposition_cipher.encrypt(original_text)
decrypted_text = transposition_cipher.decrypt(encrypted_text)

print(f"Original Text: {original_text}")
print(f"Encrypted Text: {encrypted_text}")
print(f"Decrypted Text: {decrypted_text}")
