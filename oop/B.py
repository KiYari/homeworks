class MyVector:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __add__(self, other):
        return MyVector(self.a + other.a, self.b + other.b)

    def __sub__(self, other):
        return MyVector(self.a - other.a, self.b - other.b)

    def __eq__(self, other):
        return (self.a == other.a) and (self.b == other.b)

    def __ne__(self, other):
        return (self.a != other.a) or (self.b != other.b)

    def __len__(self):
        return int((self.a ** 2 + self.b ** 2) ** 0.5)

    def __mul__(self, other):
        if type(other) == int:
            return MyVector(self.a * other, self.b * other)
        else:
            return self.a * other.a + self.b * other.b

    def __str__(self):
        return 'MyVector({},{})'.format(self.a, self.b)


v1 = MyVector(-2, 5)
v2 = MyVector(3, -4)
v3 = MyVector(-2, 5)
v_sum = v1 + v2
print(v_sum)
print(v1 - v2)
print(v1 == v3)
print(v1 != v3)
print(len(v1))
print(v1 * v2)
v1 *= 5
print(v1)
