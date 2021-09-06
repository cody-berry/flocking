class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    
    def contains(self, p):
        b = self
        return p.x <= b.x + b.w and p.x >= b.x and p.y <= b.y + b.h and p.y >= b.y
    
    
    def __repr__(self):
        return "I'm a Rectangle with coordinates of ({}, {}), a width of {}, and a height of {}.".format(self.x, self.y, self.w, self.h)
        
