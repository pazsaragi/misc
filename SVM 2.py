import matplotlib.pyplot as plt 
from matplotlib import style
import numpy as np
style.use('ggplot')


class Support_Vector_Machine: 
	def __init__(self, visualisation=True):
		self.visualisation = visualisation
		self.colors = {1:'r',-1:'b'}
		if self.visualisation:
			self.fig = plt.figure()
			self.ax = self.fig.add_subplot(1,1,1)
	def fit(self, data):
		self.data = data 
		#mag =  { ||w||: [w,b] }
		opt_dict = {}
		#for each vector transform by this 

		transforms = [[1,1],
						[-1,1],
						[-1,-1],
						[1,-1]]
		all_data = []
		for yi in self.data:
			for featureset in self.data[yi]:
				for feature in featureset:
					all_data.append(feature)

		self.max_feature_value = max(all_data)
		self.min_feature_value = min(all_data)
		all_data = None
		#w vector steps large then small steps to find minimum
		step_sizes = [self.max_feature_value * 0.1,
						self.max_feature_value * 0.01,
						#point of expense:
						self.max_feature_value * 0.001]
		#Support vectors = yi[Xi.w+b] = 1

		#extremely expensive b steps
		b_range_multiple = 1
		#we dont need to take as small steps with b as with w
		b_multiple = 5
		latest_optimum = self.max_feature_value*10

		for step in step_sizes:
			w = np.array([latest_optimum,latest_optimum])
			#stay false until no more steps down, we can do this because convex
			optimised = False
			while not optimised: 
				for b in np.arange(-1*(self.max_feature_value*b_range_multiple), 
						self.max_feature_value*b_range_multiple, 
						step*b_multiple):
					for transformation in transforms:
						w_t = w*transformation
						found_option = True
						#weakest link in SVM fundamentally
						#SMO attempts to fix this a bit  
						#constraint function is yi(Xi.w+b)>= 1
						for i in self.data:
							for xi in self.data[i]:
								yi=i 
								if not yi*(np.dot(w_t,xi)+b) >= 1:
									found_option = False

						if found_option:
							opt_dict[np.linalg.norm(w_t)] = [w_t,b]

				if w[0] < 0:
					optimised = True
					print('optimised a step.')
				else: 
					w = w - step 

			norms = sorted([n for n in opt_dict])
			#||w|| : [w,b]
			opt_choice = opt_dict[norms[0]]
			self.w = opt_choice[0]
			self.b = opt_choice[1]
			latest_optimum = opt_choice[0][0]+step*2

	def predict(self, features):
		#how to predict? sign( Xi . w+b )
		classification = np.sign(np.dot(np.array(features),self.w)+self.b)
		if classification !=0 and self.visualisation:
			self.ax.scatter(features[0], features[1], s=200, marker='*', c=self.colors[classification])
		return classification

	def visualise(self):
		[[self.ax.scatter(x[0], x[1],s=100,color=self.colors[i]) for x in data_dict[i]] for i in data_dict]
		
		#hyperplane = x.w+b 
		#v = x.w+b
		#positive SV = 1
		#negative SV = -1
		#decision boundary = 0
		def hyperplane(x,w,b,v):
			return (-w[0]*x-b+v) / w[1]

		datarange = (self.min_feature_value*0.9, self.max_feature_value*1.1)
		hyp_x_min = datarange[0]
		hyp_x_max = datarange[1]

		#(w.x+b)
		# pos SV hyperplane
		psv1 = hyperplane(hyp_x_min, self.w, self.b, 1)
		psv2 = hyperplane(hyp_x_max, self.w, self.b, 1)
		self.ax.plot([hyp_x_min, hyp_x_max],[psv1,psv2])

		#(w.x+b)
		# negative SV hyperplane
		nsv1 = hyperplane(hyp_x_min, self.w, self.b, -1)
		nsv2 = hyperplane(hyp_x_max, self.w, self.b, -1)
		self.ax.plot([hyp_x_min, hyp_x_max],[nsv1,nsv2])

		#(w.x+b)
		# decision boundary SV hyperplane
		db1 = hyperplane(hyp_x_min, self.w, self.b, 0)
		db2 = hyperplane(hyp_x_max, self.w, self.b, 0)
		self.ax.plot([hyp_x_min, hyp_x_max],[db1,db2])

		plt.show()

data_dict = {-1:np.array([[1,7],
							[2,8],
							[3,8],]), 

			 1:np.array([[5,1],
							[6,-1],
							[7,3],])}

svm = Support_Vector_Machine()
svm.fit(data=data_dict)
svm.visualise()


