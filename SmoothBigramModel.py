import math, collections

class SmoothBigramModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.total = 0
    # self.bigramCounts = collections.defaultdict(lambda: 1)
    self.bigramCounts = {}
    self.corpus = corpus
    self.train(self.corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here
    # Tip: To get words from the corpus, try
    #    for sentence in corpus.corpus:
    #       for datum in sentence.data:  
    #         word = datum.word
    for sentence in corpus.corpus:
        for i in range(0, len(sentence.data) -1):
            # if word already in dictionary 
            if sentence.data[i].word in self.bigramCounts:
                if sentence.data[i+1].word in self.bigramCounts[sentence.data[i].word]:
                    self.bigramCounts[sentence.data[i].word][sentence.data[i+1].word] += 1
                else:
                    self.bigramCounts[sentence.data[i].word][sentence.data[i+1].word] = 1
                    self.total += 1
            # if word not in dictionary yet
            else:
                # create new nested dictionary, and initiate it to 1 cuz of smoothing
                self.bigramCounts[sentence.data[i].word] = {}
                self.bigramCounts[sentence.data[i].word][sentence.data[i+1].word] = 1
                self.total += 1


  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0 
    for i in range(1, len(sentence) - 1):
        print "sentence word: " + sentence[i]
        # if sentence[i] in self.bigramCounts:
        count = (self.bigramCounts[sentence[i-1]][sentence[i]] * self.bigramCounts[sentence[i]]) / (self.bigramCounts[sentence[i-1]] + len(self.corpus))
    
        if count > 0:
            score += math.log(count)
            score -= math.log(self.total)
            #Ignore unseen words

    return score





