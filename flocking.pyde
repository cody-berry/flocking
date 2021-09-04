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
# v0.0  - Separation
# v0.0  - Seek
# v0.0  - Hack bot
# v0.1  - 3D
# v0.1  - Adjustible obstacles
# v0.1  - Target
# v0.1  - Auto-obstacle
# v0.1  - Auto-target
# v0.   - Obstacle Avoidance <- where does this go? I need to see when I create
#                               my Obsticle Path repository.

from Boid import *


def setup():
    global boids
    colorMode(HSB, 360, 100, 100, 100)
    size(600, 600)
    boids = []
    for i in range(100):
        boids.append(Boid(random(width), random(height)))
  
      
def draw():
    global boids
    background(210, 80, 32)
    fill(0, 0, 100)
    # If we do just alignment, if the force is too strong, since the boids
    # depend on all of the other boids, some of the depended ones updated and 
    # others not updated, resulting in the boids just going in circles.
    
    mouse = PVector(mouseX, mouseY)
    fill(90, 100, 100, 50)
    circle(mouse.x, mouse.y, 16)
    
    for boid in boids:
        # boid.flock(boids)
        boid.acc.add(boid.seek(mouse))
        boid.update()
        boid.edges()
        # boid.acc.add(PVector.random2D().mult(random(0.1, 0.3)))
        
    for boid in boids:
        fill(0, 0, 100)
        boid.show()
    
    s = "FPS: {:.0f}".format(frameRate)
    fill(0, 0, 100, 30)
    stroke(0, 0, 100)
    rect(40, 55, textWidth(s)+20, -32, 5)
    textSize(24)
    fill(0, 0, 100)
    text(s, 50, 50)
        
    
