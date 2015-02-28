import pygame

def rect_quad_split(rect):
    w=rect.width/2.0
    h=rect.height/2.0
    rl=[]
    rl.append(pygame.Rect(rect.left, rect.top, w, h))
    rl.append(pygame.Rect(rect.left+w, rect.top, w, h))
    rl.append(pygame.Rect(rect.left, rect.top+h, w, h))
    rl.append(pygame.Rect(rect.left+w, rect.top+h, w, h))
    return rl

class Quadtree(object):
    def __init__(self, level, rect, particles=[], color = (0,0,0)):
        self.maxlevel = 6
        self.level = level
        self.maxparticles = 0
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
        

    def update(self, display):
        if len(self.particles) > self.maxparticles and self.level <= self.maxlevel:
            self.subdivide()
            self.subdivide_particles()
            for branch in self.branches:
                branch.update(display)
        else:
            self.render(display)
        
            
            
        
        
        
                
                
        
