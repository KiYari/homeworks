class BaseObject:

    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def get_coordinates(self):
        return self.x, self.y, self.z


class Block(BaseObject):

    def shatter(self):
        self.x, self.y, self.z = None, None, None


class Entity(BaseObject):

    def move(self, x, y, z):
        self.x, self.y, self.z = x, y, z


class Thing(BaseObject):
    pass


block = Block(1, 2, 3)
print(block.get_coordinates())
block.shatter()
print(block.get_coordinates())

entity = Entity(200, 100, 100)
print(entity.get_coordinates())
entity.move(205, 300, 400)
print(entity.get_coordinates())
