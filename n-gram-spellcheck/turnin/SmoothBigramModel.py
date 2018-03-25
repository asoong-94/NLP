import math, collections

class SmoothBigramModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.total = 0
    self.bigramCounts = collections.defaultdict(lambda: 1)
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """
    for sentence in corpus.corpus:
        for i in range(0, len(sentence.data)-1):
            # bigram is just this word and previous word hashed 
            first = sentence.data[i].word
            second = sentence.data[i+1].word
            self.bigramCounts[first + ' ' + second] += 1
            self.total += 1

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0 
    for i in range(0, len(sentence)-1):
        # bigram is just this word and previous word hashed 
        first = sentence[i]
        second = sentence[i+1]
        count = self.bigramCounts[first + ' ' + second]

        if count > 0:
            score += math.log(count)
            score -= math.log(self.total)
    return score





