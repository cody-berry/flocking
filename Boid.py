

class Boid:
    def __init__(self, x, y):
        self.pos = PVector(x, y)
        self.vel = PVector.random2D().mult(random(1, 2))
        self.acc = PVector.random2D().mult(random(0.1, 0.3))
        self.r = 10
        self.max_speed = 5
        self.max_force = 3
        
        
    def show(self):
        pushMatrix()
        translate(self.pos.x, self.pos.y)
        rotate(self.vel.heading())
        fill(0, 0, 100)
        triangle(0, self.r, -self.r/2, -self.r/2, self.r/2, -self.r/2)
        popMatrix()
        
        
    def update(self):
        self.vel.add(self.acc)
        self.vel.limit(self.max_speed)
        self.pos.add(self.vel)
        self.acc = PVector(0, 0)
        
    
    # Steer in the average direction of nearby boids    
    def alignment(self, boids):
        # a Boid can't see everything!
        perception_radius = 30
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
        circle(self.pos.x, self.pos.y, perception_radius*2)
        
        # Now we can subtract our velocity, because our desired velocity = 
        # difference - current velocity
        steering_force = PVector.sub(average, self.vel)
        steering_force.limit(self.max_force)
        return steering_force
    
    
    # Steer towards nearby boids
    def cohesion(self, boids):
        # a Boid can't see everything!
        perception_radius = 30
        # we should find the average position to find the steering force
        average = PVector(0, 0, 0)
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
                average.add(boid.pos) # we want to find the average position
                
        # the last step of taking the average is dividing by the number of
        # elements, but if total = 0, we're going to get a ZeroDivisionError
        try:
            average.div(total)
        except ZeroDivisionError:
            pass
            
        stroke(210, 90, 100)
        noFill()
        circle(self.pos.x, self.pos.y, perception_radius*2)
        
        # Now we can subtract our velocity, because our desired velocity = 
        # difference - current velocity
        steering_force = PVector.sub(average, self.vel)
        steering_force.sub(self.pos)
        steering_force.limit(self.max_force)
        pushMatrix()
        translate(self.pos.x, self.pos.y)
        line(0, 0, steering_force.x, steering_force.y)
        popMatrix()
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
        cohesion = self.cohesion(boids)
        self.acc.add(cohesion)
        
