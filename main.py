import os
from payoff import *
from pde import *
from fdm import *

def getMarketParameter():
	k = 0
	r = 0
	sigma = 0
	T = 0
	while True:
		try:
			y = input("Strike : ")
			k = float(y)
			y = input("Interest Rate : ")
			r = float(y)
			y = input("Volatility : ")
			sigma = float(y)
			y = input("Maturity : ")
			T = float(y)
		except ValueError as e:
			print("Vous devez saisir un double. Exception getMarketParameter invalid type of parameter")
			continue
		else:
			break
	return k,r,sigma,T

def getSchemeParameter():
	X = 0
	J = 0
	N = 0
	while True:
		try:
			y = input("Xmax : ")
			X = float(y)
			y = input("Space : ")
			J = int(y)
			y = input("Time : ")
			N = float(y)
			y = input("Inject Analytics [0/1] : ")
			analytics = int(y)
		except ValueError as e:
			print("Vous devez saisir un double/int. Exception getMarketParameter invalid type of parameter")
			continue
		else:
			break
	return X,J,N,analytics

if __name__ == "__main__":
	print("Bienvenue dans le pricer EDP")
	continuer = True
	reponse = ""
	while (continuer) :
		K,r,sigma,T = getMarketParameter()
		print(T)
		X,J,N,analytics = getSchemeParameter()
		#Option Types
		print("1 - Call")
		print("2 - CallSpread")
		answerOption = input("OptionType : ")
		optionType = int(answerOption)
		if (optionType == 1):
			c = Call(K, r, T, 9999, 99)
		if (optionType == 2):
			answerOption = input("Barrier level : ")
			Barrier = float(answerOption)
			answerOption = input("Spread level : ")
			Spread = float(answerOption)
			c = CallSpread(K,Barrier, Spread)
			
		vo = VanillaOption(K,r,sigma,T,c)
		edp = BlackScholesPDE(vo)
		print("###TEST###")
		euler = FDMEulerImplicit(edp,X,J,T,N)
		euler.step_march_with_analytics(K, r, sigma, T, 1)
		euler.print_price()
		reponse = input("Voulez-vous pricer un autre produit ? [O/N]")
		if (reponse == "N") :
			continuer = False