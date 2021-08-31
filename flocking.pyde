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
# v0.0  - Create the Boid class
# v0.0  - Alignment
# v0.0  - Cohesion
# v0.0  - Separation
# v0.0  - Obstacle Avoidance
# v0.0  - Quadtree
# v0.0  - Hack bot
# v0.1  - 3D
# v0.1  - Adjustible obstacles
# v0.1  - Target
# v0.1  - Auto-obstacle
# v0.1  - Auto-target

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
    # If we do just alignment, if the force is too strong, since the boids
    # depend on all of the other boids, some of the depended ones updated and 
    # others not updated, resulting in the boids just going in circles.
    for boid in boids:
        boid.update()
        # boid.acc.add(PVector.random2D().mult(random(0.1, 0.3)))
        
    for boid in boids:
        boid.show()
