import sys
from DES_tex import *

def decimal_to_binary(decimal_value):
    # Convert decimal value to binary string
    binary_string = bin(decimal_value)[2:]  # Remove '0b' prefix
    # Pad binary string to 8 bits if necessary
    binary_string = binary_string.zfill(8)
    return binary_string

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 DES_img.py image.ppm key.txt image_enc.ppm")
        sys.exit(1)

    image_file = sys.argv[1]
    key_file = sys.argv[2]
    output_file = sys.argv[3]

    key = file_read(key_file)

    # Read the PPM image file
    with open(image_file, 'rb') as file:
        header = b''
        pixels = []
        lines = file.readlines()
        headCnt = 0
        for line in lines:
            if headCnt <= 3:
                header += line
                headCnt += 1
            else:
                pixels.append(int(line.decode()))

    cipher = b''

    for i in range(0, len(pixels), 8):
        binary_block = ''.join(bin(byt)[2:] for byt in pixels[i:i+8])
        # Encrypt the 64-bit block
        cipherBlock = encrypt(binary_block, key_processing(key))
        # Split encrypted block into 8 blocks of 8 decimal numbers
        binToDec = [int(cipherBlock[j:j+8], 2) for j in range(0, len(cipherBlock), 8)]

        # k of decimal numbers on new lines
        for num in binToDec:
            cipher += str(num).encode() + b'\n'
    # Combine the encrypted pixels with the original header
    encrypted_image = header + cipher
    
    # Write the encrypted image to a new PPM file
    with open(output_file, 'wb') as file:
        file.write(encrypted_image)
        
    print("Cipher Image Saved to", output_file)

if __name__ == "__main__":
    main()
