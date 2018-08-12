############################################################
# CSE 597: Homework 2
############################################################

student_name = "Anand Gopalakrishnan"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import string 
import random
import math
import bisect


############################################################
# Section 1: Markov Models
############################################################

def tokenize(text):
	text_space_punc = ''
	for c in text:
		if(c in set(string.punctuation)):
			# inserting spaces between punctuations
			text_space_punc = text_space_punc + " " + c + " "
		else:
			text_space_punc = text_space_punc + c
		tokens = text_space_punc.split()
	
	return tokens    

def ngrams(n, tokens):
	# appending <start> and <end> tokens
	tokens = ['<START>']* (n-1) + tokens + ['<END>']
	list_of_ngrams = []
	for i in range(n - 1,len(tokens)):
		# collecting history tokens
		context = tuple(tokens[i - n + 1 : i]) 
		list_of_ngrams.append((context, tokens[i]))
	return list_of_ngrams    

class NgramModel(object):

	def __init__(self, n):
		self.order = n
		# a dict with both context key and token key
		self.ngram_count = {}
		self.sort_token = {}

	def update(self, sentence):
		sentence_tokens = tokenize(sentence)
		sentence_ngrams = ngrams(self.order, sentence_tokens)
		
		# iterating through setence ngrams
		for (history, token) in sentence_ngrams:
			# adding unseen history when 1st encountered
			if history not in self.ngram_count:
				self.ngram_count[history] = {}
				self.sort_token[history] = []
			
			# counting (history,token) co-occurences
			if token in self.ngram_count[history]:
				self.ngram_count[history][token] = self.ngram_count[history][token] + 1
			else:
				self.ngram_count[history][token] = 1
				self.sort_token[history].append(token)

	def prob(self, context, token):
		# checking for (context, token) co-occurence
		if context in self.ngram_count and token in self.ngram_count[context]:
			token_in_context_count = self.ngram_count[context][token]
		else:
			return 0.0
		# checking for just context occurence        
		#all_tokens_in_context_count = 0
		#for t in self.ngram_count[context]:
		#	all_tokens_in_context_count += self.ngram_count[context][t]
        
		return float(token_in_context_count) / sum(self.ngram_count[context].values())        

	def random_token(self, context):
		self.sort_token[context].sort()
		
		# generating random number in 0-1
		r = random.random()
		
		# holds sum (j=1 -> i prob values)
		sum_prob = 0
		
		for token in self.sort_token[context]:
			# checking token return condition
			if sum_prob <= r and sum_prob + self.prob(context, token) > r:
				return token
			else:
				sum_prob = sum_prob + self.prob(context, token)        

	def random_text(self, token_count):
		token = []
		context = tuple(['<START>']* (self.order - 1))
		
		for i in range(token_count):
			rand_token = self.random_token(context)
			token.append(rand_token)
			#bisect.insort(token, rand_token)
			
			# n = 1, context always being ()
			if self.order == 1:
				context = ()
			# if END token encountered reset
			elif rand_token == '<END>':
				context =  tuple(['<START>']* (self.order - 1))
			else:
				context = context[1 : (self.order - 1)] + tuple([rand_token])
			
		# using join to return space separated items
		return ' '.join(item for item in token)        

	def perplexity(self, sentence):
		# tokenize sentence and generate ngrams
		sent_tokens = tokenize(sentence)
		sent_ngrams = ngrams(self.order, sent_tokens)
		
		log_perplex = 0.0
		m = len(sent_tokens)
		# iterating over ngrams
		for (context, token) in sent_ngrams:
			log_perplex = log_perplex - math.log(self.prob(context, token))
		
		# performing root operation in log space
		log_perplex = log_perplex / (m + 1)
		
		return math.exp(log_perplex)	        

def create_ngram_model(n, path):
	# read file
	f = open(path, "r")
	# read all lines
	all_lines = f.readlines()
	
	# init ngram model
	m = NgramModel(n)
	for line in all_lines:
		m.update(line)
	
	return m    
