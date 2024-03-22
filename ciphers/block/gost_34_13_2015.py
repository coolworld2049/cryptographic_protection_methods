from abc import ABC, abstractmethod

from loguru import logger

from ciphers.block.const import _DEFAULT_IV_KUZNECHIK
from ciphers.block.gost_34_12_2015 import GOST34122015Kuznechik
from utils import add_xor
from utils import check_value
from utils import zero_fill

_KEY_SIZE: int = 32


class GOST34132015(ABC):
    def __init__(self, key: bytearray) -> None:
        if not check_value(key, _KEY_SIZE):
            key = zero_fill(key)
            raise GOSTCipherError("GOSTCipherError: invalid key value")
        self._cipher_obj = GOST34122015Kuznechik(key)

    def __del__(self) -> None:
        self.clear()

    def _get_num_block(self, data: bytearray) -> int:
        return len(data) // self.block_size

    def _get_block(self, data: bytearray, count_block: int) -> bytearray:
        begin_block = self.block_size * count_block
        end_block = self.block_size + (self.block_size * count_block)
        return data[begin_block:end_block]

    def clear(self) -> None:
        """Сlearing the values of iterative encryption keys."""
        if hasattr(self, "_cipher_obj"):
            self._cipher_obj.clear()

    @property
    def block_size(self) -> int:
        """
        Return the value of the internal block size of the cipher algorithm.

        For the 'kuznechik' algorithm this value is 16 and the 'magma'
        algorithm, this value is 8.
        """
        return self._cipher_obj.block_size


class GOST34132015Cipher(GOST34132015, ABC):

    @abstractmethod
    def encrypt(self, data: bytearray) -> bytearray:
        if not isinstance(data, (bytes, bytearray)):
            self.clear()
            raise GOSTCipherError("GOSTCipherError: invalid plaintext data")
        return data

    @abstractmethod
    def decrypt(self, data: bytearray) -> bytearray:
        if not isinstance(data, (bytes, bytearray)):
            self.clear()
            raise GOSTCipherError("GOSTCipherError: invalid ciphertext data")
        return data


class GOST34132015CipherFeedBack(GOST34132015Cipher, ABC):

    def __init__(self, key: bytearray, init_vect: bytearray) -> None:
        GOST34132015Cipher.__init__(self, key)
        check_init_vect = isinstance(init_vect, (bytes, bytearray))
        if (not check_init_vect) or (len(init_vect) % self.block_size) != 0:
            self.clear()
            raise GOSTCipherError(
                "GOSTCipherError: invalid initialization vector value"
            )
        self._init_vect = init_vect
        self._init_vect = bytearray(self._init_vect)

    def _get_gamma(self) -> bytearray:
        return self._cipher_obj.encrypt(self._init_vect[0: self.block_size])

    def _set_init_vect(self, data: bytearray):
        iter_iv_hi = self._init_vect[self.block_size: len(self._init_vect)]
        self._init_vect[0: len(self._init_vect) - self.block_size] = iter_iv_hi
        begin_iv_low = len(self._init_vect) - self.block_size
        end_iv_low = len(self._init_vect)
        self._init_vect[begin_iv_low:end_iv_low] = data

    def _get_final_block(self, data):
        return data[self.block_size * self._get_num_block(data)::]

    def _final_cipher(self, data):
        gamma = self._get_gamma()
        cipher_block = self._get_final_block(data)
        return add_xor(gamma, cipher_block)

    @abstractmethod
    def encrypt(self, data: bytearray) -> bytearray:
        data = GOST34132015Cipher.encrypt(self, data)
        return data

    @abstractmethod
    def decrypt(self, data: bytearray) -> bytearray:
        data = GOST34132015Cipher.decrypt(self, data)
        return data

    @property
    def iv(self) -> bytearray:
        """Return the value of the initializing vector."""
        return self._init_vect[len(self._init_vect) - self.block_size::]


class GOST34132015ofb(GOST34132015CipherFeedBack):
    def encrypt(self, data: bytearray) -> bytearray:
        result = bytearray()
        gamma = bytearray()
        data = super().encrypt(data)
        for i in range(self._get_num_block(data)):
            gamma = self._get_gamma()
            cipher_block = self._get_block(data, i)
            result = result + add_xor(gamma, cipher_block)
            self._set_init_vect(gamma[0: self.block_size])
        if len(data) % self.block_size != 0:
            result = result + self._final_cipher(data)
        return result

    def decrypt(self, data: bytearray) -> bytearray:
        super().decrypt(data)
        return self.encrypt(data)


class GOSTCipherError(Exception):
    pass


if __name__ == "__main__":
    # fmt: off
    key = bytearray([
        0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
        0xfe, 0xdc, 0xba, 0x98, 0x76, 0x54, 0x32, 0x10, 0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef,
    ])

    # fmt: on

    cipher_obj = GOST34132015ofb(key=key, init_vect=_DEFAULT_IV_KUZNECHIK)

    plain_text = (
        "Я в своем познании настолько преисполнился, что я как будто бы уже сто триллионов миллиардов"
        " лет проживаю на триллионах и триллионах таких же планет, как эта Земля, мне этот мир"
        " абсолютно понятен, и я здесь ищу только одного - покоя, умиротворения"
    )
    encrypted_data = cipher_obj.encrypt(plain_text.encode("utf-8"))

    cipher_obj = GOST34132015ofb(key=key, init_vect=_DEFAULT_IV_KUZNECHIK)
    decrypted_data = cipher_obj.decrypt(encrypted_data)
    decrypted_text = decrypted_data.decode('utf-8', errors='ignore')

    logger.info(f"plain_text: {plain_text}")
    logger.info(f"encrypted_data: {encrypted_data}")
    logger.info(f"decrypted_text: {decrypted_text}")
    assert plain_text == decrypted_text
