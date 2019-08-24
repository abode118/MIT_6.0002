# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 15:48:35 2019

@author: abode
"""

# -*- coding: utf-8 -*-
# Problem Set 3: Simulating robots
# Name: Thang Tran
# Collaborators (discussion):Thang Tran
# Time: is relative

import math
import random

import ps3_visualize
import pylab

# For python 2.7:
from ps3_verify_movement27 import test_robot_movement


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.
        Does NOT test whether the returned position fits inside the room.
        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed
        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()
        
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        
        return Position(new_x, new_y)

    def __str__(self):  
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.
    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dirt. The tile is considered clean only when the amount
    of dirt on this tile is 0.
    """
    def __init__(self, width, height, dirt_amount):
        """
        Initializes a rectangular room with the specified width, height, and 
        dirt_amount on each tile.
        width: an integer > 0
        height: an integer > 0
        dirt_amount: an integer >= 0
        """
        self.width = width
        self.height = height
        self.dirt_amount = dirt_amount
        self.titles = {}
        for x in range(width):
            for y in range(height):
                self.titles[(x, y)] = dirt_amount
    
    def clean_tile_at_position(self, pos, capacity):
        """
        Mark the tile under the position pos as cleaned by capacity amount of dirt.
        Assumes that pos represents a valid position inside this room.
        pos: a Position object
        capacity: the amount of dirt to be cleaned in a single time-step
                  can be negative which would mean adding dirt to the tile
        Note: The amount of dirt on each tile should be NON-NEGATIVE.
              If the capacity exceeds the amount of dirt on the tile, mark it as 0.
        """

        if capacity >= self.titles[(math.floor(pos.x), math.floor(pos.y))]:
            self.titles[(math.floor(pos.x), math.floor(pos.y))] = 0
        elif capacity < 0:
            self.titles[(math.floor(pos.x), math.floor(pos.y))] -= capacity
        else:
            self.titles[(math.floor(pos.x), math.floor(pos.y))] -= capacity

    def is_tile_cleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.
        Assumes that (m, n) represents a valid tile inside the room.
        m: an integer
        n: an integer
        
        Returns: True if the tile (m, n) is cleaned, False otherwise
        Note: The tile is considered clean only when the amount of dirt on this
              tile is 0.
        """
        if self.titles[(m, n)] == 0:
            return True
        else:
            return False


    def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        cleantitles = list(self.titles.values())
        return cleantitles.count(0)
          
    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.
        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        if (math.floor(pos.x), math.floor(pos.y)) in self.titles.keys():
            return True
        else:
            return False

    def get_dirt_amount(self, m, n):
        """
        Return the amount of dirt on the tile (m, n)
        
        Assumes that (m, n) represents a valid tile inside the room.
        m: an integer
        n: an integer
        Returns: an integer
        """
        return self.titles[(m, n)]
        
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        # do not change -- implement in subclasses.
        raise NotImplementedError
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        returns: True if pos is in the room and (in the case of FurnishedRoom) 
                 if position is unfurnished, False otherwise.
        """
        # do not change -- implement in subclasses
        raise NotImplementedError

    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        # do not change -- implement in subclasses
        raise NotImplementedError


class Robot(object):
    """
    Represents a robot cleaning a particular room.
    At all times, the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning capacity.
    Subclasses of Robot should provide movement strategies by implementing
    update_position_and_clean, which simulates a single time-step.
    """
    def __init__(self, room, speed, capacity):
        """
        Initializes a Robot with the given speed and given cleaning capacity in the 
        specified room. The robot initially has a random direction and a random 
        position in the room.
        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        capacity: a positive interger; the amount of dirt cleaned by the robot 
                  in a single time-step
        """
        self.speed = speed
        self.capacity = capacity
        self.room = room
        self.d = random.uniform(0, 360)
        self.pos = Position(random.uniform(0, room.width), random.uniform(0, room.height))

    def get_robot_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        return self.pos

    def get_robot_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.d 

    def set_robot_position(self, position):
        """
        Set the position of the robot to position.
        position: a Position object.
        """
        self.pos = position
        return self.pos

    def set_robot_direction(self, direction):
        """
        Set the direction of the robot to direction.
        direction: float representing an angle in degrees
        """
        self.d = direction
        return self.d

    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.
        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and mark the tile it is on as having
        been cleaned by capacity amount. 
        """
        # do not change -- implement in subclasses
        raise NotImplementedError

# === Problem 2
class EmptyRoom(RectangularRoom):
    """
    An EmptyRoom represents a RectangularRoom with no furniture.
    """

    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        return len(self.titles.values())
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        Returns: True if pos is in the room, False otherwise.
        """
        return self.is_position_in_room(pos)
        
    def get_random_position(self):
        """
        Returns: a Position object; a valid random position (inside the room).
        """
        return Position(random.uniform(0, self.width), random.uniform(0, self.height))

