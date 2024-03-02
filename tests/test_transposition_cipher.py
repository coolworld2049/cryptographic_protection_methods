from loguru import logger

from ciphers.transposition.algorithm import TranspositionCipher


def test_encrypt_decrypt():
    original_text = "пусть будет так, как мы хотели"
    logger.debug(f"Original Text: {original_text}")

    transposition_cipher = TranspositionCipher()
    encrypted_text = transposition_cipher.encrypt(original_text)
    logger.debug(f"Encrypted Text: {encrypted_text}")
    assert transposition_cipher.prepare_text(
        encrypted_text
    ) != transposition_cipher.prepare_text(original_text)

    decrypted_text = transposition_cipher.decrypt(encrypted_text)
    assert transposition_cipher.prepare_text(
        decrypted_text
    ) == transposition_cipher.prepare_text(original_text)
    logger.debug(f"Decrypted Text: {decrypted_text}")
