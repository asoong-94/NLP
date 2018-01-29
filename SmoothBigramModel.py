import math, collections

class SmoothBigramModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.total = 0
    # self.bigramCounts = collections.defaultdict(lambda: 1)
    self.bigramCounts = {}
    # self.corpus = corpus
    self.train(corpus)

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
        for i in range(1, len(sentence.data)):
            # if word already in dictionary 
            curr = sentence.data[i].word
            prev = sentence.data[i-1].word

            if prev in self.bigramCounts:
                if curr in self.bigramCounts[prev]:
                    self.bigramCounts[prev][curr] += 1
                else:
                    self.bigramCounts[prev][curr] = 1
                    self.total += 1
            # if word not in dictionary yet
            else:
                # create new nested dictionary, and initiate it to 1 cuz of smoothing
                self.bigramCounts[prev] = {}
                self.bigramCounts[prev][curr] = 1
                self.total += 1


  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0 
    for i in range(1, len(sentence) - 1):
        # if sentence[i] in self.bigramCounts:
        try:
            count = self.bigramCounts[sentence[i-1]][sentence[i]] / (self.bigramCounts[sentence[i-1]] + len(self.corpus))
        except:
            count = 1

        if count > 0:
            score += math.log(count)
            score -= math.log(self.total)
            #Ignore unseen words

    return score





