import random
import time

Init_Perm = [
    58,	50,	42,	34,	26,	18,	10,	2,
    60,	52,	44,	36,	28,	20,	12,	4,
    62,	54,	46,	38,	30,	22,	14,	6,
    64,	56,	48,	40,	32,	24,	16,	8,
    57,	49,	41,	33,	25,	17,	9,	1,
    59,	51,	43,	35,	27,	19,	11,	3,
    61,	53,	45,	37,	29,	21,	13,	5,
    63,	55,	47,	39,	31,	23,	15,	7
]

Final_Perm = [
    40,	8,	48,	16,	56,	24,	64,	32,
    39,	7,	47,	15,	55,	23,	63,	31,
    38,	6,	46,	14,	54,	22,	62,	30,
    37,	5,	45,	13,	53,	21,	61,	29,
    36,	4,	44,	12,	52,	20,	60,	28,
    35,	3,	43,	11,	51,	19,	59,	27,
    34,	2,	42,	10,	50,	18,	58,	26,
    33,	1,	41,	9,	49,	17,	57,	25

]

Expan_Tab = [
    32,	1,	2,	3,	4,	5,
    4,	5,	6,	7,	8,	9,
    8,	9,	10,	11,	12,	13,
    12,	13,	14,	15,	16,	17,
    16,	17,	18,	19,	20,	21,
    20,	21,	22,	23,	24,	25,
    24,	25,	26,	27,	28,	29,
    28,	29,	30,	31,	32,	1
]

Perm_Tab = [
    16,	7,	20,	21,	29,	12,	28,	17,
    1,	15,	23,	26,	5,	18,	31,	10,
    2,	8,	24,	14,	32,	27,	3,	9,
    19,	13,	30,	6,	22,	11,	4,	25,
]

PC2 = [
    14,	17,	11,	24,	1,	5,
    3,	28,	15,	6,	21,	10,
    23,	19,	12,	4,	26,	8,
    16,	7,	27,	20,	13,	2,
    41,	52,	31,	37,	47,	55,
    30,	40,	51,	45,	33,	48,
    44,	49,	39,	56,	34,	53,
    46,	42,	50,	36,	29,	32,

]

SBox = [
    14, 4,  13, 1, 2,  15, 11, 8,  3,  10, 6,  12, 5,  9,  0, 7,
    0,  15, 7,  4, 14, 2,  13, 1,  10, 6,  12, 11, 9,  5,  3, 8,
    4,  1,  14, 8, 13, 6,  2,  11, 15, 12, 9,  7,  3,  10, 5, 0,
    15, 12, 8,  2, 4,  9,  1,  7,  5,  11, 3,  14, 10, 0,  6, 13
]

#generate 56 bit key based on system time
def generate_key():
    random.seed(time.time())
    return format(random.getrandbits(56), '056b')

#function to permute block against the perumtation tables
def permute(block, table):
    return ''.join(block[i-1] for i in table)

#functrion to xor
def xor(bits1, bits2):
    return ''.join('1' if b1 != b2 else '0' for b1, b2 in zip(bits1, bits2))

#sbox, only first box
def s_box_substitution(bits):
    output = ''
    for i in range(0, len(bits), 6):
        block = bits[i:i+6]
        row = block[0] + block[5]
        column = block[1:5]
        colInt = int(column, 2)
        rowInt = int(row, 2)
        output += format(SBox[rowInt * 16 + colInt], '04b')
    return output

#left shift for the key
def circular_left_shift(key, shifts):
    return key[shifts:] + key[:shifts]

#schedule the left shifts for each of the 16 rounds
def key_schedule(key, rounds=16):
    for _ in range(rounds):
        yield circular_left_shift(key, 1)

def pad(text):
    #calculate padding for text non multiple of 8
    padding_length = 8 - (len(text) % 8)
    padding = chr(padding_length) * padding_length
    #convert int to unicode
    return text + padding

def unpad(text):
    #remove padding for multiple chars(doesnt work perfectly)
    padding_length = ord(text[-1])
    return text[:-padding_length]

def DES(text, key, encrypt=True):
    #pad text if not multiple of 8
    if encrypt:
        text = pad(text)
    
    binaryData = ''.join(format(ord(char), '08b') for char in text)
    blocks = [binaryData[i:i+64] for i in range(0, len(binaryData), 64)]
    #for after permutations, sbox, etc
    processed_blocks = []
    #get keys from key scheduler, add to subkey
    subkeys = list(key_schedule(key))
    #reverse to decrypt
    if not encrypt:
        subkeys.reverse()

    #loop through blocks of bits
    for block in blocks:
        #split bits in half
        permuted_block = permute(block, Init_Perm)
        left, right = permuted_block[:32], permuted_block[32:]
        for subkey in subkeys:
            #loop for each round
            right_expanded = permute(right, Expan_Tab)
            right_xored = xor(right_expanded, subkey)#first xor
            rightSub = s_box_substitution(right_xored)#sBox
            new_right = permute(rightSub, Perm_Tab)#second permute
            new_left = xor(left, new_right)#second xor
            left, right = right, new_left#swap left and right

        pre_final_permutation = right + left
        final_permuted_blocks = permute(pre_final_permutation, Final_Perm)
        processed_blocks.append(final_permuted_blocks)#add them back

    #join blocks back together
    outputBin = ''.join(processed_blocks)
    #transfer back to string
    output = ''.join(chr(int(outputBin[i:i+8], 2)) for i in range(0, len(outputBin), 8))
    
    #if decrypt, unpad to get rid of useless chars
    if not encrypt:
        output = unpad(output)
    return output


#pass text and key to des to encrypt
def encrypt(text, key, encrypt=True):
    return DES(text, key, encrypt)

#pass text and key to des to decrypt
def decrypt(text, key, encrypt=False):
    return DES(text, key, encrypt)


if __name__ == '__main__':
    text= ""
    key = generate_key()
    while text.lower() != 'quit':
        print("Enter text to encrypt or decrypt ('Quit' to stop): ")
        text = input()
        encryptedText = encrypt(text, key, encrypt)
        decrypteText = decrypt(encryptedText, key, encrypt)
        print('Encrypted:', encryptedText)
        print('Decrypted:', decrypteText)
        #pass output to file because it is weird for some reason
        with open("Output.txt", "w", encoding="utf-8") as f:
            f.write("encrypted text: %s\n" % encryptedText)
            f.write("decrypted text: %s\n" % decrypteText)

        f.close()
