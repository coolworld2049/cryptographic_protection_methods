from cipher.abc import AbstractCipher


class TranspositionCipher(AbstractCipher):
    """Mirroring cipher"""

    def __init__(self, mirror_char='О'):
        self.mirror_char = mirror_char

    def pad_text(self, text):
        # Pad the text with the mirror character to make its length a multiple of 5
        padding_size = (5 - len(text) % 5) % 5
        padded_text = text + self.mirror_char * padding_size
        return padded_text

    def encrypt(self, plaintext):
        # Pad the plaintext
        padded_plaintext = self.pad_text(plaintext.upper())

        # Apply mirror permutation
        cipher_text = ''
        for i in range(0, len(padded_plaintext), 5):
            block = padded_plaintext[i:i + 5]
            cipher_text += block[::-1]

        return cipher_text

    def decrypt(self, cipher_text):
        # Apply reverse mirror permutation
        decrypted_text = ''
        for i in range(0, len(cipher_text), 5):
            block = cipher_text[i:i + 5]
            decrypted_text += block[::-1]

        return decrypted_text.rstrip(self.mirror_char)


plaintext = "ПУСТЬ БУДЕТ ТАК, КАК МЫ ХОТЕЛИ"
mirror_cipher = TranspositionCipher()
cipher_text = mirror_cipher.encrypt(plaintext)
print("Encrypted:", cipher_text)

decrypted_text = mirror_cipher.decrypt(cipher_text)
print("Decrypted:", decrypted_text)
