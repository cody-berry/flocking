

class Boid:
    def __init__(self, x, y):
        self.pos = PVector(x, y)
        self.vel = PVector.random2D().mult(random(0.1, 0.3))
        self.acc = PVector.random2D().mult(random(0.1, 0.3))
        self.r = 8
        
        
    def show(self):
        fill(0, 0, 100)
        circle(self.pos.x, self.pos.y, self.r)
        
        
    def update(self):
        self.vel.add(self.acc)
        self.pos.add(self.vel)
        self.acc = PVector(0, 0)
