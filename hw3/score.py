import math as m
sum = 0
lc = 0






def score(file):
	sum = 0
	linecount = 0
	for line in open(file, 'r'):
		tokens = line.split()
		sent_prob = float(tokens[1])
		sum -= m.log(sent_prob, 2)
		linecount += 1
	print("Cross entropy = ", sum / linecount)


if __name__ == '__main__':
	score("out.txt")
	score("out2.txt")
	score("myOut.txt")