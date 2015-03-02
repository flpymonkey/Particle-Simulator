'''This script is testing mass, particle centered gravity(left click),
density(darker blue means higher density), input amount of gravity('f' key'),
and quadtree collision system'''
import pygame, random, math

from pygame.locals import *
from Quadtreetest import *

WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
AQUA = (0, 255, 255)#CYAN
BLACK = (0, 0, 0)
FUCHSIA = (255, 0, 255)
GRAY = (128, 128, 128)
LIME = (0, 255, 0)
MAROON = (128, 0, 0)
NAVYBLUE = (0, 0, 128)
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
SILVER = (192, 192, 192)
TEAL = (0, 128, 128)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
CYAN = (0, 255, 255) #AQUA
HOTPINK = (255, 105, 180)

pygame.init()

background_colour = (0,0,0)
(width, height) = (1400, 800)
gameFont = pygame.font.Font(None, 20)
particleFont = pygame.font.Font(None, 20)
FPS = 30
FPSCLOCK = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Particle Simulator')

number_of_particles = 1000 #Number of particles when simulation begins
particleSize = (3, 8) #Range of particle size
mass_of_air = 0.02 #Mass of air (higher value means more air resistance)
gravity = [math.pi, 0.008] #gravity angle and magnitude
speedNum = False #If True, particle speeds appear near particles (Pixles per frame)

def displaymenu():
    menu = True
    menucolour = [0, 0, 0]
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print ('add quit stuff')#add quit------------------------------------
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouseLB,mouseMB,mouseRB) = pygame.mouse.get_pressed()
                (mouseX, mouseY) = pygame.mouse.get_pos()
                if mouseRB:
                    menu = False
                else:
                    selected_particle = findParticle(my_particles, mouseX, mouseY)
        menucolour = adjustcolour(menucolour, 0, 0, random.randint(1,5))
        pygame.draw.rect(screen, menucolour, menupos)
        FPSCLOCK.tick(FPS)
        pygame.display.update()

def createParticle(x = None, y = None):
    size = random.randint(particleSize[0], particleSize[1])
    density = random.randint(1, 20)
    if x == None or y == None:
        x = random.randint(size, width-size)
        y = random.randint(size, height-size)
    particle = Particle((x, y), size, density)#start color%%%
    particle.speed = random.random()
    particle.angle = random.uniform(0, math.pi*2)

    my_particles.append(particle)

def addVectors((angle1, length1), (angle2, length2)):
    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    
    angle = 0.5 * math.pi - math.atan2(y, x)
    length  = math.hypot(x, y)

    return (angle, length)

def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None

def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        angle = math.atan2(dy, dx) + 0.5 * math.pi
        total_mass = p1.mass + p2.mass
        (p1.angle, p1.speed) = addVectors((p1.angle, p1.speed*(p1.mass-p2.mass)/total_mass), (angle, 2*p2.speed*p2.mass/total_mass))
        (p2.angle, p2.speed) = addVectors((p2.angle, p2.speed*(p2.mass-p1.mass)/total_mass), (angle+math.pi, 2*p1.speed*p1.mass/total_mass))
        p1.speed *= elasticity
        p2.speed *= elasticity
        self.elasticity = 0.75 #Percent of speed remaining after a collision
        overlap = 0.5*(p1.size + p2.size - dist+1)
        p1.x += math.sin(angle)*overlap
        p1.y -= math.cos(angle)*overlap
        p2.x -= math.sin(angle)*overlap
        p2.y += math.cos(angle)*overlap


