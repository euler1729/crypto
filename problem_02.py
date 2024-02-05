import collections


def calculate_shift(ciphertext):
    # Calculate letter frequencies in the ciphertext
    letter_freq = collections.Counter(ciphertext.upper())

    # Assume the most frequent letter in English is 'E'
    most_common_letter = 'E'

    # Calculate the shift for each letter in the key
    key_shifts = {}
    for letter in letter_freq:
        shift = (ord(letter) - ord(most_common_letter)) % 26
        key_shifts[letter] = shift

    return key_shifts

def vigenere_decrypt(ciphertext, key_shifts):
    decrypted_text = ""
    key_length = len(key_shifts)

    for i, char in enumerate(ciphertext):
        if char.isalpha():
            if char.isupper():
                shift = ord('A')
            else:
                shift = ord('a')

            key_char = list(key_shifts.keys())[i % key_length]
            key_shift = key_shifts[key_char]
            decrypted_char = chr((ord(char) - key_shift - shift) % 26 + shift)
            decrypted_text += decrypted_char
        else:
            decrypted_text += char

    return decrypted_text

if __name__ == "__main__":
    ciphers_text = ''
    with open('output.txt','r') as file:
        ciphers_text = file.read().replace(' ','')

    key_shifts = calculate_shift(ciphers_text)

    decrypted_text = vigenere_decrypt(ciphers_text, key_shifts)
    print(decrypted_text[:10])
    
