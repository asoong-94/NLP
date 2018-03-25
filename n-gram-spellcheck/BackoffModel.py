import math, collections

class BackoffModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.unigramTotals = 0
    self.bigramTotals = 0

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
        for x in sentence.data:
            word = x.word
            self.unigramCounts[word] += 1
            self.unigramTotals += 1

        for i in range(0, len(sentence.data)-1):
            first = sentence.data[i].word
            second = sentence.data[i+1].word
            self.bigramCounts[first + ' ' + second] += 1 


    for word in self.unigramCounts:
        self.unigramCounts[word] += 1
        self.unigramTotals += 1

    for word in self.bigramCounts:
        self.bigramCounts[word] += 1


  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0
    for i in range(0, len(sentence)-1):
        first = sentence[i]
        second = sentence[i+1]

        prevCount = self.unigramCounts[first]
        bigramCount = self.bigramCounts[first + ' ' + second]

        if bigramCount > 0:
            score += math.log(bigramCount)
            score -= math.log(prevCount)
        else:
            unigramCount = self.unigramCounts[second]
            score += math.log(unigramCount + 1) 
            score -= math.log(self.unigramTotals)

    return score




    




