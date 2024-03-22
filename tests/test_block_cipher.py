from loguru import logger

from ciphers.block.gost_34_13_2015 import GOST_34_13_2015_GammaOutputFeedback


def test_gost34132015ofb():
    init_vect: bytearray = bytearray(
        [
            0x12,
            0x34,
            0x56,
            0x78,
            0x90,
            0xAB,
            0xCE,
            0xF0,
            0xA1,
            0xB2,
            0xC3,
            0xD4,
            0xE5,
            0xF0,
            0x01,
            0x12,
            0x23,
            0x34,
            0x45,
            0x56,
            0x67,
            0x78,
            0x89,
            0x90,
            0x12,
            0x13,
            0x14,
            0x15,
            0x16,
            0x17,
            0x18,
            0x19,
        ]
    )

    # fmt: off
    key = bytearray([
        0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
        0xfe, 0xdc, 0xba, 0x98, 0x76, 0x54, 0x32, 0x10, 0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef,
    ])

    # fmt: on

    cipher_obj = GOST_34_13_2015_GammaOutputFeedback(key=key, init_vect=init_vect)

    plain_text = "Я в своем познании настолько преисполнился"
    encrypted_data = cipher_obj.encrypt(plain_text.encode("utf-8"))

    cipher_obj = GOST_34_13_2015_GammaOutputFeedback(key=key, init_vect=init_vect)
    decrypted_data = cipher_obj.decrypt(encrypted_data)
    decrypted_text = decrypted_data.decode("utf-8", errors="ignore")

    logger.info(f"plain_text: {plain_text}")
    logger.info(f"encrypted_data: {encrypted_data}")
    logger.info(f"decrypted_data: {decrypted_data}")
    logger.info(f"decrypted_text: {decrypted_text}")
    assert plain_text == decrypted_text
