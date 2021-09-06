class Point:
    def __init__(self, x, y, userData):
        self.x = x
        self.y = y
        self.data = userData
        
    def __repr__(self):
        return "({}, {})".format(self.x, self.y)
