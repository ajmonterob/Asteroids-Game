"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.
"""
import arcade
import random
import math
from abc import ABC, abstractmethod
import os


# These are Global constants to use throughout the game
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.10
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2

class Point:
    #Point on the space
    def __init__(self):
        self.x = 0.0
        self.y = 0.0

class Velocity:
    #Initial velocity
    def __init__(self):
        self.dx = 0
        self.dy = 0

class FlyingObjects(ABC):
    """
    This class handles is the base for all the flying objects
    
    """
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.alive = True

    #Move the object
    def advance(self):
        self.wrap()
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    #verify if the object is alive
    def is_alive(self):
        return self.alive

    #Adding abstrac class
    @abstractmethod
    def draw(self):
        pass

    #Keeps the object inside the screen
    def wrap(self):
        if self.center.x > SCREEN_WIDTH:
            self.center.x -= SCREEN_WIDTH
        if self.center.x < 0:
            self.center.x += SCREEN_WIDTH
        if self.center.y > SCREEN_HEIGHT:
            self.center.y -= SCREEN_HEIGHT
        if self.center.y < 0:
            self.center.y += SCREEN_HEIGHT

class Ship(FlyingObjects):
    """
    Ship class, this is the main object of the game
    """
    def __init__(self):
        #Declaring ship variables
        self.img = "images/playerShip1_orange.png"
        self.texture = arcade.load_texture(self.img)
        self.height = self.texture.height
        self.width = self.texture.width
        super().__init__()
        self.radius = SHIP_RADIUS
        self.center.x = SCREEN_WIDTH / SMALL_ROCK_RADIUS
        self.center.y = SCREEN_HEIGHT / SMALL_ROCK_RADIUS
        self.angle = 1
        self.alive = True
    
    #moving to the right with the right key
    def right(self):
        self.angle -= SHIP_TURN_AMOUNT
        
    #moving to the lef with the right key
    def left(self):
        self.angle += SHIP_TURN_AMOUNT

    #moving to the up with the right key
    def thrust(self):
        self.velocity.dy += math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        self.velocity.dx -= math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT

    #moving to the right with the down key
    def thrust_backward(self):
        self.velocity.dy -= math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        self.velocity.dx += math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width,self.height, self.texture, self.angle, 255)

class Bullet(FlyingObjects):
    """
    Class with the lasser, this class represent the bullet
    
    """
    def __init__(self, ship_angle, ship_x, ship_y):
        #Declaring the variables
        super().__init__()
        self.img = "images/laserBlue01.png"
        self.texture = arcade.load_texture(self.img)
        self.width = self.texture.width
        self.height = self.texture.height
        self.radius = BULLET_RADIUS
        self.speed = BULLET_SPEED
        self.angle = ship_angle - 90
        self.center.x = ship_x
        self.center.y = ship_y
        self.life = BULLET_LIFE
        
    #Setting the velocity of the bullet
    def fire(self):
        self.velocity.dx -= math.sin(math.radians(self.angle + 90)) * self.speed
        self.velocity.dy += math.cos(math.radians(self.angle + 90)) * self.speed
        
        
    #Moving the bullet
    def advance(self):
        super().advance()
        self.life -= 1
        if self.life <= 0:
            self.alive = False
            
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width,self.height, self.texture, self.angle, 255)


class Asteroid(FlyingObjects):
    """
    Parent asteroid

    """
    def __init__(self):
        super().__init__()
        self.radius = 0
        self.img = "images/meteorGrey_small1.png"
        self.texture = arcade.load_texture(self.img)
        self.width = self.texture.width
        self.height = self.texture.height
        
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width,self.height, self.texture, self.angle, 255)

class SmallRock(Asteroid):
    #Small asteroid variables
    def __init__(self):
        super().__init__()
        self.radius = SMALL_ROCK_RADIUS
        self.img = "images/meteorGrey_small1.png"
        self.texture = arcade.load_texture(self.img)
        self.width = self.texture.width
        self.height = self.texture.height
        self.center.x = random.randint(1,50)
        self.center.y = random.randint(1,150)
        self.angle = 0.0
        
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width,self.height, self.texture, self.angle, 255)
        
    def advance(self):
        self.angle += SMALL_ROCK_SPIN
        super().advance()
        if self.angle >= 360:
            self.angle -= 360
        
    def break_rock(self, asteroids):
        self.alive = False
            
            
class MediumRock(Asteroid):
    def __init__(self):
        #Medium Rock Varibles
        super().__init__()
        self.radius = MEDIUM_ROCK_RADIUS
        self.speed = BIG_ROCK_SPEED
        self.img = "images/meteorGrey_med1.png"
        self.texture = arcade.load_texture(self.img)
        self.width = self.texture.width
        self.height = self.texture.height
        self.angle = 0.0
        
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width,self.height, self.texture, self.angle, 255)
        
    def advance(self):
        self.angle += MEDIUM_ROCK_SPIN
        super().advance()
        if self.angle >= 360:
            self.angle -= 360
            
    def break_rock(self, asteroids):
        small = SmallRock()
        small.center.x = self.center.x
        small.center.y = self.center.y
        small.velocity.dx = self.velocity.dy + BIG_ROCK_SPEED
        small.velocity.dy = self.velocity.dy + BIG_ROCK_SPEED

        small2 = SmallRock()
        small2.center.x = self.center.x
        small2.center.y = self.center.y
        small2.velocity.dx = self.velocity.dy - BIG_ROCK_SPEED
        small2.velocity.dy = self.velocity.dy - BIG_ROCK_SPEED

        asteroids.append(small)
        asteroids.append(small2)
        self.alive = False

class LargeRock(Asteroid):
    #Big Rocks Variables
    def __init__(self):
        super().__init__()
        self.img = "images/meteorGrey_big1.png"
        self.texture = arcade.load_texture(self.img)
        self.width = self.texture.width
        self.height = self.texture.height
        self.center.x = random.randint(1,SCREEN_WIDTH)
        self.center.y = random.randint(1,SCREEN_HEIGHT)
        self.angle = random.randint(1,360)
        self.velocity.dy = math.sin(math.radians(self.angle)) * BIG_ROCK_SPEED
        self.velocity.dx = math.cos(math.radians(self.angle)) * BIG_ROCK_SPEED
        self.radius = BIG_ROCK_RADIUS
        self.speed = BIG_ROCK_SPEED
        
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width,self.height, self.texture, self.angle, 255)

    def advance(self):
        self.angle += BIG_ROCK_SPIN
        super().advance()
        if self.angle >= 360:
            self.angle -= 360
            
    def break_rock(self, asteroids):
        med1 = MediumRock()
        med1.center.x = self.center.x
        med1.center.y = self.center.y
        med1.velocity.dy = self.velocity.dy + SMALL_ROCK_RADIUS
        
        med2 = MediumRock()
        med2.center.x = self.center.x
        med2.center.y = self.center.y
        med2.velocity.dy = self.velocity.dy - SMALL_ROCK_RADIUS
        
        small = SmallRock()
        small.center.x = self.center.x
        small.center.y = self.center.y
        small.velocity.dy = self.velocity.dy + MEDIUM_ROCK_RADIUS

        asteroids.append(med1)
        asteroids.append(med2)
        asteroids.append(small)
        self.alive = False


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.held_keys = set()
        self.asteroids = []
        self.ship = Ship()
        self.bullets = []
        self.asteroids
        self.game_over_sound = arcade.load_sound("GAMEOVER.wav")
        self.laser_sound = arcade.load_sound("laser1.wav")
        self.destroy_ship_sound = arcade.load_sound("boom.wav")
        


        # TODO: declare anything here you need the game class to track

        for i in range(INITIAL_ROCK_COUNT):
            Ast = LargeRock()
            self.asteroids.append(Ast)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # TODO: draw each object
        self.ship.draw()
        
        
        # to draw the rocks
        for i in self.asteroids:
            i.draw()
            
         #To draw the lasers bullets   
        for i in self.bullets:
            i.draw()

    #Remove the destroyed objects
    def remove_notAliveObjects(self):
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)
                
        for asteroid in self.asteroids:
            if not asteroid.alive:
                self.asteroids.remove(asteroid)
            
                
    #Verify if the objects hit each other, first the rocks
    def check_collisions(self):
        for bullet in self.bullets:
            for asteroid in self.asteroids:
                if (bullet.alive and asteroid.alive):
                    dx = abs(asteroid.center.x - bullet.center.x)
                    dy = abs(asteroid.center.y - bullet.center.y)
                    allow_distance = asteroid.radius + bullet.radius
                    if ((dx < allow_distance) and (dy < allow_distance)):
                        asteroid.break_rock(self.asteroids)
                        bullet.alive= False
                        asteroid.alive = False
                        
         #Verify if the ship was hit by a rock   
        for asteroid in self.asteroids:
            if self.ship.alive and asteroid.alive:
                impact = self.ship.radius + asteroid.radius
                if (abs(self.ship.center.x - asteroid.center.x) < impact and abs(self.ship.center.y - asteroid.center.y) < impact):
                    self.ship.alive = False
                    
                

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()
        
        
        

        # TODO: Tell everything to advance or move forward one step in time

        for i in self.asteroids:
            i.advance()

        for i in self.bullets:
            i.advance()
        
        if self.ship.alive == True:
         self.ship.advance()
         

        self.remove_notAliveObjects()
        
        self.check_collisions()
        
        #Import, here is the end of the game. The ship is replace by a explotion. 
        if self.ship.alive == False:
            self.ship.img = "images/destroyed.png"
            self.ship.texture = arcade.load_texture(self.ship.img)
            arcade.play_sound(self.destroy_ship_sound)
            arcade.play_sound(self.game_over_sound)
            arcade.exit()
            
        
            
    # Machine gun mode...
        #if arcade.key.SPACE in self.held_keys:
        #    pass

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.left()
            

        if arcade.key.RIGHT in self.held_keys:
            self.ship.right()
            

        if arcade.key.UP in self.held_keys:
            self.ship.thrust()
            

        if arcade.key.DOWN in self.held_keys:
            self.ship.thrust_backward()
            

        

    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)
            if key == arcade.key.SPACE:
                bullet = Bullet(self.ship.angle, self.ship.center.x,
self.ship.center.y)
                self.bullets.append(bullet)
                bullet.fire()
                arcade.play_sound(self.laser_sound)
                #Fire the bullet here!

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)
            


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()

