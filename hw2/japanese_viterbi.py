# Noah A. Smithx
# 2/21/08
# Runs the Viterbi algorithm (no tricks other than logmath!), given an
# HMM, on sentences, and outputs the best state path.

# Translated to python by Austin Chau

import sys
import re
import math
import itertools
from pprint import pprint
from collections import defaultdict

"""
This is a translation of viterbi.pl into python.
Both are essentially a bigram hmm viterbi, which, with modifications, should create the trigram hmm.

Note: There could be a bug in the code that leads to a different result for sentence on line 543 when compared with the original perl script.
"""

INIT_STATE = 'init'
FINAL_STATE = 'final'
OOV_SYMBOL = 'OOV'

hmmfile = 'myjapanese.hmm'
inputfile = 'jv.test.txt'

tags = set() # i.e. K in the slides, a set of unique POS tags
tags2 = set()
trans = {} # transisions
emit = {} # emissions
voc = {} # encountered words

"""
This part parses the my.hmm file you have generated and obtain the transition and emission values.
"""
with open(hmmfile) as hmmfile:
    for line in hmmfile.read().splitlines():
        trans_reg = 'trans\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)'
        emit_reg = 'emit\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)'
        trans_match = re.match(trans_reg, line)
        emit_match = re.match(emit_reg, line)
        if trans_match:
            # print "found trans match"
            qqq, qq, q, p = trans_match.groups()
            # creating an entry in trans with the POS tag pair
            # e.g. (init, NNP) = log(probability for seeing that transition)
            trans[(qqq, qq), q] = math.log(float(p))
            # add the encountered POS tags to set
            tags.update([qqq, qq, q])
        elif emit_match:
            # print "found emit match"
            qq, q, w, p = emit_match.groups()
            # creating an entry in emit with the tag and word pair
            # e.g. (NNP, "python") = log(probability for seeing that word with that tag)
            emit[(q, w)] = math.log(float(p))
            # adding the word to encountered words
            voc[w] = 1
            # add the encountered POS tags to set
            tags.update([q])
        else:
            #print 'no'
            pass


"""
This part parses the file with the test sentences, and runs the sentence through the viterbi algorithm.
"""
with open(inputfile) as inputfile:
    for line in inputfile.read().splitlines():
        line = line.split(' ')
        # initialize pi.
        # i.e. set pi(0, *, *) = 1 from slides
        pi = {(0, INIT_STATE, INIT_STATE): 0.0} # 0.0 because using logs
        bp = {} # backpointers

        # for each word in sentence and their index
        for k, word in enumerate(line):
            k = k + 1
            if word not in voc:
                # change unseen words into OOV, since OOV is assigned a score in train_hmm. This will give these unseen words a score instead of a mismatch.
                word = OOV_SYMBOL
            for u, v, w in itertools.product(tags, tags, tags): #python nested for loop
                # i.e. the first bullet point from the slides.
                # Calculate the scores (p) for each possible combinations of (u, v)
                if ((w, v), u) in trans and (u, word) in emit and (k - 1, w, v) in pi:
                    p = pi[(k - 1, w, v)] + trans[((w, v), u)] + emit[(u, word)]
                    if (k, v, u) not in pi or p > pi[(k, v, u)]:
                        # here, fine the max of all the calculated p, update it in the pi dictionary
                        pi[(k, v, u)] = p
                        # also keeping track of the backpointer
                        bp[(k, v, u)] = (w,v)


        # second bullet point from the slides. Taking the case for the last word. Find the corrsponding POS tag for that word so we can then start the backtracing.
        foundgoal = False
        goal = float('-inf')
        tag = INIT_STATE
        for u, v in itertools.product(tags, tags):
            # You want to try each (tag, FINAL_STATE) pair for the last word and find which one has max p. That will be the tag you choose.
            if ((v, u), FINAL_STATE) in trans and (len(line)-1, v, u) in pi:
                p = pi[(len(line)-1, v, u)] + trans[((v, u), FINAL_STATE)]
                if not foundgoal or p > goal:
                    # finding tag with max p
                    goal = p
                    foundgoal = True
                    tag = (u,v)
                    # tag = u
                    # prevtag = v

        if foundgoal:
            # y is the sequence of final chosen tags
            y = ['.']
            u, v = tag

            for i in xrange(len(line)-1, 2, -1): #counting from the last word
                # bp[(i, tag)] gives you the tag for word[i - 1].
                # we use that and traces through the tags in the sentence.
                v, u = bp[(i, v, u)]
                y.append(v)
                # tag = prevtag
                # prevtag = bp[(i, prevtag, tag)]

            # y is appened last tag first. Reverse it.
            y.reverse()
            # print the final output
            print ' '.join(y)
        else:
            # append blank line if something fails so that each sentence is still printed on the correct line.
            print ''


