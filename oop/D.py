class Polynomial:

    def __init__(self, coefficients):
        self.coefficients = coefficients[::]

    def __call__(self, x):
        return sum([self.coefficients[i] * x ** i for i in range(len(self.coefficients))])

    def __add__(self, other):
        if len(self.coefficients) > len(other.coefficients):
            while len(self.coefficients) > len(other.coefficients):
                other.coefficients.append(0)
        else:
            while len(self.coefficients) < len(other.coefficients):
                self.coefficients.append(0)
        return Polynomial([self.coefficients[i] + other.coefficients[i] for i in range(len(self.coefficients))])


poly = Polynomial([10, -1])
print(poly(0))
print(poly(1))
print(poly(2))

poly1 = Polynomial([0, 1])
poly2 = Polynomial([10])
poly3 = poly1 + poly2
poly4 = poly2 + poly1

print(poly3(-2), poly4(-2))
print(poly3(-1), poly4(-1))
print(poly3(0), poly4(0))
print(poly3(1), poly4(1))
print(poly3(2), poly4(2))

