from loguru import logger

from src.replacement_method.algorithm import TrithemiusCipher


def test_trithemius_cipher():
    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    keyword = "идущий к реке"
    plaintext = (
        "Я в своем познании настолько преисполнился, что я как будто бы уже сто триллионов миллиардов"
        " лет проживаю на триллионах и триллионах таких же планет, как эта Земля, мне этот мир"
        " абсолютно понятен, и я здесь ищу только одного - покоя, умиротворения"
    )
    trithemius_cipher = TrithemiusCipher(alphabet=alphabet, keyword=keyword)
    encrypted_text = trithemius_cipher.encrypt(plaintext)
    decrypted_text = trithemius_cipher.decrypt(encrypted_text)
    logger.info(f"Origin Text:\n{plaintext}")
    logger.info(f"Encrypted Text:\n{encrypted_text}")
    logger.info(f"Decrypted Text:\n{decrypted_text}")
    assert plaintext.lower() == decrypted_text.lower()
