# PS 6: Simulating robots
#
# Name: Peter Bekins
# Date: 5/5/20
#
# This program demonstrates the use of simulation to model a
# scenario rather than an analytical solution. The situation
# involves the deployment of robot vacuums in a rectangular room
# to test the rate at which the room is cleaned in relation to
# to the number of robots and their movement strategy.

import math
import random

import ps6_visualize
import pylab

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)


# === Problem 1
# Design class and methods for Room and Robot

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.
        Initially, no tiles in the room have been cleaned.
        width: an integer > 0
        height: an integer > 0
        """
        self.width = int(width)
        self.height = int(height)
        self.tiles = {}
        # create dictionary of tiles keyed to tuples (x, y) with value = False (dirty)
        # using tuples rather than Position object because tiles need to be integers
        for x in range(self.width):
            for y in range(self.height):
                #print "<" + str(x) + ", " + str(y) + ">"
                self.tiles[(x, y)] = False

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.
        Assumes that POS represents a valid position inside this room.
        pos: a Position
        """

        # Position is float, while tiles are 1x1;
        # Convert to int to locate tile within which it lands
        x = int(pos.getX())
        y = int(pos.getY())
        self.tiles[(x, y)] = True
        #print "Cleaned tile at <" + str(x) + ", " + str(y) + ">"


    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.
        Assumes that (m, n) represents a valid tile inside the room.
        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.tiles[(m, n)]

    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.
        returns: an integer
        """
        return len(self.tiles)


    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.
        returns: an integer
        """
        clean_tiles = 0
        for tile in self.tiles.values():
            if tile == True:
                clean_tiles += 1

        return clean_tiles

    def getRandomPosition(self):
        """
        Return a random position inside the room.
        returns: a Position object.
        """
        width = self.width
        height = self.height
        x = round(random.uniform(0, width), 1)
        y = round(random.uniform(0, height), 1)
        pos = Position(x, y)
        return pos

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.
        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        w = self.width
        h = self.height
        x = pos.getX()
        y = pos.getY()
        #print "Position = <" + str(x) + ", " + str(y) + "> and room = " + str(w) + "x" + str(h)
        return ((0 <= x < w) and ( 0 <= y < h))

