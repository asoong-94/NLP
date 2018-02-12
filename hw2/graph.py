import os 

inputfile = 'ptb.2-21.txt'

lines = []
results = []
sections = 0
with open(inputfile) as inputfile:
    for i, line in enumerate(inputfile.read().splitlines()):
    	lines.append(line)

sections = len(lines) % 1000

for i in range(0, sections):
	f = open('temp.txt', 'w')
	f.write(str(lines[i*1000:(i+1)*1000]))
	f.close()
	os.system("./train_hmm.py ptb.2-21.tgs temp.txt > res.txt")
	res = open("res.txt", 'r').read()
	results.append(resFile)

print results



# ./train_hmm.pl ptb.2-21.tgs 1000.txt > 1000.hmm
