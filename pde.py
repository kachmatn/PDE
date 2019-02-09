import os
import math
from payoff import *

class DiffusionPDE:
	 #PDE Coeff
	def dt_coeff(self, t,x) :
		raise NotImplementedError('subclasses must implement dt_coeff!')
	def ds_coeff(self, t,x) :
		raise NotImplementedError('subclasses must implement ds_coeff!')
	def ds2_coeff(self, t,x) :
		raise NotImplementedError('subclasses must implement ds2_coeff!')
	def zero_coeff(self, t,x) :
		raise NotImplementedError('subclasses must implement zero_coeff!')
	def source_coeff(self, t,x) :
		raise NotImplementedError('subclasses must implement source_coeff!')
	# Boundary and initial conditions
	def boundary_left(self, t,x):
		return self.option.payoff.boundary_left(t , x)
	def boundary_right(self, t,x):
		return self.option.payoff.boundary_right(t , x)
	def boundary_strike(self, t, x):
		return self.option.payoff.boundary_strike(t , x)
	def boundary_barrier(self, t, x):
		return self.option.payoff.boundary_barrier(t , x)
	def init_cond(self, x):
		return self.option.payoff.evaluate(x)	

class BlackScholesPDE(DiffusionPDE):
	def __init__(self, vanillaOption):
		self.option = vanillaOption
	def dt_coeff(self, t, x) :
		return 1
	def ds_coeff(self, t, x) :
		return self.option.r * x
	def ds2_coeff(self, t, x) :
		return 0.5*self.option.sigma*self.option.sigma*x*x
	def zero_coeff(self, t,x ) :
		return -self.option.r
	def source_coeff(self, t, x ) :
		return 0

class logPDE(DiffusionPDE):
	def __init__(self, vanillaOption):
		self.option = vanillaOption
	def dt_coeff(self, t, x) :
		return 1
	def ds_coeff(self, t, x) :
		return self.option.r - 0.5*self.option.sigma*self.option.sigma
	def ds2_coeff(self, t, x) :
		return 0.5*self.option.sigma*self.option.sigma
	def zero_coeff(self, t,x ) :
		return -self.option.r
	def source_coeff(self, t, x ) :
		return 0