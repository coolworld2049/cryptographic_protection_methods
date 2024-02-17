def generate_trisemus_table(keyword):
    keyword = keyword.lower()
    unique_keyword = "".join(sorted(set(keyword), key=keyword.index))

    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    table = [list(unique_keyword)]

    for letter in alphabet:
        if letter not in unique_keyword:
            table[0].append(letter)

    for row in range(1, len(alphabet)):
        table.append(table[0][row:] + table[0][:row])

    return table


def trisemus_encrypt(plaintext, table):
    plaintext = plaintext.lower()
    ciphertext = ""
    for char in plaintext:
        if char == " ":
            ciphertext += " "
        else:
            for row in range(len(table)):
                if char in table[row]:
                    col = table[row].index(char)
                    ciphertext += table[(row + 1) % len(table)][col]
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
keyword = "ключ"
plaintext = "методы криптографической защиты"

table = generate_trisemus_table(keyword)
encrypted_text = trisemus_encrypt(plaintext, table)
decrypted_text = trisemus_decrypt(encrypted_text, table)

print("Original Text:", plaintext)
print("Encrypted Text:", encrypted_text)
print("Decrypted Text:", decrypted_text)
