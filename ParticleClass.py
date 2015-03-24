import pygame
import math

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

speedNum = False #If True, particle speeds appear near particles (Pixles per frame)

def addVectors((angle1, length1), (angle2, length2)):
    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    
    angle = 0.5 * math.pi - math.atan2(y, x)
    length  = math.hypot(x, y)

    return (angle, length)

def adjustcolor(color, r, g, b):
        if color[0] + r <= 255:
            color[0] += r
        else:
            color[0] = color[0]+ r - 255#255
        if color[1] + g <= 255:
            color[1] += g
        else:
            color[1] = color[1]+ g - 255#255
        if color[2] + b <= 255:
            color[2] += b
        else:
            color[2] = color[2]+ b - 255#255
        return color

class Particle():
    def __init__(self, (x, y), size, density = 1, air_mass = 0.0):
        self.x = x
        self.y = y
        self.size = size
        self.density = density
        self.mass = density*size**2
        self.drag = (self.mass/(self.mass + air_mass)) ** self.size
        self.elasticity = 0.75 #Percent of speed remaining after a collision
        self.color = [0, 0, 255-density*10]#starting color 200-density*10
        self.thickness = 0
        self.speed = 0
        self.angle = 0
        self.selected = False
        self.moveable = True
        self.set_rect()

    def get_x(self):
        return int(self.x)

    def get_y(self):
        return int(self.y)

    def get_mass(self):
        return self.mass

    def get_density(self):
        return self.density

    def get_size(self):
        return self.size

    def get_color(self):
        return self.color
    
    def get_rect(self):
        return self.rect

    def get_selected(self):
        return self.selected

    def get_moveable(self):
        return self.moveable

    def set_rect(self):
        self.rect = pygame.Rect(self.x-self.size, self.y-self.size, self.size*2, self.size*2)

    def set_color(self, color):
        self.color = color

    def set_speed(self, speed):
        self.speed = speed
        
    def set_moveable(self):
        if self.moveable:
            self.moveable = False
            self.speed = 0
            self.angle = 0
        else:
            self.moveable = True
    
    def set_coordinates(self, x, y):
        self.x = x
        self.y = y
        
    def set_selected(self):
        if self.selected:
            self.selected = False
        else:
            self.selected = True

    def delete(self, particleList):
        particleList.remove(self)

    def display(self, display):
        pygame.draw.circle(display, self.color, (int(self.x), int(self.y)), self.size, self.thickness)
        if self.selected:
            pygame.draw.circle(display, WHITE, (int(self.x), int(self.y)), self.size - 2, self.thickness)
        if speedNum:
            partText = gameFont.render(str(int(self.speed)), True, WHITE)
            screen.blit(partText, (self.x,self.y))

    def move(self, gravity = [math.pi, 0.000]):
        if self.moveable:
            (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
            self.x += math.sin(self.angle) * self.speed
            self.y -= math.cos(self.angle) * self.speed
            self.speed *= self.drag
        else:
            self.speed = 0
            self.angle = 0

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

    def bounce(self, display_width, display_height):
        if self.x > display_width - self.size:
            self.x = 2*(display_width - self.size) - self.x
            self.angle = - self.angle
            self.speed *= self.elasticity

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle
            self.speed *= self.elasticity

        if self.y > display_height - self.size:
            self.y = 2*(display_height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity
