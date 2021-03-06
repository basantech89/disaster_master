# Asteroid
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time, t = 0, 0
started, explode = False, False
rocks, missiles = set(), set()

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            image_center = [self.image_center[0] + 90, self.image_center[1]]
        else:
            image_center = self.image_center            
        canvas.draw_image(self.image, image_center, self.image_size, self.pos, self.image_size, self.angle) 
        
    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # position update           
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # friction update
        self.vel[0] *= (1 - 0.01)
        self.vel[1] *= (1 - 0.01)
        
        # thrust update - acceleration in direction of forward vector
        forward = [math.cos(self.angle), math.sin(self.angle)]
        if self.thrust:
            self.vel[0] += forward[0] * 0.1
            self.vel[1] += forward[1] * 0.1
        
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.flag = True
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.flag and not explode:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)   
                        
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.age += 1
        if self.age > self.lifespan :  self.flag = False
    
    def collide(self, other):
        if dist(self.pos, other.pos) >= self.radius + other.radius:
            return False
        else:
            return True 
        
def draw(canvas):
    global time, lives, score, started, rocks, t, explode
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text("Lives " + str(lives), (10, 40), 20, "White", "monospace")
    canvas.draw_text("Score " + str(score), (WIDTH - 100, 40), 20, "White", "monospace")
    
    # draw and update things
    my_ship.draw(canvas)
    my_ship.update()
    
    for rock in rocks:
        rock.draw(canvas)
        rock.update()
        
    for missile in missiles:
        missile.draw(canvas)
        missile.update()
    
    # update lives and scores for player
    collisions = groups_collide(rocks, missiles)
    score += collisions
    if group_collide(rocks, my_ship):
        explode = True
        lives -= 1
        if explode:
            center, size = explosion_info.get_center(), explosion_info.get_size()
            current_index = (t % 21) // 1
            img_center = [center[0] + (current_index * size[0]), center[1]]
            canvas.draw_image(explosion_image, img_center, size, my_ship.pos, size)
            explosion_sound.play()
            t += 60.0 / 21
    else : explode = False
    if lives == 0:
        started = False
        rocks = set()
        soundtrack.pause()
        
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        
    
# timer handler that spawns a rock    
def rock_spawner():
    global rocks
    if started == True:
        a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
        if len(rocks) <= 12 : rocks.add(a_rock)
        for rock in rocks:
            rock.pos[0] = random.randrange(0, WIDTH)
            rock.pos[1] = random.randrange(0, HEIGHT)
            rock.vel[0] = random.random() * .6 - .3
            rock.vel[1] = random.random() * .6 - .3
            rock.angle_vel, a_rock.angle = random.random() * .2 - .1, random.randrange(0, 361)    
        
def shoot():
    global missiles
    a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1, 1], 0, 0, missile_image, missile_info, missile_sound)
    missiles.add(a_missile)
    missile_sound.play()
    cos, sin = math.cos(my_ship.angle), math.sin(my_ship.angle)
    for missile in missiles:
        missile.pos[0] = my_ship.pos[0] + (my_ship.radius * cos)
        missile.pos[1] = my_ship.pos[1] + (my_ship.radius * sin)
        missile.vel[0] = my_ship.vel[0] + cos * 6
        missile.vel[1] = my_ship.vel[1] + sin * 6
        
def thrustUpdate():
    my_ship.thrust = True
    ship_thrust_sound.rewind()
    ship_thrust_sound.play()
    
def keydown(key):
    if key == simplegui.KEY_MAP["left"] : my_ship.angle_vel -= 0.05
    if key == simplegui.KEY_MAP["right"] : my_ship.angle_vel += 0.05        
    if key == simplegui.KEY_MAP["up"]: thrustUpdate()
    if key == simplegui.KEY_MAP["space"] : shoot()            
        
def keyup(key):
    if key == simplegui.KEY_MAP["left"] or key == simplegui.KEY_MAP["right"] : my_ship.angle_vel = 0
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust = False
        ship_thrust_sound.pause()
    
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score, soundtrack
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives, score = 3, 0
        soundtrack.play()
        
def group_collide(group, sprite):
    f = False
    for g in list(group):
        if g.collide(sprite):
            group.remove(g)
            f = True                  
    return f		            
                
def groups_collide(group1, group2):
    collisions = 0
    for g in list(group2):
        if group_collide(group1, g):
            group2.remove(g)
            collisions += 1
    return collisions

    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)


# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1500.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
