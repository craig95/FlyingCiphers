import string
import re
from itertools import permutations


class DefaultDict(dict):
    def __missing__(self, key):
        """If the key is not present, the dict[key] operation calls this method with the key as argument. The value that
        this method returns is then used for the get operation."""
        return 1


class CeaserDecoder:
    def __init__(self, training_data):
        self.bi_counts = DefaultDict()
        self.tri_counts = DefaultDict()
        for word in training_data:
            for bigram in bigrams(word):
                self.bi_counts[bigram] += 1

        for word in training_data:
            for trigram in trigrams(word):
                self.tri_counts[trigram] += 1

    def score(self, plaintext):
        bi_score = 1.0
        for bigram in bigrams(plaintext.lower()):
            bi_score += self.bi_counts[bigram]

        tri_score = 1.0
        for trigram in trigrams(plaintext.lower()):
            tri_score += self.tri_counts[trigram]

        final_score = bi_score + tri_score
        if plaintext.lower()[:12] == "pleasebuyone":
            print(plaintext)
        return final_score

    def decode(self, ciphertext):
        all_shifts = []
        for permutation in permutations([string.ascii_uppercase, '1234567890']):
            permutation = ''.join(permutation)
            all_shifts += [shift_encode(ciphertext, n, permutation) for n in range(len(permutation))]
        # for i in range(len(all_shifts)-1):
        #     if not any(elem in all_shifts[i] for elem in '1234567890'):
        #         print(str(i) + ': ' + all_shifts[i])
        return argmax(all_shifts, self.score)


def bigrams(text):
    return [text[i:i + 2] for i in range(len(text) - 1)]


def trigrams(text):
    return [text[i:i + 3] for i in range(len(text) - 1)]


def shift_encode(plaintext, n, alphabet):
    "Encode text with a shift cipher that moves each letter up by n letters."
    code = ''
    for char in plaintext:
        code += alphabet[(alphabet.index(char) + n) % 36]
    return code


def argmax(sequence, fn):
    best_fn, best_e = max([(fn(e), e) for e in sequence])
    return best_e


text = open('194kwords.txt', 'r').read()
text = re.sub(r'[^A-Za-z0-9 \n]+', '', text)
text = text.lower()
words = text.split()

test = CeaserDecoder(words)
print(test.decode(
    '2XQM5QN7A10QYUXXU104M0P59146T1R5TM4Q5M0PNQOM4QR7X01661NQ5QQ0NA6TQM7564MXUM0S18Q40YQ06M0P2XQM5QNQ8USUXM06'))
