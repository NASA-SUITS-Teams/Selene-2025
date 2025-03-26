import struct # used to create UDP Packet that contains commands

import time # used to get timestamp and pause key board input reciever

import socket  # used to communicate with UDP socket


class AutoMove:
# Command number	Command	Data input
# 1107	          Brakes	float: 0 or 1
# 1109	          Throttle	float: -100, 100
# 1110	          Steering	float: -1.0, 1.0

     def __init__(self):
          # self.throttle, self.brakes, self.steering = 0.0, False, 0.0
          # self.optimal_speed, self.minT, self.maxT = 3.6, 30, 100
          # self.TIR, self.SIR, self.speed = 3, 0.2, 0.0
          self.throttle = 0.0
          self.brakes = False
          self.steering = 0.0
          self.optimal_speed = 3.6
          self.minT = 30
          self.maxT = 100
          self.TIR = 3
          self.SIR = 0.2
          self.speed = 0.0
          self.north = (-5, 5)
          self.south = (-175, 175)
          self.east = (85, 95)
          self.west = (-85, -95)
          self.northeast = (40, 50)
          self.northwest = (-40, -50)
          self.southeast = (130, 140)
          self.southwest = (-130, -140)
          
     
     def sendCommand(self, command,value):
          if (command == 135 or command == 1109 or command == 1107 
          or command == 1110 or command == 131):
               # get timestamp
               timestamp = int(time.time())
          
               # creating packet that will be sent
               if command == 135 or command == 131:
                    data = struct.pack(">II", timestamp, command)
               else:
                    data = struct.pack(">IIf", timestamp, command, value)
          
               try: 
                    # sending UDP packet
                    udp_socket.sendto(data, (IP_address, Port))
               
               # error checking, ending program if error occurs in sending
               except socket.error as err:
                    print(f"Command was unsuccesfully sent: {err}")
                    print("Exiting program")
                    # closing UDP socket
                    udp_socket.close()
                    exit()
          else:
               print("command not found or not needed")

     def receiveCommand(self, command):
          self.sendCommand(command)
          # get speed or heading
          if command == 135 or command == 131:
               try:
                    data = udp_socket.recv(12)
                    rData = struct.unpack('>IIf', data)[2]
                    return rData
               
               except socket.error as err1:
                    print(f"speed was not received: {err2}")

               except struct.error as err2:
                    print(f"Error when unpacking speed: {err2}")

          # no command  
          else:
               print("command not found or not needed")
               return -1

     def maintain_speed(self):
          if self.speed > 0 and self.speed < 3.4:
               self.throttle += self.TIR
          if self.speed < 0 and self.speed > -3.4:
               self.throttle -= self.TIR
          self.sendCommand(1109, self.throttle)

     def steer_right(self):
          while self.SIR > self.steering:
               self.steering += self.SIR  
               self.sendCommand(1110, self.steering)

     def steer_half_right(self):
          while self.SIR > self.steering:
               self.steering += (self.SIR / 2)
               self.sendCommand(1110, self.steering)

     def stop_turning_right(self, turning):
          if self.steering != 0:
               self.steering -= self.SIR
               self.sendCommand(1110,self.steering)
          else:
               turning = False

     def stop_half_right(self, turning):
          if self.steering != 0:
               self.steering -= (self.SIR / 2)
               self.sendCommand(1110,self.steering)
          else:
               turning = False

     def steer_left(self):
          while -self.SIR < self.steering:
               self.steering -= self.SIR
               self.sendCommand(1110, self.steering)

     def steer_half_left(self):
          while -self.SIR < self.steering:
               self.steering -= (self.SIR)
               self.sendCommand(1110, self.steering)

     def stop_turning_left(self, turning):
          if self.steering != 0:
               self.steering += self.SIR
               self.sendCommand(1110,self.steering)
          else:
               turning = False

     def stop_half_left(self, turning):
          if self.steering != 0:
               self.steering += (self.SIR / 2)
               self.sendCommand(1110,self.steering)
          else:
               turning = False

     def stop(self):
          while self.speed > 1 or self.speed < 1:
               if self.speed < 0:
                    self.throttle += self.TIR
                    self.sendCommand(1109, self.throttle)
               else:
                    self.throttle -= self.TIR
                    self.sendCommand(1109, self.throttle)
          
          self.brakes = True
          self.sendCommand(1107, self.brakes)

          while self.throttle != 0:
               if self.throttle < 0:
                    self.throttle += self.TIR
               else:
                    self.throttle -= self.TIR

     def forward(self):
          while self.throttle < 30:
               self.throttle += self.TIR
               self.sendCommand(1109, self.throttle)
          
          while self.speed < 3.4 or self.speed > 3.8:
               if self.speed < 3.4:
                    self.throttle += self.TIR
                    self.sendCommand(1109, self.throttle)
               else:
                    self.throttle += self.TIR
                    self.sendCommand(1109, self.throttle)
          
     def backward(self):
          while self.throttle > -30:
               self.throttle -= self.TIR
               self.sendCommand(1109, self.throttle)
          
          while self.speed > -3.4 or self.speed < -3.8:
               if self.speed > -3.4:
                    self.throttle -= self.TIR
                    self.sendCommand(1109, self.throttle)
               else:
                    self.throttle += self.TIR
                    self.sendCommand(1109, self.throttle)

     def right(self):
          turning = True
          facing = self.receiveCommand(131)

          if facing > self.north[0] and facing < self.northeast[1]:
               self.steer_right()
               while turning:
                    self.maintain_speed()
                    # update facing to tss 
                    if(facing > self.east[0] and facing < self.east[1]):
                         self.stop_turning_right(turning)
          
          elif facing > self.east[0] and facing < self.southeast[1]:
               self.steer_right()
               while turning:
                    self.maintain_speed()
                    # update facing to tss 
                    if(facing < self.south[0] and facing > self.south[1]):
                         self.stop_turning_right(turning)

          elif facing > self.south[1] or facing < self.southwest[0]:
               self.steer_right()
               while turning:
                    self.maintain_speed()
                    # update facing to tss 
                    if(facing < self.west[0] and facing > self.west[1]):
                         self.stop_turning_right(turning)
          
          elif facing > self.west[1] or facing < self.northwest[0]:
               self.steer_right()
               while turning:
                    self.maintain_speed()
                    # update facing to tss 
                    if(facing > self.north[0] and facing < self.north[1]):
                         self.stop_turning_right(turning)

     def diagonal_right(self):
          turning = True

     def left(self):
          turning = True
          facing = self.receiveCommand(131)

          if facing > self.north[1] and facing < self.northwest[0]:
               self.steer_left()
               while turning:
                    self.maintain_speed()
                    # update facing to tss 
                    if(facing < self.west[0] and facing > self.west[1]):
                         self.stop_turning_left(turning)
          
          elif facing > self.west[0] and facing < self.southwest[1]:
               self.steer_left()
               while turning:
                    self.maintain_speed()
                    # update facing to tss 
                    if(facing < self.south[0] and facing > self.south[1]):
                         self.stop_turning_left(turning)

          elif facing > self.south[0] or facing < self.southeast[0]:
               self.steer_left()
               while turning:
                    self.maintain_speed()
                    # update facing to tss 
                    if(facing < self.west[0] and facing > self.west[1]):
                         self.stop_turning_left(turning)
          
          elif facing > self.east[1] or facing < self.northeast[0]:
               self.steer_left()
               while turning:
                    self.maintain_speed()
                    # update facing to tss 
                    if(facing > self.north[0] and facing < self.north[1]):
                         self.stop_turning_left(turning)

     def diagonal_left(self):
          turning = True


     def __del__(self):
          print("dang")



IP_address = " "     # TSS IP Address
Port = 14141         # TSS UDP Port
IP_address = input("Please enter IP address: ")

throttle = 0.0
brakes = 0
steering = 0.0

# initilizing UDP socket communication
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)