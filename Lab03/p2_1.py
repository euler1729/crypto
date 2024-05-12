from BitVector import *

BLOCKSIZE = 8

def encryption(msg:str, p:str):
    cipher = ''
    prev = '0'
    
    for i in range(len(msg)):
        mi = BitVector(size = BLOCKSIZE, intVal = ord(msg[i]))

        mod = (ord(p[i]) + ord(prev)) % 256
        mod = BitVector(size = BLOCKSIZE, intVal = mod)
    
        ci = mi^mod

        prev = ci.get_text_from_bitvector()
        cipher += prev
    return cipher

def decryption(cipher:str, p: str):
    prev = '0'
    plain = ''
    for i in range(len(p)):
        mod = (ord(p[i]) + ord(prev)) % 256
        mod = BitVector(size = BLOCKSIZE, intVal = mod)
        ci = BitVector(size = BLOCKSIZE, intVal = ord(cipher[i]))

        mi = ci ^ mod   
        prev = cipher[i]

        plain += mi.get_text_from_bitvector()
    return plain

if __name__=="__main__":
    message = "BlockChain"
    key = "abcdefghij"

    cipher = encryption(message, key)
    print('Cipher Text: ',cipher)

    plain = decryption(cipher, key)
    print('Plain Text:',plain)