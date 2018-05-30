from .polynomial import Polynomial

class GaloisField:
	def __init__(self, prime, power, coef, modcoef):
		self.poly = Polynomial(prime, coef)
		self.prime = prime
		self.power = power
		self.order = prime ** power
		self.modulo = Polynomial(prime, modcoef)
		while self.modulo.degree > power:
			self.modulo.decrement_degree()
		self.poly.mod(self.modulo)

	def copy(self):
		return GaloisField(self.prime, self.power, self.poly.coef, self.modulo.coef)

	def generate(self):
		self.poly.generate(self.power)

	def add(self, other):
		self.poly.add(other.poly)

	def multiply(self, other):
		self.poly.multiply(other.poly)
		self.poly.mod(self.modulo)

	def powerr(self, k):
		k %= self.order
		if k == 1:
			return
		tmp = self.copy()
		self.poly.coef = [1]
		self.poly.degree = 0
		while k > 0:
			if (k&1) == 1:
				self.multiply(tmp)
			tmp.multiply(tmp)
			k >>= 1

	def print(self):
		self.poly.print()