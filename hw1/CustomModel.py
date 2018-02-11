import math, collections
class CustomModel:

  def __init__(self, corpus):
    """Initial custom language model and structures needed by this mode"""
    self.total = 0
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.trigramCounts = collections.defaultdict(lambda: 0)

    self.unigramTotals = 0
    self.bigramTotals = 0
    self.trigramTotals = 0

    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model.
    """  
    # TODO your code here
    for sentence in corpus.corpus:
      for x in sentence.data:
        word = x.word
        self.unigramCounts[word] += 1
        self.unigramTotals += 1

      for i in range(0, len(sentence.data)-1):
        first = sentence.data[i].word
        second = sentence.data[i+1].word
        self.bigramCounts[first + ' ' + second] += 1

      for i in range(0, len(sentence.data)-2):
        first = sentence.data[i].word
        second = sentence.data[i+1].word
        third = sentence.data[i+2].word

        self.trigramCounts[first + ' ' + second + ' ' + third] += 1
        self.total += 1 

    for word in self.unigramCounts:
      self.unigramCounts[word] += 1
      self.unigramTotals += 1

    for word in self.bigramCounts:
      self.bigramCounts[word] += 1

    # for word in self.trigramCounts:
    #   self.trigramCounts[word] += 1
    #   self.total += 1


  def score(self, sentence):
    """ With list of strings, return the log-probability of the sentence with language model. Use
        information generated from train.
    """
    # TODO your code here
    score = 0.0
    for i in range(0, len(sentence)-2):
      first = sentence[i]
      second = sentence[i+1]
      third = sentence[i+2]

      prevCount = self.unigramCounts[first]
      bigramCount = self.bigramCounts[first + ' ' + second]
      trigramCount = self.trigramCounts[first + ' ' + second + ' ' + third] 
      if trigramCount > 0:
        score += math.log(trigramCount)
        score -= math.log(bigramCount)
      elif bigramCount > 0:
        score += math.log(bigramCount)
        score -= math.log(prevCount)
      else:
        unigramCount = self.unigramCounts[second]
        score += math.log(unigramCount + 1)
        score -= math.log(self.unigramTotals)

    return score







