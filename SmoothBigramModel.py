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
    # for sentence in corpus.corpus:
    #     for i in range(len(sentence.data)):

    #         self.bigramCounts[sentence.data[i]] += 1
    #         self.bigramCounts[sentence.data[i-1].word + sentence.data[i].word] += 1
    #         self.total += 1
    # https://rstudio-pubs-static.s3.amazonaws.com/115676_ab6bb49748c742b88127e8b5ce3e1298.html
    for sentence in corpus.corpus:
        for i in range(1, len(sentence.data)-1):
            if sentence.data[i] in self.bigramCounts:
                if sentence.data[i+1] in self.bigramCounts[sentence.data[i]]:
                    self.bigramCounts[sentence.data[i]][sentence.data[i+1]] += 1
                else:
                    self.bigramCounts[sentence.data[i]][sentence.data[i+1]] = 1
                    self.total += 1
            else:
                self.bigramCounts[sentence.data[i]] = {}
                self.bigramCounts[sentence.data[i]][sentence.data[i+1]] = 1
                self.total += 1


  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0 
    for i in range(1, len(sentence) - 1):
        # if sentence[i] in self.bigramCounts:
        count = 0
        while sentence[i] in self.bigramCounts:
            count += (self.bigramCounts[sentence[i]][sentence[i+1]] * self.bigramCounts[sentence[i]]) / (self.bigramCounts[sentence[i]] + len(self.corpus))

        # if (self.bigramCounts[word]):
        #     count = self.bigramCounts[word]
        # else:
        #     count = 0

        if count > 0:
            score += math.log(count)
            score -= math.log(self.total)
            #Ignore unseen words
    return score





