import os
import math
from pde import *
#from scipy.stats import norm

class FDMBase:
	def __init__(self, edp, Xmax, J, T, N):
		self.edp = edp
		self.X = Xmax
		self.J = J
		self.dx = Xmax/J
		self.T = T
		self.N = N
		self.dt = T/N
		self.prev_t = 0
		self.cur_t = 0
		self.alpha = 0
		self.beta = 0
		self.gamma = 0
		self.somme = 0
		self.x_values = [0]*(self.J+1)
		self.new_result = [0]*(self.J+1)
		self.old_result = [0]*(self.J+1)

	def calculate_step_sizes(self):
		raise NotImplementedError('subclasses must implement calculate_step_sizes!')
	def set_initial_conditions(self):
		raise NotImplementedError('subclasses must implement set_initial_conditions!')
	def calculate_boundary_conditions(self):
		raise NotImplementedError('subclasses must implement calculate_boundary_conditions!')
	def calculate_inner_domain(self):
		raise NotImplementedError('subclasses must implement calculate_inner_domain!')
	def step_march(self):
		raise NotImplementedError('subclasses must implement step_march!')

		
class FDMEulerImplicit(FDMBase):
	def __init__(self, edp, Xmax, J, T, N):
		FDMBase.__init__(self, edp, Xmax, J, T, N)
		self.calculate_step_sizes()
		self.set_initial_conditions()

	def calculate_step_sizes(self):
		self.dx = self.X/self.J
		self.dt = self.T/self.N

	def set_initial_conditions(self):
		cur_spot = 0.0
		old_result = [0]*(self.J+1)
		new_result = [0]*(self.J+1)
		x_values = [0]*(self.J+1)
		for i in range(0,self.J):
			cur_spot = i*self.dx
			if (cur_spot == self.edp.option.K):
				self.old_result[i] = self.edp.boundary_strike(self.cur_t, cur_spot)
			elif (cur_spot == self.edp.option.payoff.Barrier):
				self.old_result[i] = self.edp.boundary_barrier(self.cur_t, cur_spot)
			else :
				self.old_result[i] = self.edp.init_cond(cur_spot)
			self.x_values[i] = cur_spot
		self.x_values[self.J] = self.X
		self.cur_t = self.T
		self.old_result[self.J] = self.edp.boundary_right(self.cur_t, self.X)
		self.prev_t = self.T
		self.cur_t = self.T


	def calculate_boundary_conditions(self):
		self.new_result[0] = self.edp.boundary_left(self.cur_t, self.x_values[0])
		self.new_result[self.J] = self.edp.boundary_right(self.cur_t, self.x_values[self.J])

	def calculate_inner_domain(self):
		for i in range(1,self.J):
			s2 = self.edp.ds2_coeff(self.cur_t, self.x_values[i])*self.dt/(self.dx*self.dx)
			c = self.edp.zero_coeff(self.cur_t, self.x_values[i])*self.dt
			s = self.edp.ds_coeff(self.cur_t, self.x_values[i])*self.dt/self.dx
			self.alpha = s
			self.beta = 1 - s - 2*s2 + c
			self.gamma = s + s2
			
			self.new_result[i] = self.alpha * self.old_result[i+1] + self.beta*self.old_result[i] + self.gamma * self.old_result[i-1]
			if (self.new_result[i] - self.new_result[i-1] < 0):
				self.new_result[i] = 0.5*self.new_result[i-1] + 0.5*self.new_result[self.J]
			
			
			
	def calculate_inner_domain_with_analytics(self, K, r, sigma, T, analytics):
		for i in range(1,self.J):
			s2 = self.edp.ds2_coeff(self.cur_t, self.x_values[i])*self.dt/(self.dx*self.dx)
			c = self.edp.zero_coeff(self.cur_t, self.x_values[i])*self.dt
			s = self.edp.ds_coeff(self.cur_t, self.x_values[i])*self.dt/self.dx
			self.alpha = s
			self.beta = 1 - s - 2*s2 + c
			self.gamma = s + s2
			
			self.new_result[i] = self.alpha * self.old_result[i+1] + self.beta*self.old_result[i] + self.gamma * self.old_result[i-1]
			if (self.new_result[i] - self.new_result[i-1] < 0) & (analytics == 1):
				d1 = (math.log(self.x_values[i]/K) + (r-sigma*sigma/2)*(T-self.cur_t))/(sigma*math.sqrt(T-self.cur_t))
				d2 = d1 - sigma*math.sqrt(T-self.cur_t)
				self.new_result[i] = self.x_values[i] * math.erf(d1) - K * math.exp(-r*(T-self.cur_t)) * math.erf(d2) 
				
	def step_march_with_analytics(self, K, r , sigma, T, analytics):
		while(self.cur_t > 0):
			self.cur_t = self.prev_t - self.dt
			self.calculate_boundary_conditions()
			self.calculate_inner_domain_with_analytics(K, r, sigma, T, analytics)
			self.old_result = self.new_result
			self.prev_t = self.cur_t
			
	def step_march(self):
		while(self.cur_t > 0):
			self.cur_t = self.prev_t - self.dt
			self.calculate_boundary_conditions()
			self.calculate_inner_domain()
			self.old_result = self.new_result
			self.prev_t = self.cur_t

	def print_price(self):
		for i in range(0,self.J+1):
			print("S: {} Prix: {}",self.x_values[i],self.new_result[i])

	def print_x(self):
		self.cur_t = self.prev_t - self.dt
		self.calculate_boundary_conditions()