import random 
import time


ef = [
	32,	1,	2,	3,	4,	5,
	4,	5,	6,	7,	8,	9,
	8,	9,	10,	11,	12,	13,
	12,	13,	14,	15,	16,	17,
	16,	17,	18,	19,	20,	21,
	20,	21,	22,	23,	24,	25,
	24,	25,	26,	27,	28,	29,
	28,	29,	30,	31,	32,	1
]
ip = [
	58, 50, 42, 34, 26, 18, 10, 2,
	60,	52,	44,	36,	28,	20,	12,	4,
	62,	54,	46,	38,	30,	22,	14,	6,
	64,	56,	48,	40,	32,	24,	16,	8,
	57,	49,	41,	33,	25,	17,	9,  1,
	59,	51,	43,	35,	27,	19,	11,	3,
	61,	53,	45,	37,	29,	21,	13,	5,
	63,	55,	47,	39,	31,	23,	15,	7
]
pc2 = [
	14, 17, 11, 24, 1, 5,
	3, 28, 15, 6, 21, 10,
	23, 19, 12, 4, 26, 8,
	16, 7, 27, 20, 13, 2,
	41, 52, 31, 37, 47, 55,
	30, 40, 51, 45, 33, 48,
	44, 49, 39, 56, 34, 53,
	46, 42, 50, 36, 29, 32
]
fp = [
	40,	8,	48,	16,	56,	24,	64,	32,
	39,	7,	47,	15,	55,	23,	63,	31,
	38,	6,	46,	14,	54,	22,	62,	30,
	37,	5,	45,	13,	53,	21,	61,	29,
	36,	4,	44,	12,	52,	20,	60,	28,
	35,	3,	43,	11,	51,	19,	59,	27,
	34,	2,	42,	10,	50,	18,	58,	26,
	33,	1,	41,	9,  49,	17,	57,	25
]

def strToBits(input):
	binary = "" #binary string to return
	if len(input) < 8:#if len less than 8
		input = input.ljust(8,'0')#Pad w/ zeros

	for char in input:#get char in input
		binVal = format(ord(char),'08b')#convert to number, than format to binary 8 digits long
		binary += binVal#add binary for char into the binary string

	return binary#return binary string to user

def bitsToStr(input):
	outputString = ""
	#use chr here


def initialPerm(binString, ip):
	return [binString[x-1] for x in ip]#swap positions with initPermutation


def expanFunc(binString, ef):
	return [binString[x-1] for x in ef]#swap positions with initPermutation



def encrypt(plaintext, key):
	ciphertext = ""
	return ciphertext

def decrypt(ciphertext, key):
	plaintext=""
	return plaintext

def DES(number, key, method):
	key = key[:1] + key[1:]

def xor(key, rHalf):
	result = ""
	for num in range(len(str(key))):
		result += str(key[num] ^ rHalf[num])
	return result


if __name__ == '__main__':

	text = ""
	print('DES Implementation:\n')
	while text != "Quit":
		text = str(input('Enter text to encrypt ("Exit" to quit): '))
		random.seed(time.time())
		key = ""
		for _ in range(56):
			keyPart = random.randint(0,1)
			key += str(keyPart)

		intkey = int(key)
		#print(intkey)
		binRep = strToBits(text)
		initialPermutation = initialPerm(binRep, ip)
		lhalf, rhalf = initialPermutation[:len(initialPermutation)//2], initialPermutation[len(initialPermutation)//2:]
		rhalf = expanFunc(rhalf,ef)

		intRhalf = int(''.join(map(str,rhalf)))

		xorRhalf = xor(intkey, intRhalf)


		#xorRhalf =intRhalf ^ intkey
		#print('{0:b}'.format(xorRhalf))


		#xorRhalf= xor(intRhalf, intkey)
		#xorRhalf = intRhalf ^ intkey 
		#print(intRhalf)
		#print(intkey)






		text = "Quit"
		


def split(text):
	textlength = len(text/2)
	return text[:textlength] + text[textlength:]



#for i in range(16):
	#split into 32 bits halves
	lhalf, rhalf = textInput[:len(textInput)//2], textInput[len(textInput)//2:]
	expanFunc(rhalf,ef)



