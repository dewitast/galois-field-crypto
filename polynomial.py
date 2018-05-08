from .utils import invmod

class Polynomial:
	def __init__(self, modulo, coef = [0]):
		self.modulo = modulo
		self.coef = [x % modulo for x in coef]
		self.truncate()

	def copy(self):
		return Polynomial(self.modulo, self.coef)

	def truncate(self):
		while len(self.coef)>1 and self.coef[-1] == 0:
			del self.coef[-1]
		self.degree = len(self.coef) - 1

	def decrement_degree(self):
		self.degree -= 1
		del self.coef[-1]

	def shift(self):
		if self.coef[-1] > 0:
			self.degree += 1
			self.coef.insert(0, 0)

	def add(self, pol):
		degree = max(self.degree, pol.degree)
		self.coef += [0 for _ in range(degree - self.degree)]
		pol.coef += [0 for _ in range(degree - pol.degree)]
		self.coef = [(self.coef[i] + pol.coef[i]) % self.modulo for i in range(degree + 1)]
		self.degree = degree
		self.truncate()
		pol.truncate()

	def power(self, k):
		if k == 1:
			return
		tmp = self.copy()
		self.coef = [0]
		self.degree = 0
		while k > 0:
			if (k&1) == 1:
				self.add(tmp)
			tmp.add(tmp)
			k >>= 1

	def subtract(self, pol):
		degree = max(self.degree, pol.degree)
		self.coef += [0 for _ in range(degree - self.degree)]
		pol.coef += [0 for _ in range(degree - pol.degree)]
		self.coef = [(self.coef[i] - pol.coef[i] + self.modulo) % self.modulo for i in range(degree + 1)]
		self.degree = degree
		self.truncate()
		pol.truncate()

	def multiply(self, pol):
		degree = self.degree + pol.degree
		coef = [0 for _ in range(degree + 1)]
		for i in range(self.degree + 1):
			for j in range(pol.degree + 1):
				coef[i + j] += (self.coef[i] * pol.coef[j]) % self.modulo
				coef[i + j] %= self.modulo
		self.coef = coef[:]
		self.degree = degree

	def mod(self, pol):
		if self.degree < pol.degree:
			return
		res = Polynomial(self.modulo, [self.coef[i] for i in range(pol.degree)])
		base = Polynomial(self.modulo)
		cpol = pol.copy()
		cpol.power(invmod(cpol.coef[-1], self.modulo))
		cpol.decrement_degree()
		base.subtract(cpol)
		if self.coef[pol.degree] > 0:
			base.power(self.coef[pol.degree])
			res.add(base)
			base.power(invmod(self.coef[pol.degree], self.modulo))
		md = Polynomial(self.modulo, base.coef)
		for i in range(pol.degree + 1, self.degree + 1):
			md.shift()
			if md.degree == pol.degree:
				k = md.coef[-1]
				md.decrement_degree()
				base.power(k)
				md.add(base)
				base.power(invmod(k, self.modulo))
			if self.coef[i] > 0:
				md.power(self.coef[i])
				res.add(md)
				md.power(invmod(self.coef[i], self.modulo))
		self.coef = res.coef[:]
		self.degree = res.degree

	def print(self):
		string = ''
		for i in range(self.degree + 1):
			tmp = str(self.coef[i])
			if i>0:
				tmp += 'x^' + str(i)
			if i < self.degree:
				tmp += ' + '
			string += tmp
		print(string)