class Robot(object):
    """
    Represents a robot cleaning a particular room.
    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.
    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        # set a random start position
        self.position = self.room.getRandomPosition()
        # clean the first tile
        self.room.cleanTileAtPosition(self.position)
        # set a random direction (angle in degrees)
        self.direction = random.choice(range(360))

    def getRobotPosition(self):
        """
        Return the position of the robot.
        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.
        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.
        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.
        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.
        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """

        # This is handled by Robot Type so raise exception

        raise NotImplementedError


# === Problem 2
# Design subclass of Robot to handle movement strategy
#
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.
    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.
        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # This class moves in a straight line. Calculate a new position
        # based on current speed and direction
        new_pos = self.position.getNewPosition(self.direction, self.speed)
        # 1. If the new position is inside the bounds of the room "move" the robot
        # to the new position.
        if self.room.isPositionInRoom(new_pos):
            #print "New pos " + str(new_pos.getX()) + ", " + str(new_pos.getY())
            self.setRobotPosition(new_pos)
            self.room.cleanTileAtPosition(self.position)
        # 2. If not (i.e., the robot hits a wall) then pick a new direction
        # at random and "turn" the robot to the new direction
        else:
            # print "Robot hit a wall"
            new_direction = random.choice(range(360))
            self.setRobotDirection(new_direction)

#
# === Problem 3
# Implement a simulation of robots cleaning a room
#

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    total_steps = 0
    for n in range(num_trials):
        # 1. Create room of size W x H
        room = RectangularRoom(width, height)

        # 2. Create robots and add to list
        robots = []
        for i in range(num_robots):
            robot = robot_type(room, speed)
            robots.append(robot)

        # 3. Calculate current coverage (proportion of tiles cleaned)
        coverage = room.getNumCleanedTiles()/float(room.getNumTiles())
        # print "     Clean tiles = " + str(room.getNumCleanedTiles())
        # print "     Total tiles = " + str((room.getNumTiles()))
        # print "     Start coverage = " + str(coverage)

        # 4. Run simulation of robot movement until coverage hits minimum threshold
        steps = 0
        while coverage < min_coverage:
            for r in robots:
                r.updatePositionAndClean()
            coverage = room.getNumCleanedTiles() / float(room.getNumTiles())
            # print "Coverage at step " + str(step) + ": " + str(coverage)
            # print "     Clean tiles = " + str(room.getNumCleanedTiles())
            # print "     Total tiles = " + str((room.getNumTiles()))

            # Track steps it took to hit min coverage.
            # Total steps accumulate over all trials for average
            steps += 1
            total_steps += 1

        # print "Run " + str(n) + " took " + str (step) + " steps"

    avg_steps = total_steps/num_trials

    return avg_steps

#
# === Problem 4
# Run simulations with given parameters and plot average results
#
# 1) How long does it take to clean 80% of a 20x20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions:
#       20x20, 25x16, 40x10, 50x8, 80x5, and 100x4?
#

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    Assume 20x20 room and 80% min coverage
    """
    print "Running Plot 1"
    data = []
    for n in range(1, 11):
        steps = runSimulation(n, 1.0, 20, 20, 0.8, 100, StandardRobot)
        data.append(steps)

    pylab.figure()
    pylab.plot(range(1,11), data)
    pylab.xlabel("Number of Robots")
    pylab.ylabel("Clean Time")
    pylab.title("Relationship of Clean Time to Number of Robots")

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    Assume two robots and 80% min coverage
    """
    print "Running Plot 2"
    data = []
    rooms = [(20, 20), (25, 16), (40, 10), (50, 8), (80, 5), (100, 4)]
    labels = []

    for r in rooms:
        print "Simulating room size " + str(r)
        steps = runSimulation(2, 1.0, r[0], r[1], 0.8, 100, StandardRobot)
        data.append(steps)
        labels.append(float(r[0])/float(r[1]))

    pylab.figure()
    pylab.plot(labels, data)
    pylab.xlabel("Room Ratio (w/h)")
    pylab.ylabel("Seconds to 80% Clean")
    pylab.title("Relationship of Clean Time to Room Shape")


#
# === Problem 5
# Create new robot subclass to handle random movement strategy
#

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """

    def updatePositionAndClean(self):

        # This class moves randomly, so pick a new direction every cycle
        new_direction = random.choice(range(360))
        self.setRobotDirection(new_direction)

        # Calculate the new position based on this direction
        new_pos = self.position.getNewPosition(self.direction, self.speed)

        # If the new position is in the room, "move" the robot, otherwise
        # let the simulation cycle another step when the robot will pick its
        # new direction

        if self.room.isPositionInRoom(new_pos):
            #print "New pos " + str(new_pos.getX()) + ", " + str(new_pos.getY())
            self.setRobotPosition(new_pos)
            self.room.cleanTileAtPosition(new_pos)


#
# === Problem 6
#
# Run simulation to compare the standard and random movement strategies while
# varying the number of robots.
#

def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """

    print "Running Plot 3"
    data1 = []
    data2 = []

    # Compare each strategy with 1 to 10 robots
    for n in range(1, 11):
        print "Simulating " + str(n) + " robots"
        step1 = runSimulation(n, 1.0, 20, 20, 0.8, 10, StandardRobot)
        step2 = runSimulation(n, 1.0, 20, 20, 0.8, 10, RandomWalkRobot)
        data1.append(step1)
        data2.append(step2)

    #print data1
    #print data2

    pylab.figure()
    pylab.plot(range(1, 11), data1, label = 'Standard')
    pylab.plot(range(1, 11), data2, label = 'Random')
    pylab.xlabel("Number of Robots")
    pylab.ylabel("Clean Time")
    pylab.title("Relationship of Clean Time to Number of Robots")
    pylab.legend()

if __name__ == '__main__':
    showPlot1()
    showPlot2()
    showPlot3()
    pylab.show()