'''This script is testing mass, particle centered gravity(left click),
density(darker blue means higher density), input amount of gravity('f' key'),
and quadtree collision system'''
import pygame, random, math, sys

from pygame.locals import *
from Quadtree import *
from ParticleClass import Particle

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
(width, height) = (1400, 800)#1400, 800
gameFont = pygame.font.Font(None, 20)
selectFont = pygame.font.Font(None, 20)
selectFont.set_underline(True)
FPS = 30
FPSCLOCK = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Particle Simulator')

number_of_particles = 100 #Number of particles when simulation begins (500)
particleSize = (3, 8) #Range of particle size (3 < particleSize < 16)
mass_of_air = 0.02 #Mass of air (higher value means more air resistance) (0.02)
gravity = [math.pi, 0.008] #gravity angle and magnitude (realistic=0.5, space=0.008)
crazysize = False

def displaymenu(particle, position):
    menu = True
    mouseClicked = False
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
        radiusText = gameFont.render('Radius: ' +str(particle.get_size()),True,textcolor)
        gravselText = gameFont.render('G',True,textcolor)
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
                    mouseClicked = True
        pygame.draw.rect(screen, menucolor, menuRect)
        pygame.draw.circle(screen, WHITE, (position[0], position[1]), 2, 0)
        if particle:
            screen.blit(speedText, (menux+5,yblit))
            screen.blit(coordText, (menux+90,yblit))
            yblit += 15
            screen.blit(massText, (menux+5,yblit))
            screen.blit(radiusText, (menux+90,yblit))
            if particle.get_selected():
                screen.blit(gravselText, (menux+180,yblit))
            yblit += 15
            screen.blit(breakText, (menux+5,yblit))
            yblit += 15
            if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux and mouseX <= menux+menuRect.width:
                deleteText = selectFont.render('DELETE PARTICLE',True,textcolor)
                if mouseClicked:
                    my_particles.remove(particle)
                    if particle in grav_particles:
                        grav_particles.remove(particle)
                    return
            else:
                deleteText = gameFont.render('DELETE PARTICLE',True,textcolor)
            screen.blit(deleteText, (menux+5,yblit))
            yblit += 15
            if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux and mouseX <= menux+menuRect.width:
                cloneText= selectFont.render('CLONE PARTICLE', True, textcolor)
                if mouseClicked:
                    clonex = particle.get_x()+5
                    cloney = particle.get_y()
                    clonesize = particle.get_size()
                    clonedensity = particle.get_density()
                    createParticle(clonex, cloney, clonesize, clonedensity)
                    return
            else:
                cloneText= gameFont.render('CLONE PARTICLE', True, textcolor)
            screen.blit(cloneText, (menux+5,yblit))
            yblit += 15
            if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux and mouseX <= menux+menuRect.width:
                if particle.get_selected():
                    gravpartText= selectFont.render('DEGRAVITATE PARTICLE', True, textcolor)
                    if mouseClicked:
                        particle.set_selected()
                        grav_particles.remove(particle)
                        return
                else:
                    gravpartText= selectFont.render('GRAVITATE PARTICLE', True, textcolor)
                    if mouseClicked:
                        particle.set_selected()
                        grav_particles.append(particle)
                        return
            else:
                if particle.get_selected():
                    gravpartText= gameFont.render('DEGRAVITATE PARTICLE', True, textcolor)
                else:
                    gravpartText= gameFont.render('GRAVITATE PARTICLE', True, textcolor)
            screen.blit(gravpartText, (menux+5,yblit))
            yblit += 15
            if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux and mouseX <= menux+menuRect.width:
                stopText= selectFont.render('STOP PARTICLE', True, textcolor)
                if mouseClicked:
                    particle.set_speed(0)
                    return
            else:
                stopText= gameFont.render('STOP PARTICLE', True, textcolor)
            screen.blit(stopText, (menux+5,yblit))
            yblit += 15
            if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux and mouseX <= menux+menuRect.width:
                if particle.get_moveable():
                    moveableText= selectFont.render('MAKE IMMOVABLE', True, textcolor)
                    if mouseClicked:
                        particle.set_moveable()
                        return
                else:
                    moveableText= selectFont.render('MAKE MOVEABLE', True, textcolor)
                    if mouseClicked:
                        particle.set_moveable()
                        return
            else:
                if particle.get_moveable():
                    moveableText= gameFont.render('MAKE IMMOVABLE', True, textcolor)
                else:
                    moveableText= gameFont.render('MAKE MOVEABLE', True, textcolor)
            screen.blit(moveableText, (menux+5,yblit))
            yblit += 15

        screen.blit(breakText, (menux+5,yblit))
        yblit += 15
        if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux and mouseX <= menux+menuRect.width:
            createText= selectFont.render('CREATE PARTICLE', True, textcolor)
            if mouseClicked:
                createParticle(position[0], position[1])
                return
        else:
            createText= gameFont.render('CREATE PARTICLE', True, textcolor)
        screen.blit(createText, (menux+5,yblit))
        yblit += 15
        screen.blit(breakText, (menux+5,yblit))
        yblit += 15
        if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux and mouseX <= menux+menuRect.width:
            gravallText= selectFont.render('DEGRAVITATE ALL', True, textcolor)
            if mouseClicked:
                for grav_particle in grav_particles[:]:
                    grav_particle.set_selected()
                    grav_particles.remove(grav_particle)
                return
        else:
            gravallText= gameFont.render('DEGRAVITATE ALL', True, textcolor)
        screen.blit(gravallText, (menux+5,yblit))
        yblit += 15
        if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux and mouseX <= menux+(menuRect.width/2):
            gravmultText= selectFont.render('3X GRAVITY', True, textcolor)
            if mouseClicked:
                gravity[1] *= 3
                return
        else:
            gravmultText= gameFont.render('3X GRAVITY', True, textcolor)
        screen.blit(gravmultText, (menux+5,yblit))
        if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux+(menuRect.width/2) and mouseX <= menux+menuRect.width:
            gravdividText= selectFont.render('GRAVITY /3', True, textcolor)
            if mouseClicked:
                gravity[1] /= 3
                return
        else:
            gravdividText= gameFont.render('GRAVITY /3', True, textcolor)
        screen.blit(gravdividText, (menux+115,yblit))
        yblit += 15
        if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux and mouseX <= menux+menuRect.width:
            entgravText= selectFont.render('ENTER GRAVITY AMOUNT', True, textcolor)
            if mouseClicked:
                gravity[1] = input('Enter a magnitude value for gravity: ')
                return
        else:
            entgravText= gameFont.render('ENTER GRAVITY AMOUNT', True, textcolor)
        screen.blit(entgravText, (menux+5,yblit))
        yblit += 15
        screen.blit(breakText, (menux+5,yblit))
        yblit += 15
        if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux and mouseX <= menux+menuRect.width:
            scrambleText= selectFont.render('SCRAMBLE PARTICLES', True, textcolor)
            if mouseClicked:
                for particle in my_particles:
                    particle.set_coordinates(random.randint(particle.size, width-particle.size), random.randint(particle.size, height-particle.size))
                return
        else:
            scrambleText= gameFont.render('SCRAMBLE PARTICLES', True, textcolor)
        screen.blit(scrambleText, (menux+5,yblit))
        yblit += 15
        if mouseY >= yblit and mouseY <= yblit+ 15 and mouseX >= menux and mouseX <= menux+menuRect.width:
            danceText= selectFont.render('DANCE PARTY', True, textcolor)
            if mouseClicked:
                for particle in my_particles:
                    particle.set_coordinates(random.randint(particle.size, width-particle.size), random.randint(particle.size, height-particle.size))
                    particle.set_speed(random.randint(20, 50))
                    particle.set_color([random.randint(20,230),random.randint(20,230),random.randint(20,230)])
                return
        else:
            danceText= gameFont.render('DANCE PARTY', True, textcolor)
        screen.blit(danceText, (menux+5,yblit))
            
        FPSCLOCK.tick(FPS)
        pygame.display.update()

