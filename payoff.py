import os
import math

class Payoff:
	def __init__(self, pK, pB, pS):
		self.K = pK
		self.Barrier = pB
		self.Spread = pS
	def evaluate(self, x):
		raise NotImplementedError('subclasses must implement evaluate!')
	def boundary_left(self, t, x):
		raise NotImplementedError('subclasses must implement boundary_left!')
	def boundary_right(self, t,x ) :
		raise NotImplementedError('subclasses must implement boundary_right!')
	def boundary_strike(self, t, x):
			raise NotImplementedError('subclasses must implement boundary_strike!')
	def boundary_barrier(self, t, x):
			raise NotImplementedError('subclasses must implement boundary_barrier!')
		
class Call(Payoff):
	def __init__(self, pK, pr, pT, pB, pS):
		Payoff.__init__(self, pK, pB, pS)
		self.r = pr
		self.T = pT
		
	def evaluate(self, x):
		if (x < self.K):
			return 0
		else:
			return x - self.K
			
	def boundary_left(self, t, x):
		return 0
	def boundary_right(self, t, x) :
		return x - self.K #return abs((x - self.K*math.exp(-self.r*(self.T-t))))	
	def boundary_strike(self, t, x):
		return x - self.K
	def boundary_barrier(self, t, x):
		return x - self.K
class CallSpread(Payoff):
	def __init__(self, pK, pB, pS):
		Payoff.__init__(self, pK, pB, pS)
		
	def evaluate (self, x):
		if (x >self.K) & (x >= self.Barrier + self.Spread):
			return abs(self.Spread)
		if (x > self.K) & (x >= self.Barrier) & (x < self.Barrier + self.Spread):
			return x - self.K
		else:
			return 0
			
	def boundary_left(self, t, x):
		return 0
	def boundary_strike(self, t, x):
		return x - self.K
	def boundary_barrier(self, t, x):
		return abs(self.Spread)
	def boundary_right(self, t, x):
		return 0
		
class VanillaOption:
	def __init__(self, pk, pr, pSigma, pT, payoff):
		self.K = pk
		self.r = pr
		self.sigma = pSigma
		self.T = pT
		self.payoff = payoff
