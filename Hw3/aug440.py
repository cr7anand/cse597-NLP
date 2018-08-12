############################################################
# CSE 597: Homework 3
############################################################

student_name = "Anand Gopalakrishnan"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import math


############################################################
# Section 1: Hidden Markov Models
############################################################

def load_corpus(path):
	f = open(path, "r")
	all_lines = f.readlines()
	
	all_sentence_pos_list = []
	# looping over all lines
	for line in all_lines:
		words_plus_tokens = line.split()
		sentence_pos_list = []
		for w in words_plus_tokens:
			sentence_pos_list.append(tuple(w.split('=')))
		
		# appending sentence_pos_list
		all_sentence_pos_list.append(sentence_pos_list)
	
	return all_sentence_pos_list

class Tagger(object):

	def __init__(self, sentences):
		self.initial_tag_prob = {}
		self.transition_prob = {}
		self.emission_prob = {}
		
		# looping over all sentences
		for sent in sentences:
			# initial_tag computation
			
			# adding unseen tags when 1st encountered
			if sent[0][1] not in self.initial_tag_prob:
				self.initial_tag_prob[sent[0][1]] = 1
			
			# incrementing already seen init_tags
			else:
				self.initial_tag_prob[sent[0][1]] += 1
			
			# looping over words in a sentence
			for i in range(len(sent)-1):
				t_i = sent[i][1]    #current tag
				t_j = sent[i+1][1]  #next tag
				
				# computing transition_prob
				# adding unseen key (i.e POS tag t_i)
				if t_i not in self.transition_prob:
					self.transition_prob[t_i] = {}
				
				# counting (t_i, t_j) co-occurences
				if t_j in self.transition_prob[t_i]:
					self.transition_prob[t_i][t_j] += 1
				else:
					self.transition_prob[t_i][t_j] = 1
				
				
			for k in range(len(sent)):
				t_k = sent[k][1]
				w_k = sent[k][0]
 				
				# computing emission_prob
				# adding unseen key (i.e POS tag t_k)
				if t_k not in self.emission_prob:
					self.emission_prob[t_k] = {}
					
				# counting (t_i, w_j) co-occurences
				if w_k in self.emission_prob[t_k]:
					self.emission_prob[t_k][w_k] += 1
					
				else:
					self.emission_prob[t_k][w_k] = 1
		
		# compute actual probabilities for init_tag by dividing by total counts
		total_init_tag = sum(self.initial_tag_prob.values())
		for key in self.initial_tag_prob:
			# laplace smoothing included
			smoothing_constant = 1e-10
			self.initial_tag_prob[key] = float(self.initial_tag_prob[key] + smoothing_constant) / (total_init_tag + len(self.initial_tag_prob.keys())*smoothing_constant)
		
		# compute actual probabilities for transition_tag by dividing by total counts
		for outer_key in self.transition_prob.keys():
			total_transition = sum(self.transition_prob[outer_key].values())
			
			for inner_key in self.transition_prob[outer_key].keys():
				# laplace smoothing included
				smoothing_constant = 1e-10 
				self.transition_prob[outer_key][inner_key] = float(self.transition_prob[outer_key][inner_key] + smoothing_constant) / (total_transition + len(self.transition_prob[outer_key].keys())*smoothing_constant) 
		
		# compute actual probabilities for emission by dividing by total counts
		for outer_key in self.emission_prob.keys():
			total_emission = sum(self.emission_prob[outer_key].values())
			
			for inner_key in self.emission_prob[outer_key].keys():
				# laplace smoothing included
				smoothing_constant = 1e-10
				self.emission_prob[outer_key][inner_key] = float(self.emission_prob[outer_key][inner_key] + smoothing_constant) / (total_emission + len(self.emission_prob[outer_key].keys())*smoothing_constant)
			
			# adding prob value for UNK
			self.emission_prob[outer_key]["<UNK>"] = smoothing_constant / (total_emission + len(self.emission_prob[outer_key].keys())*smoothing_constant)

	def most_probable_tags(self, tokens):
		# iterating over tokens
		most_prob_tags = []
		for token in tokens:
			max_prob = -1
			for tag in self.emission_prob.keys():
				try:
					tag_prob = self.emission_prob[tag][token]
				except:
					# given token not in a particular pos_tag category
					tag_prob = self.emission_prob[tag]["<UNK>"]
				if tag_prob > max_prob:
					max_prob = tag_prob
					# assigning pos_tag to max prob
					max_tag = tag
			# appending max_tag for each token after inner loop
			most_prob_tags.append(max_tag)
		
		return most_prob_tags

	def viterbi_tags(self, tokens):
		# keeping a list of POS tags is handy
		tags = self.emission_prob.keys()
		
		delta = [[0.0 for _ in tags] for _ in tokens]
		back = [[0 for _ in tags] for _ in tokens]
		
		for i in range(len(tags)):
			t = tags[i]
			if tokens[0] in self.emission_prob[t]:
				b = self.emission_prob[t][tokens[0]]  
			else:
				b = self.emission_prob[t]['<UNK>']
			delta[0][i] = self.initial_tag_prob[t]*b
		
		#computing forward
		for t in xrange(1, len(tokens)):
			for j in xrange(len(tags)):
				max_i = 0
				max_val = -1
				for i in xrange(len(tags)):
					tag_i = tags[i]
					tag_j = tags[j]
					val = delta[t-1][i]*self.transition_prob[tag_i][tag_j]

					if val > max_val:
						max_val = val
						max_i = i
					
					# storing back and tag of back
					back[t][j] = max_i
					tag_j = tags[j]
					if tokens[t] in self.emission_prob[tag_j]:            
						b = self.emission_prob[tag_j][tokens[t]] 
					else:
						b = self.emission_prob[tag_j]['<UNK>']
					delta[t][j] = max_val*b
		
		max_i = 0
		max_val = -1
		v_tags = []
		# tracing back
		for i in xrange(len(tags)):
			if delta[-1][i] > max_val:
				max_val = delta[-1][i]
				max_i = i
		v_tags.append(tags[max_i])
		last = max_i
		for t in xrange(len(tokens) - 2, -1, -1):
			last = back[t+1][last]
			v_tags.append(tags[last])

		return list(reversed(v_tags))

