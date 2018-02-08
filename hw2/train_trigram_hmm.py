from collections import defaultdict
class Hmm(object):
    '''
    Stores counts for n-grams and emissions.
    '''
 
    def __init__(self, n=3):
 
        self.n = n
        self.emission_counts = defaultdict(int)
        self.ngram_counts = [defaultdict(int) for i in xrange(self.n)]
        self.all_states = set()

	def get_emission_paras(self):
	    # stores &amp;lt;(word,tag), emission value&amp;gt;
	    self.emision_parameters = defaultdict(float)
	    for wordNtag,counts in self.emission_counts.items():
	        tag = wordNtag[1] #get tag of the tuple
	        tagCount = self.ngram_counts[0][(tag,)]
	        emission = counts / tagCount
	        self.emision_parameters[wordNtag]=emission


	def get_argmax(self):
       #buid argmax list
       for wordNtag,values in self.emision_parameters.items():
           self.argmax_list[wordNtag[0]].append((wordNtag[1],values))
       #build argmax real tag
       for word,values in self.argmax_list.items():
           tag = max(values,key=itemgetter(1))[0]
           self.argmax_value[word]=tag
 
    	print(self.argmax_value)

    def get_trigram_param(self):
 
        self.trigram_param = defaultdict(float)
        for tag_tuple,counts in self.trigram.items():
            subtag = tuple(tag_tuple[1:]) #get tag of the tuple
            tagCount = self.bigram[subtag]
            if tagCount:
                q = counts / tagCount
            else:
                q = 0.
            self.trigram_param[tag_tuple]=q


    #Viterbi Algo
	def viterbi(self,sentence):
	 
	    def findSet(index):
	        if index in range(1,len(sentence)+1):
	            return self.all_states
	        elif index == 0 or index == -1:
	            return {'*'}
	    #stores (word:tag) in this whole sentence
	    sentence_with_tag = defaultdict(str)
	 
	    #inner function to commpute pi values--start
	    def pi_viterbi(k,u,v,sentence):
	        prob = defaultdict(float)
	        #initialization
	        if k==0 and u == '*' and v == '*':
	            return (1.,'*')
	        else:
	            for w in findSet(k-2):
	                prev = pi_viterbi(k-1,w,u,sentence)[0]
	                #tuple((w,u,v))
	                q = self.trigram_param[tuple((w,u,v))]
	                e = self.emision_parameters[tuple((sentence[k-1].lower(),v))]
	                probability = prev * q * e
	                prob [tuple((w,u))] = probability
	            max_tuple = max(prob.items(), key=lambda x: x[1])
	 
	            #print (max_tuple[1],max_tuple[0][0])
	            return max_tuple[1],max_tuple[0][0]
	 
	    #inner function to compute pi values--end
	 
	    sentence_with_tag= list()
	    backpointer=defaultdict(str)
	    tags = defaultdict(str)
	    k = len(sentence)
	    u_glob = ''
	    v_glob = ''
	    glob=0.
	    for i in range(1,k+1):
	        prob = defaultdict(float)
	        for u in findSet(i-1):
	            for v in findSet(i):
	                value,w=pi_viterbi(i,u,v,sentence)
	                prob [tuple((i,u,v))] = value
	                backpointer[tuple((i,u,v))]=w
	        max_tuple = max(prob.items(), key=lambda x: x[1])
	 
	        backpointer[tuple((i,max_tuple[0][1],max_tuple[0][-1]))] = max_tuple[0][1] # bp (k,u,v)= tag w
	 
	        #sentence_with_tag.append(max_tuple[0][-1])
	        u_glob = max_tuple[0][-2]
	        v_glob = max_tuple[0][-1]
	        glob = max_tuple[1]
	        print ('Max',max_tuple)
	    tags[k-1]=u_glob
	    tags[k]=v_glob
	 
	    for i in range((k-2),0,-1):
	        tag = backpointer[tuple(((i+2),tags[i+1],tags[i+2]))]
	        tags[i]=tag
	 
	    tag_list=list()
	    for i in range(1,len(tags)+1):
	        tag_list.append(tags[i])
	 
	    #tag list as results
	    return tag_list




    def classify(word):
		# classify rare words into precise groups
		# only numbers
		if re.findall(r'\d',word):
			return 'NUM'
		# only capitalized letters
		elif re.findall(r'([A-Z]+)$',word):
			return 'ALL_CAP'
		# ends with a capitalized letter,not all capital
		elif re.findall(r'[a-z]+[A-Z]+$',word):
			return 'LAST_CAP'
		else:
			return 'RARE'










