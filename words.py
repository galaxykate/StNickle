import numpy as np
import random
from scipy import spatial
import re



# All of the vectors
data = []
# Match the words with their indices with their vectors
wordEntries = []
# Look up word indices by word
wordDict = {}

# Allison Parish is a MAGICAL PRINCESS WIZARD
wordfile = 'phonetic-similarity-vectors-master/cmudict-0.7b-simvecs'

with open(wordfile, 'r',encoding="latin-1") as reader:
	lines = reader.read().split("\n")[0:]

	for line in lines:
		word,*val = line.split(" ")
		val = [float(x) for x in val[1:]]
		# print(word)
		# print(val)
		if len(val) > 3:
			index = len(data)
			wordEntries.append({
				"word":word,
				"val":val,
				"index": index
			})
			wordDict[word] = index
			data.append(val)


# Make a cKDTree with the data 
# These are kinda like 
tree = spatial.cKDTree(data)


# for each word, find words which are closer to it
def findClosest(p):
	found = tree.query(p, 10)
	return [wordEntries[index]["word"] for index in found[1]]


# take the original word
# If it's punctuation or not in the dictionary, just pass it back unaltered
# otherwise, transform it!
def translate(ogWord):
	if len(ogWord) == 0:
		return ogWord
	if re.match('[^a-zA-Z\']', ogWord): 
		return ogWord

	# Look up the word
	word = re.sub(r'\W+', '', ogWord.upper())
	if word in wordDict:
		index = wordDict[word]
		# print(index)
		entry = wordEntries[index]
		nearby = findClosest(entry["val"])
		selected = nearby[0].lower()
		nearby = list(filter(lambda x: x != word and ("(" not in x) and (word not in x)  and ("'" not in x) and (x[-1] != "'") and (x[-1] != "."), nearby))
		# print(nearby)
		if len(nearby) > 0:
			selected = nearby[0].lower()
		if ogWord[0].isupper():
			# print("capitalize " + ogWord)
			selected = selected[0].upper() + selected[1:]

		return selected
	else:
		# print("Not found:" + word)
		return ogWord	


	return ogWord
		

with open('stnick.txt', 'r') as reader:
	# Read & print the entire file
	txt = reader.read()

	# Only do a few at a time when testing
	count = 0
	for line in txt.split("\n"):
		if count < 1000:
			# print(line)
			words = re.split('([^a-zA-Z\'])', line)
			# print(words)
			words2 = [translate(word) for word in words]
			print("".join(words2))
		count+=1

		

