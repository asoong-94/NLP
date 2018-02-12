import sys,re
from itertools import izip
from collections import defaultdict

TAG_FILE=sys.argv[1]
TOKEN_FILE=sys.argv[2]

vocab={}
OOV_WORD="OOV"
INIT_STATE="init"
FINAL_STATE="final"

emissions={}
transitions={}
# trigram hmm model 
transitionsTotal=defaultdict(lambda : defaultdict(int))
emissionsTotal=defaultdict(int)


with open(TAG_FILE) as tagFile, open(TOKEN_FILE) as tokenFile:
	for tagString, tokenString in izip(tagFile, tokenFile):


		tags=re.split("\s+", tagString.rstrip())
		tokens=re.split("\s+", tokenString.rstrip())
		pairs=zip(tags, tokens)

		prevtag=INIT_STATE
		prev2tag=INIT_STATE

		for (tag, token) in pairs:
			# print "tag: %s, token: %s" % (tag, token)
			if token not in vocab:
				vocab[token] = 1
				token = OOV_WORD

			if tag not in emissions:
				emissions[tag]=defaultdict(int)				
			# if prevtag not in emissions:
			# 	emissions[prevtag] = defaultdict()
			# if tag not in emissions[prevtag]:
			# 	emissions[prevtag][tag] = defaultdict(int)

			if prev2tag not in transitions:
				transitions[prev2tag] = defaultdict()
			if prevtag not in transitions[prev2tag]:
				transitions[prev2tag][prevtag] = defaultdict(int)


			# emissions[prevtag][tag][token] += 1
			# emissionsTotal[prevtag][tag] += 1

			emissions[tag][token]+=1
			emissionsTotal[tag]+=1

			transitions[prev2tag][prevtag][tag] += 1
			transitionsTotal[prev2tag][prevtag] += 1

			prev2tag = prevtag
			prevtag = tag

		if prev2tag not in transitions:
			transitions[prev2tag] = defaultdict()
		if prevtag not in transitions[prev2tag]:
			transitions[prev2tag][prevtag] = defaultdict(int)

		transitions[prev2tag][prevtag][FINAL_STATE] += 1
		transitionsTotal[prev2tag][prevtag] += 1


for prev2tag in transitions:
	for prevtag in transitions[prev2tag]:
		for tag in transitions[prev2tag][prevtag]:
			print "trans %s %s %s %s" % (prev2tag, prevtag, tag, float(transitions[prev2tag][prevtag][tag]) / transitionsTotal[prev2tag][prevtag])

# for prevtag in emissions:
# 	for tag in emissions[prevtag]:
# 		for token in emissions[prevtag][tag]:
# 			print "emit %s %s %s %s" % (prevtag, tag, token, float(emissions[prevtag][tag][token]) / emissionsTotal[prevtag][tag])
for tag in emissions:
	for token in emissions[tag]:
		print "emit %s %s %s " % (tag, token, float(emissions[tag][token]) / emissionsTotal[tag])









