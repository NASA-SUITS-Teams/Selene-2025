import struct # used to create UDP Packet that contains commands

import time # used to get timestamp and pauses

import socket  # used to communicate with UDP socket

from Grid import Grid   # importing the Grid class

"""
CLASS: AutoMove
    AutoMove class is used to allow the movement of the DUST simulation
    NASA Pressurized Rover to be done autonomously. By having methods 
    that increase and decrease throttle, steering and toggle brakes to 
    move forward, backwards, turn or stop.
    
"""
class AutoMove:
# Command number	Command	Data input
# 1107	          Brakes	float: 0 or 1
# 1109	          Throttle	float: -100, 100
# 1110	          Steering	float: -1.0, 1.0

     """
    Name: __init__ (CONSTRUCTOR)
    
    INPUT: 
        N/A
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        Constructor that initializes the class attributes. 
    """
     def __init__(self,Grid:Grid,ipAddress):
          # These values are subject to change.
          # All of these can be found on the tss files, cardinal directions are
          # found as "heading" and go from 0 to 180 and 0 to -180.
          self.ipAddress = ipAddress
          self.Port = 14141
          self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
          self.Grid = Grid
          self.neighbor_index = [(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0)]
          self.throttle = 0.0
          self.brakes = 0
          self.steering = 0.0
          self.optimalSpeed = 3.6
          self.minT = 30
          self.maxT = 100
          self.TIR = 3
          self.SIR = 0.8
          self.speed = 0.0
          self.north = (-22.5, 22.4)
          self.south = (157.5, -157.6)
          self.east = (67.5, 112.4)
          self.west = (-112.5, -67.6)
          self.northeast = (22.5, 67.4)
          self.northwest = (-67.5, -22.6)
          self.southeast = (112.5, 157.4)
          self.southwest = (-157.5, -112.6)
          
     """
    Name: sendCommand
    
    INPUT: 
        command:        TSS command number
        value:          input data to be sent to TSS 
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This method will create a packet that will be sent to the TSS server
        in the given format (Timestamp|Command|Input) for movement, and 
        (Timestamp|Command) for everything else.
    """
     def sendCommand(self, command,value):
          # checking if the commands are movement commands, get speed or get heading
          # other commands are not needed for this.
          if (command == 133 or command == 1109 or command == 1107 
          or command == 1110 or command == 134 or command == 136 or command == 140):
               # get timestamp
               timestamp = int(time.time())
          
               # creating packet that will be sent 
               # rover movement commands are sent in a 12 byte packet
               # while the rest in a 8 byte. 
               if command == 135 or command == 131:
                    data = struct.pack(">II", timestamp, command)
               else:
                    data = struct.pack(">IIf", timestamp, command, value)
          
               try: 
                    # sending UDP packet
                    self.udpSocket.sendto(data, (self.ipAddress, self.Port))
               
               # error checking, ending program if error occurs in sending
               except socket.error as err:
                    print(f"Command was unsuccesfully sent: {err}")
                    print("Exiting program")
                    # closing UDP socket
                    self.udpSocket.close()
                    exit()
          else:
               print("command not found or not needed")

     """
    Name: receiveCommand
    
    INPUT: 
        command:        TSS command number
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This method will unpack the information received from the TSS based
        on the command number.
    """
     def receiveCommand(self, command):
          # call sendCommand to ask for data or move the rover.
          self.sendCommand(command, 0)
          time.sleep(1)

          # receiving speed or heading
          if command == 133 or command == 134 or command == 136 or command == 140:
               try:
                    data = self.udpSocket.recv(12)

                    # using indexing to just assign the third element of the
                    # tuple since that is what we need. timestamp and command
                    # number are not needed for now, but if we were to need 
                    # them we would just create 2 other variables.
                    rData = struct.unpack('>IIf', data)[2]
                    return rData
               
               # checking for errors
               except socket.error as err1:
                    print(f"data was not received: {err2}")

               except struct.error as err2:
                    print(f"Error when unpacking data: {err2}")

          # no command  
          else:
               print("command not found or not needed")
               return None

     """
    Name: increaseThrottle
    
    INPUT: 
        N/A
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This method will increase the throttle by TIR and also check
        to ensure that throttle does not surpass maximum potential throttle
     """
     def increaseThrottle(self):
        # check to ensure throtle does overflow
        if self.throttle + self.TIR > 100.0:  
            #if yes sets to maximum  
            self.throttle = 100.0
        else:
            # if no overflow then simply increment 
            self.throttle = self.throttle + self.TIR

     """
    Name: decreaseThrottle
    
    INPUT: 
        N/A
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This method will decrease the throttle by TIR and also check
        to ensure that throttle does not surpass minimum potential throttle
    """
     def decreaseThrottle(self):
        # check to ensure throtle does underflow
        if self.throttle - self.TIR < -100.0:
            #if yes sets to minimum
            self.throttle = -100.0
        else:
            # if no underflow then simply decrement 
            self.throttle = self.throttle - self.TIR


     """
    Name: maintainSpeed
    
    INPUT: 
       N/A
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This Method will ensure that the rover is moving at the desired speed.
    """
     def maintainSpeed(self):
          # if the speed is positive, that means the rover is moving
          # forward. If it's less than the desired speed, increase the throttle
          self.speed = self.receiveCommand(140)

          if self.speed >= 0 and self.speed < 3.4:
               self.increaseThrottle()
               self.sendCommand(1109, self.throttle)
               time.sleep(1)
          
          # if the speed is negative, rover moving backwards. decrease the throttle
          # if the speed is negative but greater than the desired speed.
          elif self.speed <= 0 and self.speed > -3.4:
               self.decreaseThrottle()
               self.sendCommand(1109, self.throttle)
               time.sleep(1)
          

     """
    Name: steerRight
    
    INPUT: 
       N/A
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This Method will increase the steering to turn right.
     """
     def steerRight(self):
          # adjust the steering to be that of the SIR
          while self.SIR > self.steering:
               self.steering += self.SIR  
               self.sendCommand(1110, self.steering)
               time.sleep(1)

     """
    Name: steerHalfRight
    
    INPUT: 
       N/A
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This Method will increase the steering to turn diagonally 
        to the right.
     """
     def steerHalfRight(self):
          # adjust the steering to be that of the SIR /2 (diagonal SIR) 
          while self.SIR > self.steering:
               self.steering += (self.SIR / 2)
               self.sendCommand(1110, self.steering)
               time.sleep(1)

     """
    Name: stopRight
    
    INPUT: 
       N/A
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This Method will decrease the steering to stop self.turning right
     """
     def stopRight(self):
          # adjust the steering so that it's equal to 0 decreasing it
          # by SIR
          if self.steering != 0:
               self.steering -= self.SIR
               self.sendCommand(1110,self.steering)
               time.sleep(1)
          else:
          # make self.turning = false to stop the loop in the right function
               self.turning = False

     """
    Name: stopHalfRight
    
    INPUT: 
       N/A
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This Method will decrease the steering to stop self.turning 
        diagonally right
     """
     def stopHalfRight(self):
          # adjust the steering so that it's equal to 0. 
          # decreasing it by SIR /2 (diagonal SIR)
          if self.steering != 0:
               self.steering -= (self.SIR / 2)
               self.sendCommand(1110,self.steering)
               time.sleep(1)
          else:
               self.turning = False

     """
    Name: steerLeft
    
    INPUT: 
       N/A
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This Method will decrease the steering to turn left.
        (negative steering means turning left)
     """
     def steerLeft(self):
           # adjust the steering to be that of negative SIR
           # negative steering means turning left
          while -self.SIR < self.steering:
               self.steering -= self.SIR
               self.sendCommand(1110, self.steering)
               time.sleep(1)

     """
    Name: steerHalfLeft
    
    INPUT: 
       N/A
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This Method will decrease the steering to turn diagonally
        to the left.
     """
     def steerHalfLeft(self):
           # adjust the steering to be that of negative SIR /2
          while -self.SIR < self.steering:
               self.steering -= (self.SIR / 2)
               self.sendCommand(1110, self.steering)
               time.sleep(1)

     """
    Name: stopLeft
    
    INPUT: 
       N/A
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This Method will increase the steering to 
        stop self.turning left.
     """
     def stopLeft(self):
          # adjust the steering so that it's equal to 0 increasing it
          # by SIR
          if self.steering != 0:
               self.steering += self.SIR
               self.sendCommand(1110,self.steering)
          else:
               self.turning = False

     """
    Name: stopHalfLeft
    
    INPUT: 
       N/A
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This Method will increase the steering to stop
        self.turning diagonally to the left
     """
     def stopHalfLeft(self):
          # adjust the steering so that it's equal to 0. 
          # increasing it by SIR /2 (diagonal SIR)
          if self.steering != 0:
               self.steering += (self.SIR / 2)
               self.sendCommand(1110,self.steering)
               time.sleep(1)
          else:
               self.turning = False

     """
    Name: stop
    
    INPUT: 
       N/A
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This Method will decrease or increase throttle depending on
        if the rover is going forward or backwards. Then toggles the 
        breaks to stop.
     """
     def stop(self):
          self.speed = self.receiveCommand(140)
          time.sleep(1)
     
          # decrease or increase the throttle to 0
          while self.throttle != 0:
               if self.throttle < 0:
                    self.increaseThrottle()
                    self.sendCommand(1109, self.throttle)
                    time.sleep(1)
               elif self.throttle > 0:
                    self.decreaseThrottle()
                    self.sendCommand(1109, self.throttle)
                    time.sleep(1)

          # toggle brakes
          self.toggleBrakes()
          self.sendCommand(1107, self.brakes)
          time.sleep(1)

     """
    Name: toggle_breakes
    
    INPUT: 
        N/A
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        Will turn toggle the breaks between on an off
    """
     def toggleBrakes(self):
        # switch to on if off
        if self.brakes == 0:
            self.brakes == 1
        # switch to off if on 
        elif self.brakes == 1:
            self.brakes == 0

     """
    Name: forward
    
    INPUT: 
       N/A
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This Method will move the rover forward and ensure it is moving
        at the desired speed.
     """
     def forward(self):
          # increase the throttle to min_T (minimum throttle to move)
          # if it's not already
          while self.throttle < 30:
               self.increaseThrottle()
               self.sendCommand(1109, self.throttle)
               time.sleep(1)
          self.maintainSpeed()

     """
    Name: forward
    
    INPUT: 
       N/A
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This Method will move the rover backwards and ensure it is moving
        at the desired speed.
     """
     def backward(self):
          # increase the throttle to -min_T (minimum throttle to move)
          # if it's not already. Negative since moving backwards is negative
          while self.throttle > -30:
               self.decreaseThrottle()
               self.sendCommand(1109, self.throttle)
               time.sleep(1)
          self.maintainSpeed()

     """
    Name: right
    
    INPUT: 
       N/A
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This is the main turn right method that will enable the rover to turn
        in that direction. Checks for heading to know where to head next.

     """
     def right(self):
          self.turning = True
          self.facing = self.receiveCommand(136)

          # if facing north, turn east 
          if self.facing > self.north[0] and self.facing < self.north[1]:
               print("we are in north.")
               self.steerRight()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.west[0] and self.facing < self.west[1]:
                              print("we are now facing west, going east")
                              self.stopRight()
                    else:
                         if self.facing > self.east[0] and self.facing < self.east[1]:
                              print("we now turned east.")
                              self.stopRight()
          
          # if facing northeast, turn southeast
          elif self.facing > self.northeast[0] and self.facing < self.northeast[1]:
               print("we are in northeast.")
               self.steerRight()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.northwest[0] and self.facing < self.northwest[1]:
                              print("we are now facing northwest, going southeast")
                              self.stopRight()
                    else:
                         if self.facing > self.southeast[0] and self.facing < self.southeast[1]:
                              print("we turned southeast.")
                              self.stopRight()

           # if facing east, turn south
          elif self.facing > self.east[0] and self.facing < self.east[1]:
               print("we are in east.")
               self.steerRight()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.north[0] and self.facing < self.north[1]:
                              self.stopRight()
                              print("we are now facing north, going south")
                    else:
                         if self.facing > self.south[0] or self.facing < self.south[1]:
                              self.stopRight()
                              print("we now turned south.")

          # if facing southeast, turn southwest
          elif self.facing > self.southeast[0] and self.facing < self.southeast[1]:
               print("we are in southeast.")
               self.steerRight()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.northeast[0] and self.facing < self.northeast[1]:
                              print("we are now facing northeast, going southwest")
                              self.stopRight()
                    else:
                         if self.facing > self.southwest[0] and self.facing < self.southwest[1]:
                              print("we now turned southwest.")
                              self.stopRight()

          # if facing south turn west
          elif self.facing > self.south[0] or self.facing < self.south[1]:
               print("we are in south.")
               self.steerRight()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136) 
                    if self.throttle < 0:
                         if self.facing > self.east[0] and self.facing < self.east[1]:
                              print("we are now facing east, going west")
                              self.stopRight()
                    else:
                         if self.facing > self.west[0] and self.facing < self.west[1]:
                              print("we now turned west.")
                              self.stopRight()
          
          # if facing southwest turn northwest
          elif self.facing > self.southwest[0] and self.facing < self.southwest[1]:
               print("we are in southwest.")
               self.steerRight()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.southeast[0] and self.facing < self.southeast[1]:
                              print("we are now facing southeast, going northwest")
                              self.stopRight()
                    else:
                         if self.facing > self.northwest[0] and self.facing < self.northwest[1]:
                              print("we now turned northwest.")
                              self.stopRight()

          # if facing west turn north
          elif self.facing > self.west[0] and self.facing < self.west[1]:
               print("we are in west.")
               self.steerRight()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.south[0] or self.facing < self.south[1]:
                              print("we are now facing south, going north")
                              self.stopRight()
                    else:
                         if self.facing > self.north[0] and self.facing < self.north[1]:
                              print("we now turned north.")
                              self.stopRight()

          # if facing northwest, turn to northeast
          else: 
               print("we are in northwest.")
               self.steerRight()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.southwest[0] and self.facing < self.southwest[1]:
                              print("we are now facing southwest, going northeast")
                              self.stopRight()
                    else:
                         if self.facing > self.northeast[0] and self.facing < self.northeast[1]:
                              print("we now turned northeast.")
                              self.stopRight()

     """
    Name: diagonal Right
    
    INPUT: 
       N/A
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This is the main turn diagonal right method that will enable the rover to turn
        in that direction. Checks for heading to know where to head next.
     """
     def diagonalRight(self):
          self.turning = True
          self.facing = self.receiveCommand(136)

          # if facing north turn northeast
          if self.facing > self.north[0] and self.facing < self.north[1]:
               print("we are in north.")
               self.steerHalfRight()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if(self.facing > self.northwest[0] and self.facing < self.northwest[1]):
                              print("we are now facing northwest, going southeast")
                              self.stopHalfRight()
                    else:
                         if(self.facing > self.northeast[0] and self.facing < self.northeast[1]):
                              print("we turned northeast.")
                              self.stopHalfRight()
          
          # if facing northeast turn east
          elif self.facing > self.northeast[0] and self.facing < self.northeast[1]:
               print("we are in northeast.")
               self.steerHalfRight()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.north[0] and self.facing < self.north[1]:
                              print("we are now facing north, going south")
                              self.stopHalfRight()
                    else:
                         if(self.facing > self.east[0] and self.facing < self.east[1]):
                              print("we turned east.")
                              self.stopHalfRight()

          # if facing east turn southeast
          elif self.facing > self.east[0] and self.facing < self.east[1]:
               print("we are in east.")
               self.steerHalfRight()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.northeast[0] and self.facing < self.northeast[1]:
                              print("we are now facing northeast, going southwest")
                              self.stopHalfRight()
                    else:
                         if(self.facing > self.southeast[0] and self.facing < self.southeast[1]):
                              print("we turned southeast.")
                              self.stopHalfRight()
          
          # if facing southeast turn south
          elif self.facing > self.southeast[0] and self.facing < self.southeast[1]:
               print("we are in southeast.")
               self.steerHalfRight()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.east[0] and self.facing < self.east[1]:
                              print("we are now facing east, going west")
                              self.stopHalfRight()
                    else:
                         if(self.facing > self.south[0] or self.facing < self.south[1]):
                              print("we turned south.")
                              self.stopHalfRight()

          # if facing south turn southwest
          elif self.facing > self.south[0] or self.facing < self.south[1]:
               print("we are in south.")
               self.steerHalfRight()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.southeast[0] and self.facing < self.southeast[1]:
                              print("we are now facing southeast, going northwest")
                              self.stopHalfRight()
                    else:
                         if(self.facing > self.southwest[0] and self.facing < self.southwest[1]):
                              print("we turned southwest.")
                              self.stopHalfRight()
          
          # if facing southwest turn west
          elif self.facing > self.southwest[0] and self.facing < self.southwest[1]:
               print("we are in southwest.")
               self.steerHalfRight()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.south[0] or self.facing < self.south[1]:
                              print("we are now facing south, going north")
                              self.stopHalfRight()
                    else:
                         if(self.facing > self.west[0] and self.facing < self.west[1]):
                              print("we turned west.")
                              self.stopHalfRight()

          # if facing west turn northwest
          elif self.facing > self.west[0] and self.facing < self.west[1]:
               print("we are in west.")
               self.steerHalfRight()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.southwest[0] and self.facing < self.southwest[1]:
                              print("we are now facing southwest, going northeast")
                              self.stopHalfRight()
                    else:
                         if(self.facing > self.northwest[0] and self.facing < self.northwest[1]):
                              print("we turned northwest.")
                              self.stopHalfRight()
          
          # if facing northwest turn north
          else:
               print("we are in northwest.")
               self.steerHalfRight()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.west[0] and self.facing < self.west[1]:
                              print("we are now facing west, going east")
                              self.stopHalfRight()
                    else:
                         if(self.facing > self.north[0] and self.facing < self.north[1]):
                              print("we turned north.")
                              self.stopHalfRight()

     
     """
    Name: left
    
    INPUT: 
       N/A
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This is the main turn left method that will enable the rover to turn
        in that direction. Checks for heading to know where to head next.
     """
     def left(self):
          self.turning = True
          self.facing = self.receiveCommand(136)

          # if facing north, turn west
          if self.facing > self.north[0] and self.facing < self.north[1]:
               print("we are facing north")
               self.steerLeft()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.east[0] and self.facing < self.east[1]:
                              print("we are now facing east, going west")
                              self.stopLeft()
                    else:
                         if self.facing > self.west[0] and self.facing < self.west[1]:
                              print("we turned west")
                              self.stopLeft()
          
          # if facing northwest turn southwest
          elif self.facing > self.northwest[0] and self.facing < self.northwest[1]:
               print("we are facing northwest")
               self.steerLeft()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.northeast[0] and self.facing < self.northeast[1]:
                              print("we are now facing northeast, going southwest")
                              self.stopLeft()
                    else:
                         if self.facing > self.southwest[0] and self.facing < self.southwest[1]:
                              print("we turned southwest")
                              self.stopLeft()

          # if facing between west, turn south
          elif self.facing > self.west[0] and self.facing < self.west[1]:
               print("we are facing west")
               self.steerLeft()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.north[0] and self.facing < self.north[1]:
                              print("we are now facing north, going south")
                              self.stopLeft()
                    else:
                         if self.facing > self.south[0] or self.facing < self.south[1]:
                              print("we turned south")
                              self.stopLeft()

           # if facing southwest turn southeast
          elif self.facing > self.southwest[0] and self.facing < self.southwest[1]:
               self.steerLeft()
               print("we are facing southwest")
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.northwest[0] and self.facing < self.northwest[1]:
                              print("we are now facing northwest, going southeast")
                              self.stopLeft()
                    else:
                         if self.facing > self.southeast[0] and self.facing < self.southeast[1]:
                              print("we turned southeast")
                              self.stopLeft()

          # if facing south, turn east
          elif self.facing > self.south[0] or self.facing < self.south[1]:
               print("we are facing south")
               self.steerLeft()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.west[0] and self.facing < self.west[1]:
                              print("we are now facing west, going east")
                              self.stopLeft()
                    else:
                         if(self.facing > self.east[0] and self.facing < self.east[1]):
                              print("we turned east")
                              self.stopLeft()
          
          # if facing southeast turn northeast
          elif self.facing > self.southeast[0] and self.facing < self.southeast[1]:
               print("we are facing southeast")
               self.steerLeft()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.southwest[0] and self.facing < self.southwest[1]:
                              print("we are now facing southwest, going northeast")
                              self.stopLeft()
                    else:
                         if self.facing > self.northeast[0] and self.facing < self.northeast[1]:
                              print("we turned northeast")
                              self.stopLeft()

          # if facing between east, turn north
          elif self.facing > self.east[0] and self.facing < self.east[1]:
               print("we are facing east")
               self.steerLeft()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.south[0] or self.facing < self.south[1]:
                              print("we are now facing south, going north")
                              self.stopLeft()
                    else:
                         if(self.facing > self.north[0] and self.facing < self.north[1]):
                              print("we turned north")
                              self.stopLeft()
          
          # if facing northeast turn northwest
          else:
               print("we are facing northeast")
               self.steerLeft()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.southeast[0] and self.facing < self.southeast[1]:
                              print("we are now facing southeast, going northwest")
                              self.stopLeft()
                    else:
                         if self.facing > self.northwest[0] and self.facing < self.northwest[1]:
                              print("we turned northwest")
                              self.stopLeft()

     """
    Name: diagonalLeft
    
    INPUT: 
       N/A
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This is the main turn diagonal left method that will enable the rover to turn
        in that direction. Checks for heading to know where to head next.
     """
     def diagonalLeft(self):
          self.turning = True
          self.facing = self.receiveCommand(136)

          # if facing north turn northwest
          if self.facing > self.north[0] and self.facing < self.north[1]:
               print("we are facing north")
               self.steerHalfLeft()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.northeast[0] and self.facing < self.northeast[1]:
                              print("we are now facing northeast, going southwest")
                              self.stopHalfLeft()
                    else:
                         if(self.facing > self.northwest[0] and self.facing < self.northwest[1]):
                              print("we turned northwest")
                              self.stopHalfLeft()
          
          # if facing northwest turn west
          elif self.facing > self.northwest[0] and self.facing < self.northwest[1]:
               print("we are facing northwest")
               self.steerHalfLeft()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.north[0] and self.facing < self.north[1]:
                              print("we are now facing north, going south")
                              self.stopHalfLeft()
                    else:
                         if(self.facing > self.west[0] and self.facing < self.west[1]):
                              print("we turned west")
                              self.stopHalfLeft()

          # if facing west turn southwest
          elif self.facing > self.west[0] and self.facing < self.west[1]:
               print("we are facing west")
               self.steerHalfLeft()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.northwest[0] and self.facing < self.northwest[1]:
                              print("we are now facing northwest, going southeast")
                              self.stopHalfLeft()
                    else:
                         if(self.facing > self.southwest[0] and self.facing < self.southwest[1]):
                              print("we turned southwest")
                              self.stopHalfLeft()
          
          # if facing southwest turn south
          elif self.facing > self.southwest[0] and self.facing < self.southwest[1]:
               self.steerHalfLeft()
               print("we are facing southwest")
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.west[0] and self.facing < self.west[1]:
                              print("we are now facing west, going east")
                              self.stopHalfLeft()
                    else:
                         if(self.facing > self.south[0] or self.facing < self.south[1]):
                              print("we turned south")
                              self.stopHalfLeft()

          # if facing south turn southeast
          elif self.facing > self.south[0] or self.facing < self.south[1]:
               print("we are facing south")
               self.steerHalfLeft()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.southwest[0] and self.facing < self.southwest[1]:
                              print("we are now facing southwest, going northeast")
                              self.stopHalfLeft()
                    else:
                         if(self.facing > self.southeast[0] and self.facing < self.southeast[1]):
                              print("we turned southeast")
                              self.stopHalfLeft()
          
          # if facing southeast turn east
          elif self.facing > self.southeast[0] and self.facing < self.southeast[1]:
               print("we are facing southeast")
               self.steerHalfLeft()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.south[0] or self.facing < self.south[1]:
                              print("we are now facing south, going north")
                              self.stopHalfLeft()
                    else:
                         if(self.facing > self.east[0] and self.facing < self.east[1]):
                              print("we turned east")
                              self.stopHalfLeft()

          # if facing east turn northeast
          elif self.facing > self.east[0] and self.facing < self.east[1]:
               print("we are facing east")
               self.steerHalfLeft()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.southeast[0] and self.facing < self.southeast[1]:
                              print("we are now facing southeast, going northwest")
                              self.stopHalfLeft()
                    else:
                         if(self.facing > self.northeast[0] and self.facing < self.northeast[1]):
                              print("we turned northeast")
                              self.stopHalfLeft()
          
          # if facing northeast turn north
          else:
               print("we are facing northeast")
               self.steerHalfLeft()
               while self.turning:
                    self.maintainSpeed()
                    self.facing = self.receiveCommand(136)
                    if self.throttle < 0:
                         if self.facing > self.east[0] and self.facing < self.east[1]:
                              print("we are now facing east, going west")
                              self.stopHalfLeft()
                    else:
                         if(self.facing > self.north[0] and self.facing < self.north[1]):
                              print("we turned north")
                              self.stopHalfLeft()
     """
    Name: findValidneighbors
    
    INPUT: 
       current: tuple[int,int]: tuple of ints representing the current position as a tuple
    
    RETURN: 
        neighbors: list of tuples that represent the neighboring cells of passed in tuple 
    
    DESCRIPTION:
        This function receives the current position as a tuple and finds all valid neighboring cells 
        ( not out of bounds) and stores that location as tuples else stores the non valid locations as 0s 

     """
     def findValidneigbors(self,current:tuple[int,int]):
          neighbors = []
          for indexes in self.neighbor_index:
               temp = (current[0]+indexes[0],current[1]+indexes[1])
               if self.Grid.isOutofBounds(temp):
                   neighbors.append(0)
               else:
                   neighbors.append(temp)
          return neighbors
     
     """
    Name: findCurrentheading
    
    INPUT: 
       N/A
    
    RETURN: 
        String/character: representing the cardinal direction the rover is currently facing
    
    DESCRIPTION:
        Finds the current heading of the rover from the TSS then 
        assigns a string value to represent where it is facing 
     """
     def findCurrentheading(self):
        self.facing = self.receiveCommand(136)
        if self.facing > self.north[0] and self.facing < self.north[1]:
             return "N"
        elif self.facing > self.northeast[0] and self.facing < self.northeast[1]:
             return "NE"
        elif self.facing > self.east[0] and self.facing < self.east[1]:
             return "E"
        elif self.facing > self.southeast[0] and self.facing < self.southeast[1]:
             return "SE"
        elif self.facing > self.south[0] or self.facing < self.south[1]:
             return "S"
        elif self.facing > self.southwest[0] and self.facing < self.southwest[1]:
             return "SW"
        elif self.facing > self.west[0] and self.facing < self.west[1]:
             return "W"
        elif self.facing > self.northwest[0] and self.facing < self.northwest[1]:
             return "NW"
        
     """
    Name: generateMovepattern()
    
    INPUT: 
       path: list of tuples generated from path planning class
    
    RETURN: 
        pattern: list of strings/characters to represent the movement pattern needed to get to the end of path
    
    DESCRIPTION:
        Generates a list of string which represent the series of movements the rover needs to make 
        to arrive at the end point of the path. only accounts for forward movement (Left,Right,Forward
        Diagonal left, Diagonal right). This does account for changing of where the rover may be 
        facing at the time. 
     """
     def generateMovepattern(self,path:list[tuple[int,int]]):
          pattern = []
          facing = self.findCurrentheading()
          n = 0
          for n in range(len(path)-1):
               current = path[n]
               neighbors = self.findValidneigbors(current)
               nextPosition = neighbors.index(path[n+1])
               if facing == "N":
                    if nextPosition == 0:
                         pattern.append("DL")
                         facing = "NW"
                    elif nextPosition == 1:
                         pattern.append("F")
                         facing = "N"
                    elif nextPosition == 2:
                         pattern.append("DR")
                         facing = "NE"
                    elif nextPosition == 3:
                         pattern.append("R")
                         facing = "E"
                    elif nextPosition == 7:
                         pattern.append("L")
                         facing = "W"
               elif facing == "NE":
                    if nextPosition == 0:
                         pattern.append("L")
                         facing = "NW"
                    elif nextPosition == 1:
                         pattern.append("DL")
                         facing = "N"
                    elif nextPosition == 2:
                         pattern.append("F")
                         facing = "NE"
                    elif nextPosition == 3:
                         pattern.append("DR")
                         facing = "E"
                    elif nextPosition == 4:
                         pattern.append("R")
                         facing = "SE"
               elif facing == "E":
                    if nextPosition == 1:
                         pattern.append("L")
                         facing = "N"
                    elif nextPosition == 2:
                         pattern.append("DL")
                         facing = "NE"
                    elif nextPosition == 3:
                         pattern.append("F")
                         facing = "E"
                    elif nextPosition == 4:
                         pattern.append("DR")
                         facing = "SE"
                    elif nextPosition == 5:
                         pattern.append("R")
                         facing = "S"
               elif facing == "SE":
                    if nextPosition == 2:
                         pattern.append("L")
                         facing = "NE"
                    elif nextPosition == 3:
                         pattern.append("DL")
                         facing = "E"
                    elif nextPosition == 4:
                         pattern.append("F")
                         facing = "SE"
                    elif nextPosition == 5:
                         pattern.append("DR")
                         facing = "S"
                    elif nextPosition == 6:
                         pattern.append("R")
                         facing = "SW"
               elif facing == "S":
                    if nextPosition == 3:
                         pattern.append("L")
                         facing = "E"
                    elif nextPosition == 4:
                         pattern.append("DL")
                         facing = "SE"
                    elif nextPosition == 5:
                         pattern.append("F")
                         facing = "S"
                    elif nextPosition == 6:
                         pattern.append("DR")
                         facing = "SW"
                    elif nextPosition == 7:
                         pattern.append("R")
                         facing = "W"
               elif facing == "SW":
                    if nextPosition == 0:
                         pattern.append("R")
                         facing = "NW"
                    elif nextPosition == 4:
                         pattern.append("L")
                         facing = "SE"
                    elif nextPosition == 5:
                         pattern.append("DL")
                         facing = "S"
                    elif nextPosition == 6:
                         pattern.append("F")
                         facing = "SW"
                    elif nextPosition == 7:
                         pattern.append("DR")
                         facing = "W"
               elif facing == "W":
                    if nextPosition == 0:
                         pattern.append("DR")
                         facing = "NW"
                    elif nextPosition == 1:
                         pattern.append("R")
                         facing = "N"
                    elif nextPosition == 5:
                         pattern.append("L")
                         facing = "S"
                    elif nextPosition == 6:
                         pattern.append("DL")
                         facing = "SW"
                    elif nextPosition == 7:
                         pattern.append("F")
                         facing = "W"
               elif facing == "NW":
                    if nextPosition == 0:
                         pattern.append("F")
                         facing = "NW"
                    elif nextPosition == 1:
                         pattern.append("DR")
                         facing = "N"
                    elif nextPosition == 2:
                         pattern.append("R")
                         facing = "NE"
                    elif nextPosition == 6:
                         pattern.append("L")
                         facing = "SW"
                    elif nextPosition == 7:
                         pattern.append("DL")
                         facing = "W"
          self.pattern = pattern
     
     """
    Name: moveThroughPattern()
    
    INPUT: 
       N/A
    
    RETURN: 
       N/A
    
    DESCRIPTION:
        using the pattern generated from generateMovepattern(), it moves 
        the rover making it follow the pattern by calling 
        the movement functions.
     """
     def moveThroughPattern(self):
          for turn in self.pattern:
               if turn == 'F':
                    self.forward()
                    time.sleep(2)
                    self.stop()
               elif turn == 'DR':
                    self.diagonalRight()
                    time.sleep(.5)
                    self.stop()
               elif turn == 'R':
                    self.right()
                    time.sleep(.5)
                    self.stop()
               elif turn == 'DL':
                    self.diagonalLeft()
                    time.sleep(.5)
                    self.stop()
               elif turn == 'L':
                    self.left()
                    time.sleep(.5)
                    self.stop()
                    
     def __del__(self):
          print("deleting instance of class")


## For Testing 
#ipAdress = " "     # TSS IP Address
#Port = 14141         # TSS UDP Port
#ipAdress = input("Please enter IP address: ")

# initilizing UDP socket communication
#udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#testing = Grid(110, 70, -5450, -6500, -9750, -10450)
#moving = AutoMove(testing)
#x = moving.receiveCommand(128)
#y = moving.receiveCommand(129)
#start = testing.convertCoords((x,y))
#print(start)
#path = [start, (86,36),(85,36),(85,37),(86,37),(87,37),(87,38)]
#moving.generateMovepattern(path)
#moving.moveThroughPattern()