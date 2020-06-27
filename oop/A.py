class Balance:

    def __init__(self):
        self.right = 0
        self.left = 0

    def add_right(self, n):
        self.right += n

    def add_left(self, n):
        self.left += n

    def result(self):
        if self.left == self.right:
            return '='
        elif self.left > self.right:
            return 'L'
        else:
            return 'R'


balance = Balance()
balance.add_right(10)
balance.add_left(9)
balance.add_left(2)
print(balance.result())

balance = Balance()
balance.add_right(10)
balance.add_left(5)
balance.add_left(5)
print(balance.result())

balance.add_right(1)
print(balance.result())
