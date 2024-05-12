from crypt import AES
import base64

def decrypt_message(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_bytes = cipher.decrypt(base64.b64decode(ciphertext))
    decrypted_message = decrypted_bytes.decode('utf-8').strip()
    return decrypted_message

def main():
    ciphertext = "3c2b223a71277173636930742f6c296b33702e2a7d127b086b146c09721821083d092c112645265e7b202574126f147c0b690b3d392d2b342b40"
    possible_keys = range(2**16) # Brute-force all possible 16-bit keys
    passphrase = "Hopes and dreams of a million years"

    for key in possible_keys:
        key_bytes = key.to_bytes(16, byteorder='big') # Convert key to bytes
        decrypted_message = decrypt_message(ciphertext, key_bytes)

        # Check if the decrypted message contains the words "Douglas Adams"
        if "Douglas Adams" in decrypted_message:
            print("Found key:", key)
            print("Decrypted message:", decrypted_message)
            break

if __name__ == "__main__":
    main()
