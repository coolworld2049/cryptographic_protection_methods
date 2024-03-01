from src.cipher.transposition.algorithm import TranspositionCipher


def test_encrypt_decrypt():
    original_text = "пусть будет так, как мы хотели"

    transposition_cipher = TranspositionCipher()
    encrypted_text = transposition_cipher.encrypt(original_text)
    assert transposition_cipher.prepare_text(
        encrypted_text
    ) != transposition_cipher.prepare_text(original_text)

    decrypted_text = transposition_cipher.decrypt(encrypted_text)
    assert transposition_cipher.prepare_text(
        decrypted_text
    ) == transposition_cipher.prepare_text(original_text)
