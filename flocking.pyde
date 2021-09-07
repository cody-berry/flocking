# Cody
# August 30, 2021
# Flocking simulation
# Coding Challenge #124 —— Daniel Shiffman
# Boid rules:
#     Separation: Steering to avoid crowding other boids
#     Alignment: Steer in the average direction of nearby boids
#     Cohesion: Steer towards nearby boids
#     Obsticle Avoidance: Get away from obsticles
#
# v0.01 - Create the Boid class
# v0.02 - Alignment
# v0.03 - Cohesion
# v0.04 - Separation
# v0.05 - Seek
# v0.06 - Seek velocity
# v0.0  - Hack bot
# v0.1  - 3D
# v0.1  - Adjustible obstacles
# v0.1  - Target
# v0.1  - Auto-obstacle
# v0.1  - Auto-target
# v0.   - Obstacle Avoidance <- where does this go? I need to see when I create
#                               my Obsticle Path repository.

from Boid import *
from Quadtree import *
from Rectangle import *
from Point import *

def setup():
    global boids, qt, points
    colorMode(HSB, 360, 100, 100, 100)
    size(640, 360)
    boids = []
    points = []
    boundary = Rectangle(0, 0, width, height)
    qt = Quadtree(boundary, 4)
    frameRate(600)
    for i in range(150):
        x = random(width)
        y = random(height)
        b = Boid(x, y)
        p = Point(x, y, b)
        boids.append(Boid(random(width), random(height)))
        qt.insert(p)
  
      
def draw():
    global boids, qt, points
    qt = Quadtree(Rectangle(0, 0, width, height), 4)
    background(210, 80, 32)
    fill(0, 0, 100)
    # If we do just alignment, if the force is too strong, since the boids
    # depend on all of the other boids, some of the depended ones updated and 
    # others not updated, resulting in the boids just going in circles.
    
    
    
    for i in range(len(boids)):
        b = boids[i]
        p = Point(b.pos.x, b.pos.y, b)
        qt.insert(p)
        
    qt.show()    
    
    mouse = PVector(mouseX, mouseY)
    fill(90, 100, 100, 50)
    
    for boid in boids:
        # now that we have a quadtree, we can find all of the points in the 
        # quadtree
        perception_radius = 15
        qt_query = qt.query(Rectangle(boid.pos.x - perception_radius,
                                      boid.pos.y - perception_radius, 
                                      perception_radius*2, 
                                      perception_radius*2))
        queried_boids = []
        for p in qt_query:
            queried_boids.append(p.data)
        boid.flock(queried_boids)
        # boid.acc.add(boid.seek(mouse))
        boid.update()
        boid.edges()
        # boid.acc.add(PVector.random2D().mult(random(0.1, 0.3)))
        
    for boid in boids:
        fill(0, 0, 100)
        boid.show()
    
    s = "FPS: {}".format(frameRate)
    fill(0, 0, 100, 30)
    stroke(0, 0, 100)
    rect(40, 55, textWidth(s)+20, -32, 5)
    textSize(24)
    fill(0, 0, 100)
    text(s, 50, 50)
    
    
    
    
    
    
    
        
    
