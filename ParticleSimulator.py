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

background_color = (0,0,0)
(width, height) = (1400, 800)
gameFont = pygame.font.Font(None, 20)
selectFont = pygame.font.Font(None, 20)
selectFont.set_underline(True)
FPS = 30
FPSCLOCK = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Particle Simulator')

number_of_particles = 1000 #Number of particles when simulation begins (500)
particleSize = (3, 8) #Range of particle size (3 < particleSize < 16)
mass_of_air = 0.02 #Mass of air (higher value means more air resistance) (0.02)
gravity = [math.pi, 0.008] #gravity angle and magnitude (realistic-0.5, space-0.008)
speedNum = False #If True, particle speeds appear near particles (Pixles per frame)

def displaymenu(particle, position):
    menu = True
    if position[1] >= height/2:
        menuy = position[1]-position[3]
    else:
        menuy = position[1]
    if position[0] >= width/2:
        menux = position[0]-position[2]
    else:
        menux = position[0]
    menuRect = Rect(menux, menuy, position[2], position[3])
    menucolor = averagecolor(my_particles)
    if menucolor[0] > 210 or menucolor[1] > 210 or menucolor[2] > 210:
        textcolor = BLACK
    else:
        textcolor = WHITE
    if particle:
        speedText = gameFont.render('Speed:'+str(round(particle.speed,2)), True, textcolor)
        coordText = gameFont.render('(x,y):'+str((particle.get_x(),particle.get_y())), True, textcolor)
        massText = gameFont.render('Mass:'+str(particle.get_mass()),True,textcolor)
    breakText = gameFont.render('--------------------------------',True,textcolor)

    while menu:
        yblit = menuy + 5
        (mouseX, mouseY) = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouseLB,mouseMB,mouseRB) = pygame.mouse.get_pressed()
                if mouseRB:
                    menu = False
                else:
                    (mouseX, mouseY) = pygame.mouse.get_pos()
        pygame.draw.rect(screen, menucolor, menuRect)
        pygame.draw.circle(screen, WHITE, (position[0], position[1]), 2, 0)
        if particle:
            screen.blit(speedText, (menux+5,yblit))
            screen.blit(coordText, (menux+90,yblit))
            yblit += 15
            screen.blit(massText, (menux+5,yblit))
            yblit += 15
            screen.blit(breakText, (menux+5,yblit))
            yblit += 15
            if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux and mouseX <= menux+menuRect.width:
                deleteText = selectFont.render('DELETE PARTICLE',True,textcolor)
            else:
                deleteText = gameFont.render('DELETE PARTICLE',True,textcolor)
            screen.blit(deleteText, (menux+5,yblit))
            yblit += 15
            if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux and mouseX <= menux+menuRect.width:
                cloneText= selectFont.render('CLONE PARTICLE', True, textcolor)
            else:
                cloneText= gameFont.render('CLONE PARTICLE', True, textcolor)
            screen.blit(cloneText, (menux+5,yblit))
            yblit += 15
            if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux and mouseX <= menux+menuRect.width:
                gravpartText= selectFont.render('GRAVITATE PARTICLE', True, textcolor)
            else:
                gravpartText= gameFont.render('GRAVITATE PARTICLE', True, textcolor)
            screen.blit(gravpartText, (menux+5,yblit))
            yblit += 15
            if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux and mouseX <= menux+menuRect.width:
                stopText= selectFont.render('STOP PARTICLE', True, textcolor)
            else:
                stopText= gameFont.render('STOP PARTICLE', True, textcolor)
            screen.blit(stopText, (menux+5,yblit))
            yblit += 15

        screen.blit(breakText, (menux+5,yblit))
        yblit += 15
        if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux and mouseX <= menux+menuRect.width:
            createText= selectFont.render('CREATE PARTICLE', True, textcolor)
        else:
            createText= gameFont.render('CREATE PARTICLE', True, textcolor)
        screen.blit(createText, (menux+5,yblit))
        yblit += 15
        screen.blit(breakText, (menux+5,yblit))
        yblit += 15
        if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux and mouseX <= menux+menuRect.width:
            gravallText= selectFont.render('DEGRAVITATE ALL', True, textcolor)
        else:
            gravallText= gameFont.render('DEGRAVITATE ALL', True, textcolor)
        screen.blit(gravallText, (menux+5,yblit))
        yblit += 15
        if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux and mouseX <= menux+(menuRect.width/2):
            gravmultText= selectFont.render('3X GRAVITY', True, textcolor)
        else:
            gravmultText= gameFont.render('3X GRAVITY', True, textcolor)
        screen.blit(gravmultText, (menux+5,yblit))
        if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux+(menuRect.width/2) and mouseX <= menux+menuRect.width:
            gravdividText= selectFont.render('GRAVITY /3', True, textcolor)
        else:
            gravdividText= gameFont.render('GRAVITY /3', True, textcolor)
        screen.blit(gravdividText, (menux+115,yblit))
        yblit += 15
        if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux and mouseX <= menux+menuRect.width:
            entgravText= selectFont.render('ENTER GRAVITY AMOUNT', True, textcolor)
        else:
            entgravText= gameFont.render('ENTER GRAVITY AMOUNT', True, textcolor)
        screen.blit(entgravText, (menux+5,yblit))
        yblit += 15
        screen.blit(breakText, (menux+5,yblit))
        yblit += 15
        if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux and mouseX <= menux+menuRect.width:
            scrambleText= selectFont.render('SCRAMBLE PARTICLES', True, textcolor)
        else:
            scrambleText= gameFont.render('SCRAMBLE PARTICLES', True, textcolor)
        screen.blit(scrambleText, (menux+5,yblit))
        yblit += 15
        if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux and mouseX <= menux+menuRect.width:
            airmassText= selectFont.render('MASS OF AIR TO ZERO', True, textcolor)
        else:
            airmassText= gameFont.render('MASS OF AIR TO ZERO', True, textcolor)
        screen.blit(airmassText, (menux+5,yblit))
        yblit += 15
        if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux and mouseX <= menux+menuRect.width:
            danceText= selectFont.render('DANCE PARTY', True, textcolor)
        else:
            danceText= gameFont.render('DANCE PARTY', True, textcolor)
        screen.blit(danceText, (menux+5,yblit))
            
        FPSCLOCK.tick(FPS)
        pygame.display.update()

