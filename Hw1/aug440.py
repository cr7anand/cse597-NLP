############################################################
# CSE597: Homework 1
############################################################

student_name = "Anand Gopalakrishnan"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import email
import math
import os
import collections
############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):    
	fp = open(email_path)
	msg = email.message_from_file(fp)
	lines = email.iterators.body_line_iterator(msg)
	tokens = []
	for line in lines:
		tokens = tokens + line.rstrip('\n').split()
	return tokens

def log_probs(email_paths, smoothing):
	log_probability = {}
	counts = {}
	total = 0
	for email_path in email_paths:
		tokens = load_tokens(email_path)
		total = total + len(tokens)
		for word in tokens:
			if word in counts:
				counts[word] += 1
			else:
				counts[word] = 1
	
	for word in counts:
		log_probability[word] = math.log((counts[word] + smoothing) / (total  + smoothing*(len(counts) + 1)))
	
	# log_probs of UNK
	log_probability["<UNK>"] = math.log(smoothing / (total  + smoothing*(len(counts) + 1)))
	
	return log_probability

class SpamFilter(object):

	def __init__(self, spam_dir, ham_dir, smoothing):
		spam_paths = [os.path.join(spam_dir, f) for f in os.listdir(spam_dir)]
		ham_paths = [os.path.join(ham_dir, f) for f in os.listdir(ham_dir)]
		self.log_probability_spam = log_probs(spam_paths, smoothing)
		self.log_probability_ham = log_probs(ham_paths, smoothing)
		self.p_spam = float(len(spam_paths)) / (len(spam_paths) + len(ham_paths))
		self.p_ham  = float(len(ham_paths)) / (len(ham_paths) + len(spam_paths))
    
	def is_spam(self, email_path):
		tokens = load_tokens(email_path)
		prob_token_given_spam = 0.0
		prob_token_given_ham = 0.0
		# computing spam probs
		for token in tokens:
			if token in self.log_probability_spam:
				prob_token_given_spam += self.log_probability_spam[token]
			else:
				prob_token_given_spam += self.log_probability_spam["<UNK>"]
		
		# computing ham probs
		for token in tokens:
			if token in self.log_probability_ham:
				prob_token_given_ham += self.log_probability_ham[token]
			else:
				prob_token_given_ham += self.log_probability_ham["<UNK>"]
		
		#computing class probs
		spam_class_given_doc = math.log(self.p_spam) + prob_token_given_spam
		ham_class_given_doc = math.log(self.p_ham) + prob_token_given_ham
		
		if(spam_class_given_doc > ham_class_given_doc):
			return True
		else:
			return False

	def most_indicative_spam(self, n):
		spam_indication = {}
		for token in self.log_probability_spam:
			# checking if token exists in ham as well
			if(token in self.log_probability_ham):
				#computing total prob P(w)
				p_word = math.exp(self.log_probability_spam[token])*self.p_spam + math.exp(self.log_probability_ham[token])*self.p_ham 
				spam_indication[token] = self.log_probability_spam[token] - math.log(p_word)
				
		n_spam_indication = sorted(spam_indication, key = spam_indication.get, reverse=True)[:n]
		
		return n_spam_indication   

	def most_indicative_ham(self, n):
		ham_indication = {}
		for token in self.log_probability_ham:
			# checking if token exists in ham as well
			if(token in self.log_probability_spam):
				#computing total prob P(w)
				p_word = math.exp(self.log_probability_spam[token])*self.p_spam + math.exp(self.log_probability_ham[token])*self.p_ham 
				ham_indication[token] = self.log_probability_ham[token] - math.log(p_word)
				
		n_ham_indication = sorted(ham_indication, key = ham_indication.get, reverse=True)[:n]
		
		return n_ham_indication  
