from BitVector import *
from tqdm import tqdm


def findInPredictedWordList(predictedWord:list, item:str):
    try:
        return predictedWord.index(item)
    except ValueError:
        return -1

if __name__=="__main__":
    
    w1 = "e93ae9c5fc7355d5"
    w2 = "f43afec7e1684adf"
    
    w1 = BitVector(hexstring = w1)
    w2 = BitVector(hexstring = w2)

    xor = w1 ^ w2

    words = open('/usr/share/dict/words', 'r').read().splitlines()
    prob = []
    for i in words:
        if len(i) == 8:
            prob.append(i)

    word1 = ''
    word2 = ''
    for i in tqdm(range(len(prob)), leave=False):
        word1 = BitVector(textstring = prob[i])
        decrypt = word1 ^ xor
        word2 = decrypt.get_text_from_bitvector()
        check = findInPredictedWordList(predictedWord=prob, item=word2)
        try:
            prob.index(word2)
            break
        except:
            continue
    print(word1.get_text_from_bitvector())
    print(word2)