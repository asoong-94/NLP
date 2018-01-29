import math, collections

class SmoothUnigramModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.total = 0
    self.unigramCounts = collections.defaultdict(lambda: 1)
    self.train(corpus)
    

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here
    # for sentence in corpus.corpus:
    #     for datum in sentence.data:  
    #         word = datum.word
    #         self.unigramCounts[word] += 1
    #         self.total += 1
    for sentence in corpus.corpus:
      for i in range(len(sentence.data)):
        word = sentence.data[i].word
        self.unigramCounts[word] += 1
        self.total += 1

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0 
    for token in sentence:
      count = self.unigramCounts[token]
      if count > 0:
        score += math.log(count)
        score -= math.log(self.total)
      #Ignore unseen words
    return score
