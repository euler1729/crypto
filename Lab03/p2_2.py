from BitVector import *
import itertools as it
from tqdm import tqdm

validChar = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz?!-()., '
punctuations = ['.', ',', ' ', '(', ')', '-', '!', '?']


def isValid(words:list, value:str):
    try:
        return words.index(value)
    except ValueError:
        return -1

def getPredictedChar(prevcipherletter, col):
    count = 0
    prob_char = []
    prob_pad = []
    for i in range(256):
        for j in range(len(col)):
            mod = ((prevcipherletter[j]) + i)%256
            mod_bv = BitVector(size=8, intVal= mod)
            
            cipher_bv = BitVector(size= 8, intVal= col[j])
            pred = mod_bv ^ cipher_bv
            char = pred.get_text_from_bitvector()
            if validChar.find(char) != -1:
                count += 1
        if (count) >= 10:
            prob_pad.append(i)
            prob_char.append(char)
        count = 0

    return prob_char, prob_pad


def getPlain(reverse):

    words = []
    with open("/usr/share/dict/words", "r") as f:
        for line in f:
            words.append(line.strip('\n')) #line

    prob_chars = []
    prob_pad = []

    prob_char, pad = getPredictedChar([0]*10, reverse[0])
    prob_chars.append(prob_char)
    prob_pad.append(pad)
    

    for i in range(1, len(reverse)):
        prob_char, pad = getPredictedChar(reverse[i-1], reverse[i])
        prob_chars.append(prob_char)
        prob_pad.append(pad)

    permu = []
    punc_idx = []
    val = 1
    for i in range(len(prob_chars)):
        if all(elem in punctuations for elem in prob_chars[i]):
            permu.append(val)
            punc_idx.append(i)
            val = 1
        else:
            val *= (len(prob_chars[i]))
        if i == len(prob_chars)-1:
            permu.append(val)
 
    plain10 = []
    prev = 0
    punc_idx.append(60)

    for j in range(len(punc_idx)):
        ax = []
        for i in range(permu[j]):
            w = ''.join(list(it.product(*prob_chars[prev:punc_idx[j]]))[i])
            if isValid(words=words, value = w) != -1:
                ax.append(w)
        plain10.append(ax)
        prev = punc_idx[j]+1

    return plain10

def preprocess(cipherFile:str):
    value = []
    with open(cipherFile, "r") as f:
        for row in f:
            row = row.replace("[", "")
            row = row.replace("]", "")
            row = row.replace("\n", "")
            row = row.replace(" ", "")
            value.append(list(map(int, row.split(","))))
    return value

if __name__ == '__main__':
    
    cipher = preprocess("Ciphertext_Assignment_3.txt")

    reverse = []
    for i in range(len(cipher[0])):
        col = []
        for j in range(len(cipher)):
            a = (j+0)%10
            col.append(cipher[a][i])
        reverse.append(col)

    plain10 = getPlain(reverse)

    val = 1
    for i in range(len(plain10)):
        val *= len( plain10[i])

    print(val)

    for i in range(len(plain10)):
        print(plain10[i])

    print('\n\n\n')
    prob_msg = []
    for i in range(val):
        prob_msg.append(' '.join(list(it.product(*plain10[:]))[i]))
    print(prob_msg[-10:])