

class Boid:
    def __init__(self, x, y):
        self.pos = PVector(x, y)
        self.vel = PVector().random2D().mult(random(1, 5))
        self.acc = PVector(0, 0)
        self.r = 8
        self.max_speed = 10
        self.max_force = 0.1
        
        
    def show(self):
        fill(0, 0, 100)
        circle(self.pos.x, self.pos.y, self.r*2)
        
        
    def update(self):
        self.vel.add(self.acc)
        self.vel.limit(self.max_speed)
        self.pos.add(self.vel)
        self.acc = PVector(0, 0)
        
    
    # Steer in the average direction of nearby boids    
    def alignment(self, boids):
        # a Boid can't see everything!
        perception_radius = 20
        # we should find the average direction to find the steering force
        average = PVector(0, 0)
        # total is the number of boids we find
        total = 0
        # iterate through the boids
        for boid in boids:
            # We don't want to do anything unless our boid is a boid inside
            # a circle centered at us with a radius of perception_radius!
            # Also, we don't want to use us as a boid.
            d = dist(self.pos.x, self.pos.y, boid.pos.x, boid.pos.y)
            if boid != self and d < perception_radius:
                # This means we've found a boid!
                total += 1
                # We can update our average
                average.add(boid.vel) # we want to find the average direction
                
        # the last step of taking the average is dividing by the number of
        # elements, but if total = 0, we're going to get a ZeroDivisionError
        try:
            average.div(total)
        except:
            average = self.vel
            
        stroke(210, 90, 100)
        noFill()
        circle(self.pos.x, self.pos.y, perception_radius)
        
        # Now we can subtract our velocity, because our desired velocity = 
        # difference - current velocity
        steering_force = PVector.sub(average, self.vel)
        steering_force.limit(self.max_force)
        return steering_force
    
    
    # what if the boids go off the screen? We'll lose a pack though. The pack will
    # continue to go on though.
    def edges(self):
        if self.pos.x + self.r > width: # right edge
            self.pos.x = self.r
        if self.pos.x - self.r < 0: # left edge
            self.pos.x = width - self.r
            
        if self.pos.y - self.r < 0: # top edge
            self.pos.y = height - self.r
        if self.pos.y + self.r > height: # bottom edge
            self.pos.y = self.r
                    
            
    def flock(self, boids):
        alignment = self.alignment(boids)
        self.acc.add(alignment)
        