def createParticle(x = None, y = None, size = None, density = None):
    if size == None:
        size = random.randint(particleSize[0], particleSize[1])
    if density == None:
        density = random.randint(1, 20)
    if x == None or y == None:
        x = random.randint(size, width-size)
        y = random.randint(size, height-size)
    particle = Particle(x, y, size, density, mass_of_air)
    particle.speed = random.random()
    particle.angle = random.uniform(0, math.pi*2)

    my_particles.append(particle)

def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None        

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
                menu = True
            else:
                selected_particle = findParticle(my_particles, mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None
        elif event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                mousegrav = True
            if event.key == pygame.K_a:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                createParticle(mouseX, mouseY)
            if event.key == pygame.K_w:
                gravity[1] += 0.001
            if event.key == pygame.K_e:
                gravity[1] += 0.01
            if event.key == pygame.K_s:
                gravity[1] -= 0.001
            if event.key == pygame.K_d:
                gravity[1] -= 0.01
            if event.key == pygame.K_r:
                gravity[1] = -gravity[1]
            if event.key == pygame.K_p:
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
    if screenfill:
        screen.fill(background_color)
    if not pause:
        if mousegrav:
            for i, particle in enumerate(my_particles):
                (mouseX, mouseY) = pygame.mouse.get_pos()
                dx = mouseX - particle.x
                dy = mouseY - particle.y
                (particle.angle, particle.speed) = addVectors(particle.angle, particle.speed, 0.5*math.pi + math.atan2(dy, dx), math.hypot(dx, dy) * gravity[1])
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
                    (particle.angle, particle.speed) = addVectors(particle.angle, particle.speed, 0.5*math.pi + math.atan2(dy, dx), math.hypot(dx, dy) * gravity[1])
        for particle in my_particles:
            if crazysize:
                particle.adjustsize(1)
            particle.move(gravity)
            particle.bounce(width, height)
            particle.set_rect()
            particle.adjustcolor(0, random.randint(1,5), random.randint(1,5))
            #print (particle.get_x(),particle.get_y())
        tree = Quadtree(0, pygame.Rect(0,0,width,height), my_particles)#comment out these lines for no collisions
        tree.update(screen)#comment out these lines for no collisions
    for particle in my_particles:
        particle.display(screen)
    gravText = gameFont.render(str(gravity[1]), True, WHITE)
    numText = gameFont.render(str(len(my_particles)), True, WHITE)
    if pause:
        screen.blit(pauseText, (5,35)) 
    screen.blit(gravText, (5,5))
    screen.blit(numText, (5,20))
    if menu:
        if mouse_particle:
            menupos = (mouse_particle.get_x(), mouse_particle.get_y(), 200, 265)#x,y,w,h
        else:
            menupos = (mouseX, mouseY, 200, 145)#x,y,w,h
        if not pause:
            screen.blit(pauseText, (5,35))
        displaymenu(mouse_particle, menupos)
        menu = False
    FPSCLOCK.tick(FPS)
    pygame.display.update()

pygame.quit()
sys.exit()
