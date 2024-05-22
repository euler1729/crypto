import freqAnalysis
import itertools
from tqdm import tqdm


def read_file(file_name):
    with open (file_name, 'r') as file:
        text = file.read()
    return text

def write_file(file_name, text):
    with open(file_name, 'w') as file:
        file.write(text)


def find_repeated_sequence(text):
    distances = []
    for i in range (0, len(text)):

        # Take substring of length key_len
        sub_string_1 = text[i : i + 3]

        # For every substring of length 3 check if it matches with sub_string_1
        for j in range(i + 3, len(text)):
            sub_string_2 = text[j : j + 3]
            if sub_string_1 == sub_string_2:
                # If match found, record the distances between the matches
                distances.append(j - i)
                # print(distances)
    
    return distances


def get_factors(distances):
    factors = []
    # don't consider 1
    for i in range(0, len(distances)):
        n = distances[i]

        for j in range(2, n):
            # Check while j < sqrt(n)
            if j * j > n:
                break 
            
            if n % j == 0 and j < 10:
                factors.append(j)
                if j != (int)(n/j) and j < 10:
                    factors.append((int)(n/j))

    # print(len(factors))

    return factors
            


def get_key_lengths(ciphertext):
    # Perform Kasiski examination to estimate key length
    

    # Find matching sequences of length 3 to find the possible key lengths
    distances = find_repeated_sequence(ciphertext)

    # Get all the factors of the found distances
    factors = get_factors(distances)

    # Find the factors with the highest apperance
    mp = {} # Map to store frequency
    for i in range (len(factors)):
        # count the frequency of each factor
        mp[factors[i]] = mp.get(factors[i], 0) + 1
    
    possible_key_lengths = []
    cnt = {}
    for i in tqdm(range(len(factors))):
        # Assume that the factor that appeared more than 500 times is a possible length of the key
        if(mp.get(factors[i], 0) >= 500 and cnt.get(factors[i], 0) == 0):
            if (factors[i] > 2):
                possible_key_lengths.append(factors[i])
            cnt[factors[i]] = cnt.get(factors[i], 0) + 1
    
    return possible_key_lengths

def match_length(text, key):
    while len(key) < len(text):
        key += key

    while len(key) > len(text):
        key = key[:-1]
    
    # print(text)
    # print(key)
    return key

def vigenere_decrypt(ciphertext, key):
    
    if(len(key) < len(ciphertext)):
        key = match_length(ciphertext, key)

    # print(ciphertext, key)
    plaintext = ''

    key_len = len(key)
    
    for i, char in enumerate(ciphertext):
         # Determine the shift 
        shift = ord(key[i % key_len]) - ord('a')
        
        # Decrypt the character 
        if char.isupper():
            plaintext += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        else:
            plaintext += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
    # print(plaintext)
    return plaintext


def generate_possible_keys(all_freq_scores):
    possible_keys = []

    # Generate all possible keys
    for combination in itertools.product(*all_freq_scores):
        current_string = ''.join(inner_tuple[1] for inner_tuple in combination)
        possible_keys.append(current_string)

    return possible_keys
    


def getItemAtIndexOne(x):
    return x[0]

def test_for_key_length(ciphertext, key_len):
    # take every i-th letters of the text and analyze
    all_texts = []
    
    for i in range (key_len):
        cur_text = ''
        for j in range(i, len(ciphertext), key_len):
            cur_text += ciphertext[j]
        # print(cur_text)
        all_texts.append(cur_text)
    
    all_freq_scores = []

    # cipherUp = ciphertext.upper()

    for i in range (key_len):
        # Check the options for i-th letter
        freq_scores = []

        for j in range(26):
            letter = chr(j + 65)

            cipherUp = all_texts[i].upper()
            # print(letter, cipherUp)
            decrypted_text = vigenere_decrypt(cipherUp, letter)
            score = freqAnalysis.englishFreqMatchScore(decrypted_text)

            freq_scores.append((score, letter))

        for j in range(26):
            letter = chr(j + 97)

            cipherUp = all_texts[i].upper()
            # print(letter, cipherUp)
            decrypted_text = vigenere_decrypt(cipherUp, letter)
            score = freqAnalysis.englishFreqMatchScore(decrypted_text)

            freq_scores.append((score, letter))

        freq_scores.sort(key = getItemAtIndexOne, reverse=True)

        all_freq_scores.append(freq_scores[:2]) # attempt for maximum 2 most frequent letters
    
    # print(all_freq_scores)


    possible_keys = generate_possible_keys(all_freq_scores)

    test_the_keys(ciphertext, possible_keys)


def test_the_keys(ciphertext, possible_keys):

    mx = 0
    for i in range(len(possible_keys)):
        decrypted_text = vigenere_decrypt(ciphertext, possible_keys[i])
        mx = max(mx, freqAnalysis.englishFreqMatchScore(decrypted_text))

    for i in range(len(possible_keys)):
        decrypted_text = vigenere_decrypt(ciphertext, possible_keys[i])
        if(freqAnalysis.englishFreqMatchScore(decrypted_text) == mx):
            write_file('decrypted_without_key', decrypted_text)


def main():
    # Read ciphertext from 'output.txt'
    ciphertext = read_file('output.txt')
    print("Length of the ciphertext:", len(ciphertext))

    # Get possible key lengths
    possible_key_lengths = get_key_lengths(ciphertext)

    # Print the possible key lengths
    print("Number of possible Key lengths:", len(possible_key_lengths))

    for i in possible_key_lengths:
        if i == 7:
            test_for_key_length(ciphertext, i)
        print("Possible Key length:", i)


if __name__ == "__main__":
    main()