class FurnishedRoom(RectangularRoom):
    """
    A FurnishedRoom represents a RectangularRoom with a rectangular piece of 
    furniture. The robot should not be able to land on these furniture tiles.
    """
    def __init__(self, width, height, dirt_amount):
        """ 
        Initializes a FurnishedRoom, a subclass of RectangularRoom. FurnishedRoom
        also has a list of tiles which are furnished (furniture_tiles).
        """
        # This __init__ method is implemented for you -- do not change.
        
        # Call the __init__ method for the parent class
        RectangularRoom.__init__(self, width, height, dirt_amount)
        # Adds the data structure to contain the list of furnished tiles
        self.furniture_tiles = []
        
    def add_furniture_to_room(self):
        """
        Add a rectangular piece of furniture to the room. Furnished tiles are stored 
        as (x, y) tuples in the list furniture_tiles 
        
        Furniture location and size is randomly selected. Width and height are selected
        so that the piece of furniture fits within the room and does not occupy the 
        entire room. Position is selected by randomly selecting the location of the 
        bottom left corner of the piece of furniture so that the entire piece of 
        furniture lies in the room.
        """
        # This addFurnitureToRoom method is implemented for you. Do not change it.
        furniture_width = random.randint(1, self.width - 1)
        furniture_height = random.randint(1, self.height - 1)

        # Randomly choose bottom left corner of the furniture item.    
        f_bottom_left_x = random.randint(0, self.width - furniture_width)
        f_bottom_left_y = random.randint(0, self.height - furniture_height)

        # Fill list with tuples of furniture tiles.
        for i in range(f_bottom_left_x, f_bottom_left_x + furniture_width):
            for j in range(f_bottom_left_y, f_bottom_left_y + furniture_height):
                self.furniture_tiles.append((i,j))             

    def is_tile_furnished(self, m, n):
        """
        Return True if tile (m, n) is furnished.
        """
        if (m, n) in self.furniture_tiles:
            return True
        else:
            return False
        
    def is_position_furnished(self, pos):
        """
        pos: a Position object.
        Returns True if pos is furnished and False otherwise
        """
        if (math.floor(pos.x), math.floor(pos.y)) in self.furniture_tiles:
            return True
        else:
            return False
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        returns: True if pos is in the room and is unfurnished, False otherwise.
        """
        if self.is_position_in_room(pos) and not self.is_position_furnished(pos):
            return True
        else:
            return False
        
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room that can be accessed.
        """
        num = 0
        for fur in self.furniture_tiles:
            if fur in self.titles.keys():
                num += 1
        return num
        
    def get_random_position(self):
        """
        Returns: a Position object; a valid random position (inside the room and not in a furnished area).
        """
        while True:
            p = Position(random.uniform(0, self.width), random.uniform(0, self.height))
            if not self.is_position_furnished(p):
                break
        return p

# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.
    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall or furtniture, it *instead*
    chooses a new direction randomly.
    """
    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.
        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and clean the dirt on the tile
        by its given capacity. 
        """

        new_p = self.get_robot_position().get_new_position(self.get_robot_direction(), self.speed)
        self.set_robot_position(new_p)
        if self.room.get_num_tiles() == self.room.width * self.room.height:
            while self.room.is_position_in_room(self.pos) == False:
                    self.set_robot_direction(random.uniform(0, 360))
                    self.set_robot_position(self.pos.get_new_position(self.d, self.speed))
        else:
            while self.room.is_position_in_room(self.pos) == False or self.room.is_position_furnished(self.pos) == True:
                self.set_robot_direction(random.uniform(0, 360))
                self.set_robot_position(self.pos.get_new_position(self.d, self.speed))
        self.room.clean_tile_at_position(self.pos, self.capacity)

# Uncomment this line to see your implementation of StandardRobot in action!
test_robot_movement(StandardRobot, EmptyRoom)
# test_robot_movement(StandardRobot, FurnishedRoom)