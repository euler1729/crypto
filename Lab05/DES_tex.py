import sys


# initial permutation
initial_perm = [58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7]

# Expansion D-box Table
exp_d = [32, 1, 2, 3, 4, 5, 4, 5,
        6, 7, 8, 9, 8, 9, 10, 11,
        12, 13, 12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21, 20, 21,
        22, 23, 24, 25, 24, 25, 26, 27,
        28, 29, 28, 29, 30, 31, 32, 1]

# Straight Permutation Table
per = [16, 7, 20, 21, 29, 12, 28, 17,
        1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9,
        19, 13, 30, 6, 22, 11, 4, 25]

# S-box Table
sbox = [[
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

            [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

            [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
            
            [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
            
            [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
            
            [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
            
            [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
            
            [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
        ]]

# final permutation
final_perm = [40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25]

# key permutation 1
keyp1 = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

# shift table
shift_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


# key permutation 2
keyp2 = [14, 17, 11, 24, 1, 5, 3, 28,
        15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56,
        34, 53, 46, 42, 50, 36, 29, 32]

# convert a hex to binary
def hex_to_bin(text):
    mp = {'0': '0000', '1': '0001', '2': '0010', '3': '0011',
        '4': '0100', '5': '0101', '6': '0110', '7': '0111',
        '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
        'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'}
    res = ''.join(mp[i] for i in text)
    return res

# convert a binary to hex
def bin_to_hex(text):
    mp = {'0000': '0', '0001': '1', '0010': '2', '0011': '3',
        '0100': '4', '0101': '5', '0110': '6', '0111': '7',
        '1000': '8', '1001': '9', '1010': 'A', '1011': 'B',
        '1100': 'C', '1101': 'D', '1110': 'E', '1111': 'F'}
    res = ''.join(mp[text[i:i+4]] for i in range(0, len(text), 4))
    return res

# ascii to binary
def ascii_to_bin(text):
    res = ''.join(format(ord(i), '08b') for i in text)
    return res

# binary to ascii
def bin_to_ascii(text):
    res = ''.join(chr(int(text[i:i+8], 2)) for i in range(0, len(text), 8))
    return res

# binary to decimal
def bin_to_dec(text):
    res = int(text, 2)
    return res

# decimal to binary
def dec_to_bin(text):
    res = format(text, '08b')
    return res

# permutation
def permute(text, table, n):
    res = ''
    for i in range(n):
        res += text[table[i]-1]
    return res

# xor
def xor(a, b):
    res = ''
    for i in range(len(a)):
        if a[i] == b[i]:
            res += '0'
        else:
            res += '1'
    return res

#shift the bits to the left by n bits
def shift_left(text, n):
    return text[n:] + text[:n]


# padding
def padding(text):
    plen = (len(text)+63) // 64 * 64
    return text.ljust(plen, '0')

# file read
def file_read(filename):
    with open(filename, 'r') as f:
        return f.read()
        
# file write
def file_write(filename, text):
    with open(filename, 'w') as f:
        f.write(text)      
        


# key processing
def key_processing(key):
    key = ascii_to_bin(key)
    #getting 56 bit key from 64 bit
    key = permute(key, keyp1, 56)
    # split the key into two
    left = key[:28]
    right = key[28:]
    
    round_keys = []
    round_keys.append(key)
    for i in range(16):
        # shift the key
        left = shift_left(left, shift_table[i])
        right = shift_left(right, shift_table[i])
        
        # combine the key
        combine_key = left + right
        # key permutation 2
        round_key = permute(combine_key, keyp2, 48)
        round_keys.append(round_key)
    return round_keys

# f(R, K)
def f(R, K):
    # expansion
    R = permute(R, exp_d, 48)
    # xor
    xor_r = xor(R, K)
    
    # s-box
    s_res = ''
    for i in range(8):
        row = int(xor_r[i] + xor_r[i+5], 2)
        col = int(xor_r[i+1:i+5], 2)
        val = sbox[i][row][col]
        s_res += format(val, '04b')
    
    # straight permutation
    s_res = permute(s_res, per, 32)
    return s_res

# encrypt
def encrypt(text, round_keys):
    cipher = ''
    txt = padding(text)
    txt = permute(txt, initial_perm, 64)
    
    left, right = txt[:32], txt[32:]
    i = 0
    for k in round_keys[1:]:
        op = f(right, k)
        op = xor(left, op)
        left = right
        right = op
        # print(bin_to_hex(left), bin_to_hex(right))
    cipher = permute(right + left, final_perm, 64)
    return cipher

# _encrypt 
def _encrypt(text, key):
    kk = key_processing(key)
    # for k in kk:
    #     print(bin_to_ascii(k))
    txt = ascii_to_bin(text)
    blocks  = []
    
    for i in range(0, len(txt), 64):
        block = encrypt(txt[i:i+64], kk)
        blocks.append(block)
    
    cipher = ''.join(blocks)
    cipherhex = bin_to_hex(cipher)
    print('Cipher Text:', cipherhex)
    file_write('encrypted.txt', cipherhex)

# decrypt
def decrypt(text, round_keys):
    plain = ''
    # txt = hex_to_bin(text)
    txt = permute(text, initial_perm, 64)
    
    left, right = txt[:32], txt[32:]
    
    for k in reversed(round_keys[1:]):
        temp = right
        right = xor(left, f(right, k))
        left = temp
    plain = permute(right + left, final_perm, 64)
    return plain
    
# _decrypt
def _decrypt(text, key):
    kk = key_processing(key)
    txt = hex_to_bin(text)
    blocks = []
    
    for i in range(0, len(txt), 64):
        block = decrypt(txt[i:i+64], kk)
        blocks.append(block)
    plain = ''.join(blocks)
    plain = bin_to_ascii(plain)
    print('Decrypted Text:', plain)
    file_write('decrypted.txt', plain)
    
# main
def main():
    if len(sys.argv) != 4:
        print('Usage: python DES_tex.py <message/encrypted>.txt <key>.txt <encrypted/decrypted>.txt')
        sys.exit(1)
    inputfile = sys.argv[1]
    key = sys.argv[2]
    filename = sys.argv[3]
    
    is_encrypt = inputfile.startswith('message')
    text = file_read(inputfile)
    # print('Text:', text)
    key = file_read(key)
    
    if is_encrypt:
        print('Encrypting...')
        _encrypt(text, key)
    else:
        print('Decrypting...')
        _decrypt(text, key)

if __name__ == '__main__':
    main()