class Particle():
    def __init__(self, (x, y), size, density = 1):
        self.x = x
        self.y = y
        self.size = size
        self.density = density
        self.mass = density*size**2
        self.drag = (self.mass/(self.mass + mass_of_air)) ** self.size
        self.elasticity = 0.75 #Percent of speed remaining after a collision
        self.colour = [200-density*10, 200-density*10, 255]
        self.thickness = 0
        self.speed = 0
        self.angle = 0
        self.selected = False
        self.set_rect()

    def get_rect(self):
        return self.rect

    def set_rect(self):
        self.rect = pygame.Rect(self.x-self.size, self.y-self.size, self.size*2, self.size*2)

    def getselected(self):
        return self.selected

    def setselected(self):
        if self.selected:
            self.selected = False
        else:
            self.selected = True

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)
        if self.selected:
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size - 2, self.thickness)
        if speedNum:
            partText = particleFont.render(str(int(self.speed)), True, WHITE)
            screen.blit(partText, (self.x,self.y))

    def move(self):
        (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag

    def adjstcolour(self, r, g, b):
        if self.colour[0] + r <= 255:
            self.colour[0] += r
        else:
            self.colour[0] = self.colour[0]+ r - 255
        if self.colour[1] + g <= 255:
            self.colour[1] += g
        else:
            self.colour[1] = self.colour[1]+ g - 255
        if self.colour[2] + b <= 255:
            self.colour[2] += b
        else:
            self.colour[2] = self.colour[2]+ b - 255

    def bounce(self):
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = - self.angle
            self.speed *= self.elasticity

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle
            self.speed *= self.elasticity

        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity

my_particles = []
grav_particles = []

for n in range(number_of_particles):
    createParticle()

selected_particle = None
mousegrav = False
running = True
pause = False
screenfill = True
menu = False
pauseText = gameFont.render('Paused', True, WHITE)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseLB,mouseMB,mouseRB) = pygame.mouse.get_pressed()
            (mouseX, mouseY) = pygame.mouse.get_pos()
            if mouseRB:
                grav_particle = findParticle(my_particles, mouseX, mouseY)
                if grav_particle:
                    grav_particle.setselected()
                    if grav_particle.getselected():
                        grav_particles.append(grav_particle)
                    else:
                        grav_particles.remove(grav_particle)
                #pause = True
                #menu = True
                #menupos = Rect((mouseX, mouseY),(200,300))
            else:
                selected_particle = findParticle(my_particles, mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None
        elif event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                mousegrav = True
            if event.key == pygame.K_w:
                gravity[1] += 0.001
            if event.key == pygame.K_e:
                gravity[1] += 0.01
            if event.key == pygame.K_s:
                gravity[1] -= 0.001
            if event.key == pygame.K_d:
                gravity[1] -= 0.01
            if event.key == pygame.K_f:
                gravity[1] = input('Enter a magnitude value for gravity: ')
            if event.key == pygame.K_r:
                gravity[1] = -gravity[1]
            if event.key == pygame.K_q:
                if pause:
                    pause = False
                else:
                    pause = True
            if event.key == pygame.K_c:
                if screenfill:
                    screenfill = False
                else:
                    screenfill = True
        elif event.type == KEYUP:
            if event.key == pygame.K_SPACE:
                mousegrav = False
    if not pause:
        if screenfill:
            screen.fill(background_colour)
        if mousegrav:
            for i, particle in enumerate(my_particles):
                (mouseX, mouseY) = pygame.mouse.get_pos()
                dx = mouseX - particle.x
                dy = mouseY - particle.y
                (particle.angle, particle.speed) = addVectors((particle.angle, particle.speed), (0.5*math.pi + math.atan2(dy, dx), math.hypot(dx, dy) * gravity[1]))
        if selected_particle:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            dx = mouseX - selected_particle.x
            dy = mouseY - selected_particle.y
            selected_particle.angle = 0.5*math.pi + math.atan2(dy, dx)
            selected_particle.speed = math.hypot(dx, dy) * 0.1
        if len(grav_particles) > 0:
            for i, particle in enumerate(my_particles):
                for i, grav_particle in enumerate(grav_particles):
                    dx = grav_particle.x - particle.x
                    dy = grav_particle.y - particle.y
                    (particle.angle, particle.speed) = addVectors((particle.angle, particle.speed), (0.5*math.pi + math.atan2(dy, dx), math.hypot(dx, dy) * gravity[1]))
    else:
        screen.blit(pauseText, (5,35))
    if menu:
        displaymenu()
        pause = False
        menu = False
            
    for particle in my_particles:
        if not pause: 
            particle.move()
            particle.bounce()
            particle.set_rect()
            particle.adjstcolour(0, random.randint(1,5), 0)
    tree = Quadtree(0, pygame.Rect(0,0,width,height), my_particles)#comment out these lines two not use quadtree framework
    tree.update(screen)#comment out these lines two not use quadtree framework
    for particle in my_particles:
        particle.display()
    gravText = gameFont.render(str(gravity[1]), True, WHITE)
    numText = gameFont.render(str(len(my_particles)), True, WHITE)
    screen.blit(gravText, (5,5))
    screen.blit(numText, (5,20))
    FPSCLOCK.tick(FPS)
    pygame.display.flip()
