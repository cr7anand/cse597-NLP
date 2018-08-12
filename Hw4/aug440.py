############################################################
# CSE597: Homework 4
############################################################

student_name = "Anand Gopalakrishnan"

############################################################
# Imports
############################################################

import homework4_data as data

# Include your imports here, if any are used.
import homework4_data as data
import collections


############################################################
# Section 1: Perceptrons
############################################################

class BinaryPerceptron(object):

	def __init__(self, examples, iterations):
		# collecting datapoints from data_label tuples
		example_dict = [data_label[0] for data_label in examples]
		# feature names 
		keys = {key for train_data in example_dict for key in train_data.keys()}

		# init weights to zeros
		self.w = {key: 0 for key in keys}
		
		for _ in range(iterations):
			# loop through all datapoints
			for example in examples:
				feature_vector = collections.defaultdict(int, example[0])
				y_gt = example[1] # ground truth label
				y_hat = self.predict(feature_vector)
				
				# update weights when prediction is wrong
				if y_hat != y_gt:
					if y_gt > 0:  
						for key in self.w.keys():
							self.w[key] = self.w[key] + feature_vector[key]
					else:
						for key in self.w.keys():
							self.w[key] = self.w[key] - feature_vector[key]  

	def predict(self, x):
		dot_product = 0
		x = collections.defaultdict(int, x)
		# computing w.x
		for k in self.w.keys():
			dot_product = dot_product + x[k]*self.w[k]
		if dot_product > 0:
			return True
		else:
			return False

class MulticlassPerceptron(object):

	def __init__(self, examples, iterations):
		categories = {data_label[1] for data_label in examples}
		# collecting datapoints from data_label tuples
		example_dict = [data_label[0] for data_label in examples]
		# feature names
		keys = {key for train_data in example_dict for key in train_data.keys()}

		# init weights to zeros
		self.w = {category: {key: 0 for key in keys} for category in categories}

		for _ in range(iterations):
			
			# loop through all datapoints
			for example in examples:
				feature_vector = collections.defaultdict(int, example[0])
				y_gt = example[1] # ground truth label
				y_hat = self.predict(feature_vector)
				
				# update weights when prediction is wrong
				if y_hat != y_gt:
					for key in keys:
						self.w[y_gt][key] = self.w[y_gt][key] + feature_vector[key]
						self.w[y_hat][key] = self.w[y_hat][key] - feature_vector[key]
    
	def predict(self, x):
		argmax = (None, None)  
		x = collections.defaultdict(int, x)
		# computing w.x
		for category in self.w.keys():
			dot_product = 0
			for key in self.w[category].keys():
				dot_product = dot_product + x[key]*self.w[category][key]
			if dot_product > argmax[0]:
				argmax = (dot_product, category)
		
		# return label of argmax point
		return argmax[1]

############################################################
# Section 2: Applications
############################################################

class IrisClassifier(object):

	def __init__(self, data):
		# creating feature ids
		self.feature_id = ("x1", "x2", "x3", "x4")
		train = []
		
		for data_point in data:
			data_point = list(data_point)
			data_point[0] = dict(zip(self.feature_id, data_point[0]))
			data_point = tuple(data_point)
			train.append(data_point)
		
		# init and train classifier on data
		self.classifier = MulticlassPerceptron(train, 5)

	def classify(self, instance):
		test_data = dict(zip(self.feature_id, instance))
		return self.classifier.predict(test_data)

class DigitClassifier(object):

	def __init__(self, data):
		self.feature_id = set()
		for i in xrange(1, 65):
			self.feature_id.add("".join(["x", str(i)]))
		
		train = []
		for data_point in data:
			data_point = list(data_point)
			data_point[0] = dict(zip(self.feature_id, data_point[0]))
			data_point = tuple(data_point)
			train.append(data_point)

		# init and train classifier on data
		self.classifier = MulticlassPerceptron(train, 25)    

	def classify(self, instance):
		test_data = dict(zip(self.feature_id, instance))
		return self.classifier.predict(test_data)   

class BiasClassifier(object):

	def __init__(self, data):
		# creating feature ids
		self.feature_id = ("x1", "x2")
		train = []
		for data_point in data:
			# adding bias term
			if data_point[0] > 1:
				bias = (data_point[0], 1)
			else:
				bias = (data_point[0], -1)
			data_point = list(data_point)
			data_point[0] = dict(zip(self.feature_id, bias))
			data_point = tuple(data_point)
			train.append(data_point)
		
		# init and train classifier on data
		self.classifier = BinaryPerceptron(train, 5)  

	def classify(self, instance):
		if instance > 1:
			bias = (instance, 1)
		else:
			bias = (instance, -1)
		test_data = dict(zip(self.feature_id, bias))
		return self.classifier.predict(test_data)  

# feature extractor function for mystery 1 data
def radius(data):
	# Inputs
	# data = tuple of (x,y) form
	# Output
	# bool variable for radius > 4 (True if > 4)
	rad = data[0]**2 + data[1]**2
	return (rad > 4)

class MysteryClassifier1(object):

	def __init__(self, data):
		# creating feature ids
		self.feature_id = ("x1")
		train = []
		for data_point in data:
			# extracting feature from data
			rad = radius(data_point[0])
			if rad:
		            feature_mystery = (1,)
			else:
		            feature_mystery = (-1,)
			data_point = list(data_point)
			data_point[0] = dict(zip(self.feature_id, feature_mystery))
			data_point = tuple(data_point)
			train.append(data_point)
		
		# init and train classifier on data
		self.classifier = BinaryPerceptron(train, 5)  

	def classify(self, instance):
		rad = radius(instance)
		if rad:
			feature_mystery = (1,)
		else:
			feature_mystery = (-1,)
			
		test_data = dict(zip(self.feature_id, feature_mystery))
		return self.classifier.predict(test_data)
	
# feature extractor function for mystery 2 data
def negative_count(data):
	negative_counts = 0
	for d in data:
		if d < 0:
			negative_counts = negative_counts + 1
	return negative_counts  

class MysteryClassifier2(object):

	def __init__(self, data):
		# creating feature ids
		self.feature_id = ("x1")
		train = []
		for data_point in data:
			# extracting feature from data
			negative = negative_count(data_point[0])
			if negative % 2 == 0:
				mystery = (1,)
			else:
				mystery = (-1,)
			data_point = list(data_point)
			data_point[0] = dict(zip(self.feature_id, mystery))
			data_point = tuple(data_point)
			train.append(data_point)
		
		# init and train classifier on data
		self.classifier = BinaryPerceptron(train, 5)  

	def classify(self, instance):
		neg_counts = negative_count(instance)
		if neg_counts % 2 == 0:
			feature_mystery = (1,)
		else:
			feature_mystery = (-1,)
		test_data = dict(zip(self.feature_id, feature_mystery))
		return self.classifier.predict(test_data)        