def createParticle(x = None, y = None):
    size = random.randint(particleSize[0], particleSize[1])
    density = random.randint(1, 20)
    if x == None or y == None:
        x = random.randint(size, width-size)
        y = random.randint(size, height-size)
    particle = Particle((x, y), size, density)
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

def adjustcolor(color, r, g, b):
        if color[0] + r <= 255:
            color[0] += r
        else:
            color[0] = color[0]+ r - 255
        if color[1] + g <= 255:
            color[1] += g
        else:
            color[1] = color[1]+ g - 255
        if color[2] + b <= 255:
            color[2] += b
        else:
            color[2] = color[2]+ b - 255
        return color

def averagecolor(particlelist):
    coloravg = [0,0,0]
    for particle in particlelist:
        coloravg[0] += particle.color[0]
        coloravg[1] += particle.color[1]
        coloravg[2] += particle.color[2]
    coloravg[0]= coloravg[0]/len(particlelist)
    coloravg[1]= coloravg[1]/len(particlelist)
    coloravg[2]= coloravg[2]/len(particlelist)
    return coloravg

class Particle():
    def __init__(self, (x, y), size, density = 1):
        self.x = x
        self.y = y
        self.size = size
        self.density = density
        self.mass = density*size**2
        self.drag = (self.mass/(self.mass + mass_of_air)) ** self.size
        self.elasticity = 0.75 #Percent of speed remaining after a collision
        self.color = [200-density*10, 0, 200-density*10]#starting color
        self.thickness = 0
        self.speed = 0
        self.angle = 0
        self.selected = False
        self.set_rect()

    def get_x(self):
        return int(self.x)

    def get_y(self):
        return int(self.y)

    def get_mass(self):
        return self.mass
    
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
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size, self.thickness)
        if self.selected:
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size - 2, self.thickness)
        if speedNum:
            partText = gameFont.render(str(int(self.speed)), True, WHITE)
            screen.blit(partText, (self.x,self.y))

    def move(self):
        (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag

    def adjustcolor(self, r, g, b):
        if self.color[0] + r <= 255:
            self.color[0] += r
        else:
            self.color[0] = self.color[0]+ r - 255
        if self.color[1] + g <= 255:
            self.color[1] += g
        else:
            self.color[1] = self.color[1]+ g - 255
        if self.color[2] + b <= 255:
            self.color[2] += b
        else:
            self.color[2] = self.color[2]+ b - 255

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
                mouse_particle = findParticle(my_particles, mouseX, mouseY)
                pause = True
                menu = True
                if mouse_particle:
                    menupos = (mouse_particle.get_x(), mouse_particle.get_y(), 200, 265)#x,y,w,h
                else:
                    menupos = (mouseX, mouseY, 200, 160)#x,y,w,h
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
            #if event.key == pygame.K_f:
                #gravity[1] = input('Enter a magnitude value for gravity: ')
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
            screen.fill(background_color)
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
        displaymenu(mouse_particle, menupos)
        pause = False
        menu = False
            
    for particle in my_particles:
        if not pause: 
            particle.move()
            particle.bounce()
            particle.set_rect()
            particle.adjustcolor(random.randint(1,5), 0, random.randint(1,5))
    tree = Quadtree(0, pygame.Rect(0,0,width,height), my_particles)#comment out these lines for no collisions
    tree.update(screen)#comment out these lines for no collisions
    for particle in my_particles:
        particle.display()
    gravText = gameFont.render(str(gravity[1]), True, WHITE)
    numText = gameFont.render(str(len(my_particles)), True, WHITE)
    screen.blit(gravText, (5,5))
    screen.blit(numText, (5,20))
    FPSCLOCK.tick(FPS)
    pygame.display.update()

pygame.quit()
sys.exit()
