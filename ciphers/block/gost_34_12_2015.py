import json
from typing import List

from loguru import logger

from ciphers.block.const import (
    _BLOCK_SIZE_KUZNECHIK,
    _KEY_SIZE,
    _GF,
    _S_BOX_KUZNECHIK,
    _S_BOX_REVERSE_KUZNECHIK,
)
from ciphers.block.utils import add_xor
from ciphers.block.utils import zero_fill


class GOST_34_12_2015_Kuznechik:
    """
    ГОСТ Р 34.12-2015 КРИПТОГРАФИЧЕСКАЯ ЗАЩИТА ИНФОРМАЦИИ. Блочные шифры

    Алгоритм блочного шифрования с длиной блока n = 128 бит «Кузнечик»
    """

    def __init__(self, key: bytearray):
        # Initialize cipher_c and cipher_iter_key
        self._cipher_c: List[bytearray] = []
        self._cipher_iter_key = []
        self._cipher_get_c()

        # Split key into two halves
        key_1 = key[: _KEY_SIZE // 2]
        key_2 = key[_KEY_SIZE // 2:]

        # Generate iterative keys
        internal = bytearray(_KEY_SIZE // 2)
        self._cipher_iter_key.append(key_1)
        self._cipher_iter_key.append(key_2)

        for i in range(4):
            for j in range(8):
                internal = add_xor(key_1, self._cipher_c[i * 8 + j])
                internal = GOST_34_12_2015_Kuznechik._cipher_s(internal)
                internal = GOST_34_12_2015_Kuznechik._cipher_l(internal)
                key_1, key_2 = [add_xor(internal, key_2), key_1]

            self._cipher_iter_key.append(key_1)
            self._cipher_iter_key.append(key_2)

        logger.warning(
            f"{self.__class__.__name__}\n{json.dumps(dict(key_size=_KEY_SIZE, key=key, key_1=key_1, key_2=key_2, internal=internal), indent=2, default=str)}"
        )

        # Clear keys for security reasons
        key_1 = bytearray(self.key_size // 2)
        key_2 = bytearray(self.key_size // 2)
        key = bytearray(self.key_size)

        logger.debug(
            f"{self.__class__.__name__}\n{json.dumps(self.__dict__, indent=2, default=str)}"
        )

    def __del__(self) -> None:
        """
        Delete the ciphering object.

        When deleting an instance of a class, it clears the values of
        iterative keys.
        """
        self.clear()

    @staticmethod
    def _cipher_s(data: bytearray) -> bytearray:
        result = bytearray(_BLOCK_SIZE_KUZNECHIK)
        for i in range(_BLOCK_SIZE_KUZNECHIK):
            result[i] = _S_BOX_KUZNECHIK[data[i]]
        return result

    @staticmethod
    def _cipher_s_reverse(data: bytearray) -> bytearray:
        result = bytearray(_BLOCK_SIZE_KUZNECHIK)
        for i in range(_BLOCK_SIZE_KUZNECHIK):
            result[i] = _S_BOX_REVERSE_KUZNECHIK[data[i]]
        return result

    @staticmethod
    def _cipher_r(data: bytearray) -> bytearray:
        a_0 = 0
        result = bytearray(_BLOCK_SIZE_KUZNECHIK)
        for i in range(_BLOCK_SIZE_KUZNECHIK):
            result[i] = data[i - 1]
            a_0 = a_0 ^ _GF[i][result[i]]
        result[0] = a_0
        return result

    @staticmethod
    def _cipher_r_reverse(data: bytearray) -> bytearray:
        a_15 = 0
        result = bytearray(_BLOCK_SIZE_KUZNECHIK)
        for i in range(_BLOCK_SIZE_KUZNECHIK - 1, -1, -1):
            result[i - 1] = data[i]
            a_15 = a_15 ^ _GF[i][data[i]]
        result[15] = a_15
        return result

    @staticmethod
    def _cipher_l(data: bytearray) -> bytearray:
        result = bytearray(_BLOCK_SIZE_KUZNECHIK)
        result = data
        for _ in range(16):
            result = GOST_34_12_2015_Kuznechik._cipher_r(result)
        return result

    @staticmethod
    def _cipher_l_reverse(data: bytearray) -> bytearray:
        result = bytearray(_BLOCK_SIZE_KUZNECHIK)
        result = data
        for _ in range(16):
            result = GOST_34_12_2015_Kuznechik._cipher_r_reverse(result)
        return result

    def _cipher_get_c(self) -> None:
        for i in range(1, 33):
            internal = bytearray(_BLOCK_SIZE_KUZNECHIK)
            internal[15] = i
            self._cipher_c.append(GOST_34_12_2015_Kuznechik._cipher_l(internal))

    @property
    def block_size(self) -> int:
        """
        Return the value of the internal block size of the cipher algorithm.

        For the 'kuznechik' algorithm this value is 16 and the 'magma'
        algorithm, this value is 8.
        """
        return _BLOCK_SIZE_KUZNECHIK

    @property
    def key_size(self) -> int:
        """
        Return the value of the cipher key size.

        For the 'magma' and 'kuznechik' algorithms, the key size is 32 bytes
        (256 bits).
        """
        return _KEY_SIZE

    def decrypt(self, block: bytearray) -> bytearray:
        """
        Decrypting a block of ciphertext.

        Args:
            block: The block of ciphertext to be decrypted (the block size is
              16 bytes).

        Returns:
            The block of plaintext.
        """
        block = bytearray(block)
        block = add_xor(self._cipher_iter_key[9], block)
        for i in range(8, -1, -1):
            block = GOST_34_12_2015_Kuznechik._cipher_l_reverse(block)
            block = GOST_34_12_2015_Kuznechik._cipher_s_reverse(block)
            block = add_xor(self._cipher_iter_key[i], block)
        return block

    def encrypt(self, block: bytearray) -> bytearray:
        """
        Encrypting a block of plaintext.

        Args:
            block: The block of plaintext to be encrypted (the block size is
              16 bytes).

        Returns:
            The block of ciphertext.
        """
        block = bytearray(block)
        logger.debug(
            f"{self.__class__.__name__}\n{json.dumps(dict(block_before=block), indent=2, default=str)}"
        )
        for i in range(9):
            block = add_xor(self._cipher_iter_key[i], block)
            block = GOST_34_12_2015_Kuznechik._cipher_s(block)
            block = GOST_34_12_2015_Kuznechik._cipher_l(block)
            block = add_xor(self._cipher_iter_key[9], block)
        logger.debug(
            f"{self.__class__.__name__}\n{json.dumps(dict(block_after=block), indent=2, default=str)}"
        )
        return block

    def clear(self) -> None:
        """Сlearing the values of iterative encryption keys."""
        for i in range(10):
            self._cipher_iter_key[i] = zero_fill(self._cipher_iter_key[i])
