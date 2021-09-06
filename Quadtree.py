

from Rectangle import *


class Quadtree:
    def __init__(self, boundary, point_cap): # boundary is a Rectangle
        self.boundary = boundary
        self.point_cap = point_cap
        self.points = []
        self.divided = False
        
    
    def intersects(self, r):
        b = self.boundary
        return not (b.x > r.x + r.w or 
                   r.x > b.x + b.w or 
                   r.y > b.y + b.h or
                   b.y > r.y + r.h)
    
    
    def subdivide(self):
        b = self.boundary
        # northwest
        nw = Rectangle(b.x, b.y, b.w/2.0, b.h/2.0)
        self.northwest = Quadtree(nw, self.point_cap)
        # northeast
        ne = Rectangle(b.x + b.w/2.0, b.y, b.w/2.0, b.h/2.0)
        self.northeast = Quadtree(ne, self.point_cap)
        # southwest
        sw = Rectangle(b.x, b.y + b.h/2.0, b.w/2.0, b.h/2.0)
        self.southwest = Quadtree(sw, self.point_cap)
        # southeast
        se = Rectangle(b.x + b.w/2.0, b.y + b.h/2.0, b.w/2.0, b.h/2.0)
        self.southeast = Quadtree(se, self.point_cap)
        # We've divided! Now we can say that this quadtree has divided, and say that the others
        # have not (set in the constructor).
        self.divided = True
        
    
    def insert(self, p):
        # If you look at the code after "Spoilers from Daniel's code!", we only want to insert
        # so that only 1 of them gains it.
        if not self.boundary.contains(p):
            return False
        
        
        # Success! We can add a point as long as the quadtree rectangle boundary is not full.
        if len(self.points) < self.point_cap:
            self.points.append(p)
            return True
        
        
        # Oh no! Our quadtree boundary rectangle is full. We need to split up and give the point
        # to whichever point owns it. If it is somwhere near the edge or corner, the priority 
        # queue is from most important to least important: [nw, ne, sw, se], where nw stands for
        # northwest, ne stands for northeast, sw stands for southwest, and se stands for southeast.    
        else:
            if not self.divided:
                self.subdivide()
            # Spoilers from Daniel's code!
            if self.northwest.insert(p):
                return True
            if self.northeast.insert(p):
                return True
            if self.southwest.insert(p):
                return True
            if self.southeast.insert(p):
                return True
            
            
    def show(self):
        noFill()
        stroke(0, 0, 100, 100)
        strokeWeight(1)
        b = self.boundary
        rect(b.x, b.y, b.w, b.h)
        # We also want to show all of our children!
        if self.divided:
            self.northwest.show()
            self.northeast.show()
            self.southwest.show()
            self.southeast.show()
    
                    
    # def __repr__(self):
    #     if self.divided:
    #         return "Self contents: I have {} points. Northwest contents: {} Northeast contents: {} Southwest contents: {} Southeast contents: {}".format(len(self.points), self.northwest, self.northeast, self.southwest, self.southeast)
    #     else:
    #         return "I have {} points.".format(len(self.points))
    
    
    # The total number of points inserted is what this function gives.
    def count(self):
        total = len(self.points)
        if self.divided:
            total += self.northwest.count()
            total += self.northeast.count()
            total += self.southwest.count()
            total += self.southeast.count()
            
        return total
    
    
    def query(self, r):
        found = []        
        if not self.intersects(r):
            return found
        
        for p in self.points:
            if r.contains(p):
                found.append(p)
                
        
        # If we just queried ourselves, we would leave our children unchecked and left apart, 
        # while we want to do it for all of us.        
        if self.divided:
            found += self.northwest.query(r)
            found += self.northeast.query(r)
            found += self.southwest.query(r)
            found += self.southeast.query(r)
            
            
        return found
    
    
    def reset_points(self):
        self.points = []
        if self.divided:
            self.northwest.reset_points()
            self.southwest.reset_points()
            self.northeast.reset_points()
            self.southeast.reset_points()
