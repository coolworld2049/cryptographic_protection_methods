import sys
from typing import Literal

import pytest
from loguru import logger

from src.cipher.substitution.algorithm import TrisemusSubstitutionCipher

logger.remove()
logger.add(sys.stderr, level="INFO")

TEXT = {
    "ru": (
        "Я в своем познании настолько преисполнился, что я как будто бы уже сто триллионов миллиардов"
        " лет проживаю на триллионах и триллионах таких же планет, как эта Земля, мне этот мир"
        " абсолютно понятен, и я здесь ищу только одного - покоя, умиротворения"
    ),
    "en": (
        "I have become so complete in my knowledge that I seem to already be a hundred trillion billion."
        "I’ve been living for years on trillions and trillions of planets just like this Earth, this is the world for me"
        "absolutely understandable, and I’m looking for only one thing here - peace, tranquility"
    ),
}


@pytest.mark.parametrize("lang,keyword", [("ru", "ключ"), ("en", "key")])
def test_encrypt_decrypt(lang: Literal["ru", "en"], keyword: str):
    plaintext = TEXT[lang]
    trisemus_cipher = TrisemusSubstitutionCipher(lang=lang, keyword=keyword)
    encrypted_text = trisemus_cipher.encrypt(plaintext)
    decrypted_text = trisemus_cipher.decrypt(encrypted_text)
    logger.info(trisemus_cipher)
    logger.info(f"Origin Text:\n\n{plaintext}\n")
    logger.info(f"Encrypted Text:\n\n{encrypted_text}\n")
    logger.info(f"Decrypted Text:\n\n{decrypted_text}\n")
    assert plaintext.lower() == decrypted_text.lower()
