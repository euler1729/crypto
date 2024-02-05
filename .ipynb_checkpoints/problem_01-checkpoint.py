def clean_text(text):
    cleaned_text = ""
    for char in text:
        if char.isalpha():
            cleaned_text += char
    return cleaned_text
    
def vigenere_encrypt(text, key):
    encrypted_text = ""
    key_length = len(key)
    for i, char in enumerate(text):
        shift = ord('A') if char.isupper() else ord('a')

        k = key[i%key_length]
        k_shift = ord('A') if k.isupper() else ord('a')
        k = ord(k) - k_shift
        
        ch = ord(char) - shift
        c = chr((ch+k)%26 + shift)
        
        encrypted_text += c      
        
    return encrypted_text

def vigenere_decrypt(text, key):
    decrypted_text = ""
    key_length = len(key)
    for i, char in enumerate(text):
        shift = ord('A') if char.isupper() else ord('a')

        k = key[i%key_length]
        k_shift = ord('A') if k.isupper() else ord('a')
        k = ord(k) - k_shift
        
        ch = ord(char) - shift
        c = chr((ch-k+26)%26 + shift)
        
        decrypted_text += c 
        
    return decrypted_text

def chunkify_text(text, chunk_size):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def main():
    text = ""
    key = ""
    cipher = ""
    decrypted = ""
    
    #read plain text
    with open('input.txt','r') as file:
        text = file.read()
    #read key
    with open('key.txt','r') as file:
        key = file.read()
        
    # (a) Remove unnecessary characters except A - Z, a - z
    text = clean_text(text)

    # (b) Encode the message using the keyphrase in ‘key.txt’.
    cipher = vigenere_encrypt(text, key)

    # (c) - Convert the ciphertext into 5-character words
    words = chunkify_text(cipher, 5)
    formatted_output = ' '.join(words)

    # Write formatted output to 'output.txt'
    with open('output.txt', 'w') as output_file:
        output_file.write(formatted_output)

    # (d) - Decode the ciphertext in 'output.txt' back to the original message
    decoded_text = vigenere_decrypt(cipher, key)

    with open('decoded.txt', 'w') as file:
        file.write(decoded_text)

    print("KEY: ", key)

    miss_count = 0

    for i in range(len(text)):
        if text[i]!= decoded_text[i]:
            miss_count += 1
    print("Error rate: ", miss_count/len(text)*100)

if __name__ == "__main__":
    main()