import json
import os
import pathlib
import sys

from loguru import logger

from ciphers.block.const import _KEY_SIZE
from ciphers.block.gost_34_12_2015 import GOST_34_12_2015_Kuznechik
from ciphers.block.utils import add_xor
from ciphers.block.utils import check_value
from ciphers.block.utils import zero_fill

logger.remove()
if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
logger.add(sys.stdout)
log_path = pathlib.Path(__file__).parent.joinpath("log.log")
log_path.unlink(missing_ok=True)
logger.add(log_path)


class GOST_34_13_2015:
    """
    ГОСТ Р 34.13-2015 КРИПТОГРАФИЧЕСКАЯ ЗАЩИТА. Режимы работы блочных шифров
    """

    def __init__(self, key: bytearray) -> None:
        if not check_value(key, _KEY_SIZE):
            key_size = len(key)
            key = zero_fill(key)
            raise GOSTCipherError(
                f"GOSTCipherError: invalid key value. Your key size {key_size} != {_KEY_SIZE}"
            )
        self._cipher_obj = GOST_34_12_2015_Kuznechik(key)

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

    @property
    def key_size(self) -> int:
        """
        Return the value of the internal block size of the cipher algorithm.

        For the 'kuznechik' algorithm this value is 16 and the 'magma'
        algorithm, this value is 8.
        """
        return self._cipher_obj.key_size


class GOST_34_13_2015_GammaOutputFeedback(GOST_34_13_2015):

    def __init__(self, key: bytearray, init_vect: bytearray) -> None:
        super().__init__(key)
        check_init_vect = isinstance(init_vect, (bytes, bytearray))
        if (not check_init_vect) or (len(init_vect) % self.block_size) != 0:
            self.clear()
            raise GOSTCipherError(
                f"GOSTCipherError: invalid initialization vector value.\n"
                f"Condition: len(init_vect) % self.block_size != 0.\n"
                f"Result: {len(init_vect)} % {self.block_size} = {len(init_vect) % self.block_size}"
            )
        self._init_vect = init_vect
        self._init_vect = bytearray(self._init_vect)
        logger.debug(f"{self.__class__.__name__}\n{dict(_init_vect=self._init_vect)}")

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

    def encrypt(self, data: bytearray) -> bytearray:
        if not isinstance(data, (bytes, bytearray)):
            self.clear()
            raise GOSTCipherError("GOSTCipherError: invalid plaintext data")
        result = bytearray()
        gamma = bytearray()
        logger.debug(
            f"{self.__class__.__name__}\n number of blocks {self._get_num_block(data)}"
        )
        for i in range(self._get_num_block(data)):
            gamma = self._get_gamma()
            cipher_block = self._get_block(data, i)
            result += add_xor(gamma, cipher_block)
            self._set_init_vect(gamma[0: self.block_size])
            log_message = dict(gamma=gamma, cipher_block=cipher_block, result=result)
            logger.debug(
                f"{self.__class__.__name__}\n[block][{i}]\n{json.dumps(log_message, indent=2, default=str)}"
            )

        if len(data) % self.block_size != 0:
            result += self._final_cipher(data)
            logger.debug(
                f"{self.__class__.__name__}\n final cipher result\n{json.dumps(dict(result=result), indent=2, default=str)}"
            )
        return result

    def decrypt(self, data: bytearray) -> bytearray:
        if not isinstance(data, (bytes, bytearray)):
            self.clear()
            raise GOSTCipherError("GOSTCipherError: invalid ciphertext data")
        logger.debug(f"{self.__class__.__name__}\n[decrypt] >>>")
        return self.encrypt(data)

    @property
    def iv(self) -> bytearray:
        """Return the value of the initializing vector."""
        return self._init_vect[len(self._init_vect) - self.block_size::]


class GOSTCipherError(Exception):
    pass
