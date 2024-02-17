import string
from pprint import pprint


def generate_trisemus_table(keyword):
    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    keyword = keyword.lower().replace(" ", "")
    unique_keyword = "".join(sorted(set(keyword), key=keyword.index))
    remaining_chars = "".join(sorted(set(alphabet) - set(unique_keyword)))

    # same_chars = [['е', 'ё'], ['и', 'й'], ['ш', 'щ'], ['ь', 'ъ']]
    # for i, orig in enumerate(remaining_chars):
    #     for same_char in same_chars:
    #         if orig in same_char:
    #             for char_replacement in same_char:
    #                 remaining_chars = remaining_chars.replace(char_replacement, "")

    polybius_square_string = unique_keyword + remaining_chars + string.punctuation
    polybius_square = [
        list(polybius_square_string[i : i + 6])
        for i in range(0, len(polybius_square_string), 6)
    ]

    return polybius_square


def trisemus_encrypt(plaintext, table):
    plaintext = plaintext.lower()
    ciphertext = ""
    for char in plaintext:
        if char == " ":
            ciphertext += char
            continue
        for row in range(len(table)):
            if char in table[row]:
                col = table[row].index(char)
                replace_row = (row + 1) % len(table)
                cipher_value = table[replace_row][col]
                ciphertext += cipher_value
                print(
                    f"'{char}' -> '{cipher_value}'; row: {row}, col: {col}, replace_row: {replace_row}"
                )
                break

    return ciphertext


def trisemus_decrypt(ciphertext, table):
    ciphertext = ciphertext.lower()
    plaintext = ""
    for char in ciphertext:
        if char == " ":
            plaintext += " "
        else:
            for row in range(len(table)):
                if char in table[row]:
                    col = table[row].index(char)
                    plaintext += table[(row - 1) % len(table)][col]
                    break

    return plaintext


# Пример использования
keyword = "секреты"
plaintext = (
    "Я в своем познании настолько преисполнился, что я как будто бы уже сто триллионов миллиардов"
    " лет проживаю на триллионах и триллионах таких же планет, как эта Земля, мне этот мир"
    " абсолютно понятен, и я здесь ищу только одного - покоя, умиротворения"
)

table = generate_trisemus_table(keyword)
encrypted_text = trisemus_encrypt(plaintext, table)
decrypted_text = trisemus_decrypt(encrypted_text, table)

print(f"table:")
pprint(table)
print(f"\nEncrypted Text:\n{encrypted_text}")
print(f"\nDecrypted Text:\n{decrypted_text}")
