

class Boid:
    def __init__(self, x, y):
        self.pos = PVector(x, y)
        self.vel = PVector.random2D().mult(random(1, 2))
        self.acc = PVector.random2D().mult(random(0.1, 0.3))
        self.r = 10
        self.max_speed = 4
        self.max_force = .2
        
        
    def show(self):
        pushMatrix()
        translate(self.pos.x, self.pos.y)
        rotate(self.vel.heading())
        fill(0, 0, 100)
        triangle(self.r, 0, -self.r/2, -self.r/2, -self.r/2, self.r/2)
        popMatrix()
        
        
    def update(self):
        self.vel.add(self.acc)
        # we don't want our velocity to go over max speed
        self.vel.limit(self.max_speed)
        self.pos.add(self.vel)
        self.acc = PVector(0, 0)
        
    
    # A good way for getting to a target from far away quickly. 
    # This algorithm is based on Creg Renold's paper. 
    # steering = desired - current, kind of like error correction
    # What happens if the target is too close? The boid will overshoot,
    # and it will continue going on forever.
    def seek(self, target):
        distance = PVector.sub(target, self.pos)
        
        # our desired velocity is that set to our max speed
        desired = distance.setMag(self.max_speed)
        # steering = desired - current
        steering_force = PVector.sub(desired, self.vel)
        # we need to make sure we don't apply too much force
        steering_force.limit(self.max_force)
        return steering_force
        
    
    # Steer in the average direction of nearby boids    
    def alignment(self, boids):
        # a Boid can't see everything!
        perception_radius = 40
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
            stroke(210, 90, 100)
            noFill()
            circle(self.pos.x, self.pos.y, perception_radius*2)
        
            # Now we can subtract our velocity, because our desired velocity = 
            # difference - current velocity
            steering_force = average
            steering_force.setMag(self.max_speed)
            steering_force.sub(self.vel)
            steering_force.limit(self.max_force)
            return steering_force
        except:
            return average
            
       
    
    
    # Steer towards nearby boids
    def cohesion(self, boids):
        # a Boid can't see everything!
        perception_radius = 40
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
            stroke(210, 90, 100)
            noFill()
            circle(self.pos.x, self.pos.y, perception_radius*2)
            
            # Now we can subtract our velocity, because our desired velocity = 
            # difference - current velocity
            steering_force = average
            
            steering_force.sub(self.pos) # TODO: Figure our why you subtract position
            steering_force.setMag(self.max_speed)
            steering_force = PVector.sub(average, self.vel)
            steering_force.limit(self.max_force)
            pushMatrix()
            translate(self.pos.x, self.pos.y)
            line(0, 0, steering_force.x, steering_force.y)
            popMatrix()
            return steering_force
        except ZeroDivisionError:
            return average
            
        
    
    
    # Steering to avoid crowding other boids
    def seperation(self, boids):
        perception_radius = 30
        total = 0
        average = PVector(0, 0) # this is our desired velocity
        
        # find the average of the positions of all the boids
        for boid in boids:
            distance = PVector.dist(self.pos, boid.pos)
            
            # only calculate within a desired perception radius
            if boid != self and distance < perception_radius:
                difference = PVector.sub(self.pos, boid.pos)
                # we want this difference to be inversely proportional to the distance between
                # self and other; the further away it is, the lower the magnitude we want
                
                # TODO: fix zero division error
                difference.div(distance)
                
                total += 1 # count how many are within our radius to divide later for average
                
                # in self.align, we added the other boids' velocities. here we add position!
                average.add(difference)                
        
        steering_force = average
        
        if total > 0:
            steering_force.div(total) # this is our desired velocity!
             
            steering_force.setMag(self.max_speed)
            steering_force.sub(self.vel)
            steering_force.limit(self.max_force).mult(1.5)
            
            
        # # note that if we didn't find anything, we return the zero vector
        # return PVector(0, 0)
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
        # alignment
        alignment = self.alignment(boids).mult(1)
        self.acc.add(alignment)
        # cohesion
        cohesion = self.cohesion(boids).mult(1)
        self.acc.add(cohesion)
        # seperation
        seperation = self.seperation(boids).mult(3)
        self.acc.add(seperation)
        
