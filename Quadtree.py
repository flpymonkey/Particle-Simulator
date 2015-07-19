import pygame
import math

displayTree = False #Display quadtree in background if True

def rect_quad_split(rect):
    w=rect.width/2.0
    h=rect.height/2.0
    rl=[]
    rl.append(pygame.Rect(rect.left, rect.top, w, h))
    rl.append(pygame.Rect(rect.left+w, rect.top, w, h))
    rl.append(pygame.Rect(rect.left, rect.top+h, w, h))
    rl.append(pygame.Rect(rect.left+w, rect.top+h, w, h))
    return rl

def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        angle = math.atan2(dy, dx) + 0.5 * math.pi
        total_mass = p1.mass + p2.mass
        overlap = 0.5*(p1.size + p2.size - dist+1)
        if p1.get_moveable():
            (p1.angle, p1.speed) = addVectors(p1.angle, p1.speed*(p1.mass-p2.mass)/total_mass, angle, 2*p2.speed*p2.mass/total_mass)
            p1.speed *= p1.elasticity
            p1.x += math.sin(angle)*overlap
            p1.y -= math.cos(angle)*overlap
        
        if p2.get_moveable():
            (p2.angle, p2.speed) = addVectors(p2.angle, p2.speed*(p2.mass-p1.mass)/total_mass, angle+math.pi, 2*p1.speed*p1.mass/total_mass)
            p2.speed *= p2.elasticity
            p2.x -= math.sin(angle)*overlap
            p2.y += math.cos(angle)*overlap

def addVectors(angle1, length1, angle2, length2):
    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    
    angle = 0.5 * math.pi - math.atan2(y, x)
    length  = math.hypot(x, y)

    return (angle, length)

class Quadtree(object):
    def __init__(self, level, rect, particles=[], color = (0,0,0)):
        '''A quad tree class that recursively subdivides to create subbranches for collision detection
        level: the level of subdivision that the branch is created on (0 for original branch)
        rect: a pygame Rect object that represents the portion of the screen the branch covers
        particles: list of Particle object instances that determine subdivision
        color: the color of the quadtree (if displayTree == True'''
        
        self.maxlevel = 4#max level of subdivision
        self.level = level
        self.maxparticles = 3#minimum number of particles without subdivision
        self.rect = rect
        self.particles = particles
        self.color = color
        self.branches = []

    def get_rect(self):
        return self.rect

    def subdivide(self):
        for rect in rect_quad_split(self.rect):
            branch = Quadtree(self.level+1, rect, [], (self.color[0]+30,self.color[1],self.color[2]))
            self.branches.append(branch)
    
    def add_particle(self, particle):
        self.particles.append(particle)

    def subdivide_particles(self):
        for particle in self.particles:
            for branch in self.branches:
                if branch.get_rect().colliderect(particle.get_rect()):
                    branch.add_particle(particle)

    def render(self, display):
        pygame.draw.rect(display, self.color, self.rect)

    def test_collisions(self):
        for i, particle in enumerate(self.particles):
            for particle2 in self.particles[i+1:]:
                collide(particle, particle2)
        
        

    def update(self, display):
        '''tests for subdivisions of branches and collision of particles
        if displayTree == True the quadtree will be displayed behind particle simulation'''
        if len(self.particles) > self.maxparticles and self.level <= self.maxlevel:
            self.subdivide()
            self.subdivide_particles()
            for branch in self.branches:
                branch.update(display)
        else:
            self.test_collisions()
            if displayTree:
                self.render(display)
        
            
            
        
        
        
                
                
        
