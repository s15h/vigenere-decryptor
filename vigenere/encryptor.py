import os.path
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


# vigenere en/decrypt
def vigenere(keystr, plaintext):
    ciphertext = ''
    keylist = keystr.lower()
    keycounter = 0
    for i in range(0, len(plaintext)):
        plet = plaintext[i].lower()
        if plet in ALPHABET:
           textindex = ALPHABET.index(plet)
           keyindex = ALPHABET.index(keylist[keycounter % len(keylist)])
           clet = ALPHABET[(textindex + keyindex) % 26]
           keycounter = keycounter + 1
           if plaintext[i].isupper():
              clet = clet.upper()
           ciphertext = ciphertext + clet
        else:
           ciphertext += plaintext[i]
    return ciphertext

# determine the "inverse" key to use.
# This ensures that
#     plaintext == vigenere( vig_decryptkey(KEY), vigenere(KEY, plaintext) )
def vig_decryptkey(encryptkey):
	decryptkey = ""
	for i in encryptkey:
		decryptkey += ALPHABET[(len(ALPHABET) - ALPHABET.index(i)) % 26]
	return decryptkey

# Caesar en/decrypt
def caesar(n, string):
    retstr = ""
    for i in string:
         if i in ALPHABET:
            index = ALPHABET.index(i)
            retstr = retstr + ALPHABET[(index + n) % 26]
         else:
            retstr += i
    return retstr


def strtolist(str):
	return [ALPHABET.index(i) for i in str]


# Split a string into N buckets
# only go to next bucket upon an alphabetic character
# i.e., characters like ",.:?! are added but do not change the bucket
def splitstring(cnt, str):
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	retval = ['' for _ in range(cnt)]
	bucket_idx = 0
	for char in str:
		retval[bucket_idx] += char
		if char.lower() in alphabet:
			bucket_idx = (bucket_idx + 1) % cnt
	return retval

# gives the distribution (percentages) of occurrences of alphabet letters
def letter_distribution(str):
	sum = 0
	dict = countlettersstr(str)
	for i in dict:
		sum += dict[i]
	return {i: dict[i] * 100 / sum for i in dict}


#	Breaks a string into N buckets, returns letter distribution
#	for each bucket
def vig_dist(N, str):
	splittedtxt = splitstring(N, str)
	retval = []
	for i in splittedtxt:
		retval.append(letter_distribution(i))
	return retval

# prints the maximum value of a list of dicts, i.e. a list of
# distributions of letter frequencies
def print_max_dist_val(listofdicts):
	for i in listofdicts:
		print(max(i.values()))

def countlettersstr(str):
	str = str.lower()

	# gebruik list comprehension
	return {i: str.count(i) for i in ALPHABET}

	## Dit is hetzelfde als:
	## ret = {}
	## for i in alphabet:
	## 	ret[i] = str.count(i)
	## return ret

# Converts a dictionary with frequencies to one with percentages
# I.e., something like {'a': 1837, 'b': 734, 'c': 190, ...}
#       becomes sth like {..., 'e': 0.1789, ..., 'n': 10.012, ...}
def dictfreqtopercent(dict):
	sum = 0
	for i in dict:
		sum += dict[i]
	return map(lambda x: x / sum, dict)

# Counts letters in a file
def countlettersfile(fname):
	ret = {}
	file = open(fname, "r")
	contents = file.read().lower()
	for i in ALPHABET:
		ret[i] = contents.count(i)
	return ret

# Determine the vigenere key used given a plain- and ciphertext
def vigkey(plaintext, ciphtext):
	ptxt = plaintext.lower()
	ctxt = ciphtext.lower()
	key = ""
	for i in range(len(ptxt)):
		if ctxt[i] in ALPHABET:
			keyidx = ALPHABET.index(ctxt[i]) - ALPHABET.index(ptxt[i])
			key = key + ALPHABET[keyidx % 26]
	return key.upper()


# Encrypt an entire file -- apparently broken :s
#
# WARNING FOR STUDENTS: APPARENTLY BROKEN!!
#  (basics of code works when run directly in interactive mode, not from
#   subroutine. Haven't gotten round to investigating)
def vigefile(fname, key):
	if os.path.exists(fname):
		with open(fname, 'r') as file:
			return vigenere(key, file.read())
	else:
		return "File not found."

