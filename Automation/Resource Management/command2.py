# 

import struct # used to create UDP Packet that contains commands

import time # used to get timestamp and pause key board input reciever

import socket  # used to communicate with UDP socket

import json # used for saving data as json file.

import os # used for saving the json file locally.

import time # used for pausing the program to allow for data collection

class Command:
    def __init__(self):
          
        self.scriptDir = os.path.dirname(os.path.abspath(__file__))  # Get the script’s directory
        self.targetDir = os.path.abspath(os.path.join(self.scriptDir, "../../User_Interface/UI_Main/client/src/telemetry_json"))  # Move up two levels
        self.IP_address = " "     # TSS IP Address
        self.Port = 14141         # TSS UDP Port

        # initilizing UDP socket communication
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


        self.evaState = {
                        "eva": {
                            "started": False,
                            "paused": False,
                            "completed": False,
                            "total_time": 0,
                            "uia": {
                                "started": False,
                                "completed": False,
                                "time": 0
                            },
                            "dcu": {
                                "started": False,
                                "completed": False,
                                "time": 0
                            },
                            "rover": {
                                "started": False,
                                "completed": False,
                                "time": 0
                            },
                            "spec": {
                                "started": False,
                                "completed": False,
                                "time": 0
                            }
                        }
        }

        self.evaTelemetry = {
             "telemetry": 
             {
                "eva_time": 0,
                "eva1": {
                    "batt_time_left": 5077.148926,
                    "oxy_pri_storage": 23.755802,
                    "oxy_sec_storage": 15.489529,
                    "oxy_pri_pressure": 0.000000,
                    "oxy_sec_pressure": 0.000000,
                    "oxy_time_left": 4238,
                    "heart_rate": 90.000000,
                    "oxy_consumption": 0.000000,
                    "co2_production": 0.000000,
                    "suit_pressure_oxy": 3.072300,
                    "suit_pressure_co2": 0.005900,
                    "suit_pressure_other": 11.554200,
                    "suit_pressure_total": 14.632401,
                    "fan_pri_rpm": 0.000000,
                    "fan_sec_rpm": 0.000000,
                    "helmet_pressure_co2": 0.000000,
                    "scrubber_a_co2_storage": 0.000000,
                    "scrubber_b_co2_storage": 0.000000,
                    "temperature": 70.000000,
                    "coolant_ml": 20.508068,
                    "coolant_gas_pressure": 0.000000,
                    "coolant_liquid_pressure": 0.000000
                },
                "eva2": {
                    "batt_time_left": 3384.893799,
                    "oxy_pri_storage": 24.231962,
                    "oxy_sec_storage": 19.419136,
                    "oxy_pri_pressure": 0.000000,
                    "oxy_sec_pressure": 0.000000,
                    "oxy_time_left": 4714,
                    "heart_rate": 90.000000,
                    "oxy_consumption": 0.000000,
                    "co2_production": 0.000000,
                    "suit_pressure_oxy": 3.072300,
                    "suit_pressure_cO2": 0.005900,
                    "suit_pressure_other": 11.554200,
                    "suit_pressure_total": 14.632401,
                    "fan_pri_rpm": 0.000000,
                    "fan_sec_rpm": 0.000000,
                    "helmet_pressure_co2": 0.000000,
                    "scrubber_a_co2_storage": 0.000000,
                    "scrubber_b_co2_storage": 0.000000,
                    "temperature": 70.000000,
                    "coolant_ml": 22.034748,
                    "coolant_gas_pressure": 0.000000,
                    "coolant_liquid_pressure": 0.000000
                }
            }
        }

        self.uia = {
             "uia": 
             {
                "eva1_power":        False,
                "eva1_oxy":          False,
                "eva1_water_supply": False,
                "eva1_water_waste":  False,
                "eva2_power":        False,
                "eva2_oxy":          False,
                "eva2_water_supply": False,
                "eva2_water_waste":  False,
                "oxy_vent":          False,
                "depress":           False
            }
        }
        self.rover = {
             "rover": 
                {
                "posx": 0.000000,
                "posy": 0.000000,
                "poi_1_x": 0.000000,
                "poi_1_y": 0.000000,
                "poi_2_x": 0.000000,
                "poi_2_y": 0.000000,
                "poi_3_x": 0.000000,
                "poi_3_y": 0.000000
                }
        }
        self.dcu = {
             "dcu": 
             {
                "eva1": {
                    "batt": False,
                    "oxy": False,
                    "comm": False,
                    "fan": False,
                    "pump": False,
                    "co2": False
                },
                "eva2": {
                    "batt": False,
                    "oxy": False,
                    "comm": False,
                    "fan": False,
                    "pump": False,
                    "co2": False
                }
            }
        }


        # Stores positon fo the EVA.
        self.imu = {
             "imu": 
             {
                "eva1": {
                    "posx": 0.000000,
                    "posy": 0.000000,
                    "heading": 0.000000
                },
                "eva2": {
                    "posx": 0.000000,
                    "posy": 0.000000,
                    "heading": 0.000000
                }
            }
        }

      

        self.telemetry_data = {
            "pr_telemetry": {
                "ac_heating": False,
                "ac_cooling": False,
                "co2_scrubber": False,
                "lights_on": False,
                "internal_lights_on": False,
                "brakes": False,
                "in_sunlight": False,
                "throttle": 0,
                "steering": 0,
                "current_pos_x": 0,
                "current_pos_y": 0,
                "current_pos_alt": 0,
                "heading": 0,
                "pitch": 0,
                "roll": 0,
                "distance_traveled": 0,
                "speed": 0,
                "surface_incline": 0,
                "oxygen_tank": 100,
                "oxygen_pressure": 0,
                "oxygen_levels": 0,
                "fan_pri": True,
                "ac_fan_pri": 0,
                "ac_fan_sec": 0,
                "cabin_pressure": 4,
                "cabin_temperature": 22,
                "battery_level": 100,
                "power_consumption_rate": 0,
                "solar_panel_efficiency": 0,
                "external_temp": 0,
                "pr_coolant_level": 44.5,
                "pr_coolant_pressure": 500,
                "pr_coolant_tank": 100,
                "radiator": 0,
                "motor_power_consumption": 0,
                "terrain_condition": 0,
                "solar_panel_dust_accum": 0,
                "mission_elapsed_time": 0,
                "mission_planned_time": 0,
                "point_of_no_return": 0,
                "distance_from_base": 0,
                "switch_dest": False,
                "dest_x": 0,
                "dest_y": 0,
                "dest_z": 0,
                "dust_wiper": False,
                "lidar": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            }
        }

    def setIPAdress(self, ip):
         self.IP_address = ip
    """
        Name: sendCommand
        
        INPUT: 
            command:        TSS command number
        
        RETURN: 
            N/A
        
        DESCRIPTION:
            This method will create a packet that will be sent to the TSS server
            in the given format (Timestamp|Command)
    """
    def sendCommand(self,command):
            # get timestamp
            timestamp = int(time.time())
            
            # creating packet that will be sent
            data = struct.pack(">II", timestamp, command)
            try: 
                # sending UDP packet
                self.udp_socket.sendto(data, (self.IP_address, self.Port))
                
            # error checking, ending program if error occurs in sending
            except socket.error as err:
                print(f"Command was unsuccesfully sent: {err}")
                print("Exiting program")
                # closing UDP socket
                self.udp_socket.close()
                exit()
            
            response = self.receive_command(command)
            
            time.sleep(1)
            return response

        
    """
        Name: receive_command
        
        INPUT: 
            command:        TSS command number
        
        RETURN: s
            N/A
        
        DESCRIPTION:
            This method will receive a packet from the TSS and unpack it, returning
            the unpacked data. For anything but lidar: (timestamp | command number | value) 
            For lidar: (timestamp | command number | 13 float values)
        """
    def receive_command(self,command):
        # get lidar command (handle command 167 and 172 specifically)
        if command == 167 or command == 172: # Handle 167 and 172 (LIDAR)
            try:
                # Assuming LIDAR data for 167 is also 60 bytes and format >II13f
                # If command 167 has a different format/size than 172,
                # you'll need separate handling for 167.
                expected_size = 60
                if command == 167:
                     print("Receiving LIDAR data for command 167...")
                     # Verify actual size and format for command 167 from TSS docs
                     # For now, assuming it's the same as 172 (60 bytes, >II13f)
                     pass # Keep expected_size = 60

                elif command == 172:
                     print("Receiving LIDAR data for command 172...")
                     expected_size = 60 # Keep expected_size = 60


                dataR, address = self.udp_socket.recvfrom(expected_size)

                # Check if we received the expected amount of data
                if len(dataR) != expected_size:
                    print(f"Warning: Received {len(dataR)} bytes for command {command} instead of expected {expected_size} bytes")
                    # Return default values if data is incomplete
                    # Assuming LIDAR returns list of floats
                    return [0.0] * 13 # Use floats for default if expecting floats

                info = struct.unpack('>II13f', dataR)
                list_of_lidar = list(info[2:]) # Ensure it's a list of floats
                return list_of_lidar

            except struct.error as e:
                print(f"Error unpacking data for command {command}: {e}")
                print(f"Received {len(dataR)} bytes instead of expected {expected_size}")
                # Return default values if unpacking fails
                return [0.0] * 13 # Use floats for default if expecting floats

        # get other commands (excluding 167 and 172)
        elif command > 1: # Implicitly less than 167 and 172 due to previous check
            # recvfrom returns a tuple with the data and the address
            # of the sender. Could use recv() if we dont need the address
            data, address = self.udp_socket.recvfrom(12) # Assuming 12 bytes for these commands
            try:
                int_Timestamp, int_commandN, int_info = struct.unpack('>III', data)
                float_Timestamp, float_commandN, float_info = struct.unpack('>IIf', data)

                # unpacking the data...
                if (command >= 17 and command <= 47) or (command >= 58 and command <= 118) or (command >= 126 and command <= 139) or (command >= 141 and command <= 159) or (command >= 161 and command <= 163):
                    return float_info
                else:
                    return int_info
            except struct.error as e:
                 print(f"Error unpacking data for command {command}: {e}")
                 print(f"Received data length: {len(data)}")
                 return None # Or handle the error appropriately


        # no command
        else:
            return "command not found."
    #######################################################################################
    # def receive_command(self,command):
    #     # get commands
    #         if command < 173 and command > 1:
    #         # recvfrom returns a tuple with the data and the address 
    #         # of the sender. Could use recv() if we dont need the address
    #             data, address = self.udp_socket.recvfrom(12)
    #             int_Timestamp, int_commandN, int_info = struct.unpack('>III', data)
    #             float_Timestamp, float_commandN, float_info = struct.unpack('>IIf', data)

    #             # unpacking the data. Assigning three variables since the
    #             # data is sent to us as a tuple of 3 items. The actual data
    #             # from the json files is the 3rd item so that is what is returned here.
    #             # if assigning the whole unpacked data to just one variable,
    #             # when printed, it would look like (120, 119, 2.9994838)
    #             # (random numbers for the example) meaning (timestamp, command number, valuefromfile).
    #             # by assigning all 3 we get rid of the tuple. 
    #             if(command >= 17 and command <= 47) or (command >= 58 and command <= 118) or (command >= 126 and command <= 139) or (command >= 141 and command <= 159) or (command >= 161 and command <= 163):
    #                 return float_info
    #             else:
    #                 return int_info

    #         # get lidar command
    #         elif command == 167 or command == 172:
    #             try:
    #                     dataR, address = self.udp_socket.recvfrom(60)

    #                     # Check if we received the expected amount of data
    #                     if len(dataR) != 60:
    #                         print(f"Warning: Received {len(dataR)} bytes for LIDAR data instead of expected 60 bytes")
    #                         # Return default values if data is incomplete
    #                         return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            
    #                     info = struct.unpack('>II13f', dataR)
    #                     r_timestamp = info[0]
    #                     command_num = info[1]
    #                     list_of_lidar = info[2:]
    #                     return list_of_lidar
    #             except struct.error as e:
    #                     print(f"Error unpacking LIDAR data: {e}")
    #                     print(f"Received {len(dataR)} bytes instead of expected 60")
    #                     # Return default values if unpacking fails
    #                     return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #         # no command  
    #         else:
    #             return "command not found."

    """
        Name: getData
        
        INPUT: 
        N/A
        
        RETURN: 
            N/A
        
        DESCRIPTION:
            This Method will begin reading keystrokes and performing neccesary function
            based on key stroke entered
    """
    def getData(self):
        """
        Automatically fetches all telemetry data in sequence without requiring key input,
        then saves the collected data to a JSON file.
        """
        print("Starting data collection...")

        print("Getting DCU data...")
        # Getting DCU data for eva1.

        self.dcu["dcu"]["eva1"]["batt"] = self.sendCommand(2)
        self.dcu["dcu"]["eva1"]["oxy"] = self.sendCommand(3)
        self.dcu["dcu"]["eva1"]["comm"] = self.sendCommand(4)
        self.dcu["dcu"]["eva1"]["fan"] = self.sendCommand(5)
        self.dcu["dcu"]["eva1"]["pump"] = self.sendCommand(6)
        self.dcu["dcu"]["eva1"]["co2"] = self.sendCommand(7)



        # Getting DCU data for eva2.
        self.dcu["dcu"]["eva2"]["batt"] = self.sendCommand(8)
        self.dcu["dcu"]["eva2"]["oxy"] = self.sendCommand(9)
        self.dcu["dcu"]["eva2"]["comm"] = self.sendCommand(10)
        self.dcu["dcu"]["eva2"]["fan"] = self.sendCommand(11)
        self.dcu["dcu"]["eva2"]["pump"] = self.sendCommand(12)
        self.dcu["dcu"]["eva2"]["co2"] = self.sendCommand(13)



        print("Getting IMU data...")

        # Getting IMU data for eva1.
        self.imu["imu"]["eva1"]["posx"] = self.sendCommand(17)
        self.imu["imu"]["eva1"]["posy"] = self.sendCommand(18)
        self.imu["imu"]["eva1"]["heading"] = self.sendCommand(19)



        # Getting IMU data for eva2.
        self.imu["imu"]["eva2"]["posx"] = self.sendCommand(20)
        self.imu["imu"]["eva2"]["posy"] = self.sendCommand(21)
        self.imu["imu"]["eva2"]["heading"] = self.sendCommand(22)




        print("Getting Rover data...")

        # Getting position of rover.
        self.rover["rover"]["posx"] = self.sendCommand(23)
        self.rover["rover"]["posy"] = self.sendCommand(24)
        # self.rover["rover"]["poi_1_x"] = self.sendCommand(22)
        # self.rover["rover"]["poi_1_y"] = self.sendCommand(22)
        # self.rover["rover"]["poi_2_x"] = self.sendCommand(22)
        # self.rover["rover"]["poi_2_y"] = self.sendCommand(22)
        # self.rover["rover"]["poi_3_x"] = self.sendCommand(22)
        # self.rover["rover"]["poi_3_y"] = self.sendCommand(22)



        print("Getting UIA data...")

        # Getting UIA data.
        self.uia["uia"]["eva1_power"] = self.sendCommand(53)
        self.uia["uia"]["eva1_oxy"] = self.sendCommand(54)
        self.uia["uia"]["eva1_water_supply"] = self.sendCommand(55)
        self.uia["uia"]["eva1_water_waste"] = self.sendCommand(56)
        self.uia["uia"]["eva2_power"] = self.sendCommand(57)
        self.uia["uia"]["eva2_oxy"] = self.sendCommand(58)
        self.uia["uia"]["eva2_water_supply"] = self.sendCommand(59)
        self.uia["uia"]["eva2_water_waste"] = self.sendCommand(60)
        self.uia["uia"]["oxy_vent"] = self.sendCommand(61)
        self.uia["uia"]["depress"] = self.sendCommand(62)





        # Getting Telemetry for eva1.
        self.evaTelemetry["telemetry"]["eva_time"] = self.sendCommand(63)
        self.evaTelemetry["telemetry"]["eva1"]["batt_time_left"] = self.sendCommand(64)
        self.evaTelemetry["telemetry"]["eva1"]["oxy_pri_storage"] = self.sendCommand(65)
        self.evaTelemetry["telemetry"]["eva1"]["oxy_sec_storage"] = self.sendCommand(66)
        self.evaTelemetry["telemetry"]["eva1"]["oxy_pri_pressure"] = self.sendCommand(67)
        self.evaTelemetry["telemetry"]["eva1"]["oxy_sec_pressure"] = self.sendCommand(68)
        self.evaTelemetry["telemetry"]["eva1"]["oxy_time_left"] = self.sendCommand(69)
        self.evaTelemetry["telemetry"]["eva1"]["heart_rate"] = self.sendCommand(70)
        self.evaTelemetry["telemetry"]["eva1"]["oxy_consumption"] = self.sendCommand(71)
        self.evaTelemetry["telemetry"]["eva1"]["co2_production"] = self.sendCommand(72)
        self.evaTelemetry["telemetry"]["eva1"]["suit_pressure_oxy"] = self.sendCommand(73)
        self.evaTelemetry["telemetry"]["eva1"]["suit_pressure_co2"] = self.sendCommand(74)
        self.evaTelemetry["telemetry"]["eva1"]["suit_pressure_other"] = self.sendCommand(75)
        self.evaTelemetry["telemetry"]["eva1"]["suit_pressure_total"] = self.sendCommand(76)
        self.evaTelemetry["telemetry"]["eva1"]["fan_pri_rpm"] = self.sendCommand(77)
        self.evaTelemetry["telemetry"]["eva1"]["fan_sec_rpm"] = self.sendCommand(78)
        self.evaTelemetry["telemetry"]["eva1"]["helmet_pressure_co2"] = self.sendCommand(79)
        self.evaTelemetry["telemetry"]["eva1"]["scrubber_a_co2_storage"] = self.sendCommand(80)
        self.evaTelemetry["telemetry"]["eva1"]["scrubber_b_co2_storage"] = self.sendCommand(81)
        self.evaTelemetry["telemetry"]["eva1"]["temperature"] = self.sendCommand(82)
        self.evaTelemetry["telemetry"]["eva1"]["coolant_ml"] = self.sendCommand(83)
        self.evaTelemetry["telemetry"]["eva1"]["coolant_gas_pressure"] = self.sendCommand(84)
        self.evaTelemetry["telemetry"]["eva1"]["coolant_liquid_pressure"] = self.sendCommand(85)
        
        # Getting Telemetry for eva2.
        self.evaTelemetry["telemetry"]["eva2"]["batt_time_left"] = self.sendCommand(86)
        self.evaTelemetry["telemetry"]["eva2"]["oxy_pri_storage"] = self.sendCommand(87)
        self.evaTelemetry["telemetry"]["eva2"]["oxy_sec_storage"] = self.sendCommand(88)
        self.evaTelemetry["telemetry"]["eva2"]["oxy_pri_pressure"] = self.sendCommand(89)
        self.evaTelemetry["telemetry"]["eva2"]["oxy_sec_pressure"] = self.sendCommand(90)
        self.evaTelemetry["telemetry"]["eva2"]["oxy_time_left"] = self.sendCommand(91)
        self.evaTelemetry["telemetry"]["eva2"]["heart_rate"] = self.sendCommand(92)
        self.evaTelemetry["telemetry"]["eva2"]["oxy_consumption"] = self.sendCommand(93)
        self.evaTelemetry["telemetry"]["eva2"]["co2_production"] = self.sendCommand(94)
        self.evaTelemetry["telemetry"]["eva2"]["suit_pressure_oxy"] = self.sendCommand(95)
        self.evaTelemetry["telemetry"]["eva2"]["suit_pressure_co2"] = self.sendCommand(96)
        self.evaTelemetry["telemetry"]["eva2"]["suit_pressure_other"] = self.sendCommand(97)
        self.evaTelemetry["telemetry"]["eva2"]["suit_pressure_total"] = self.sendCommand(98)
        self.evaTelemetry["telemetry"]["eva2"]["fan_pri_rpm"] = self.sendCommand(99)
        self.evaTelemetry["telemetry"]["eva2"]["fan_sec_rpm"] = self.sendCommand(100)
        self.evaTelemetry["telemetry"]["eva2"]["helmet_pressure_co2"] = self.sendCommand(101)
        self.evaTelemetry["telemetry"]["eva2"]["scrubber_a_co2_storage"] = self.sendCommand(102)
        self.evaTelemetry["telemetry"]["eva2"]["scrubber_b_co2_storage"] = self.sendCommand(103)
        self.evaTelemetry["telemetry"]["eva2"]["temperature"] = self.sendCommand(104)
        self.evaTelemetry["telemetry"]["eva2"]["coolant_ml"] = self.sendCommand(105)
        self.evaTelemetry["telemetry"]["eva2"]["coolant_gas_pressure"] = self.sendCommand(106)
        self.evaTelemetry["telemetry"]["eva2"]["coolant_liquid_pressure"] = self.sendCommand(107)

        # Getting Eva state
        print("Getting Eva State data")

        self.evaState["eva"]["started"] = self.sendCommand(108)
        self.evaState["eva"]["paused"] = self.sendCommand(109)
        self.evaState["eva"]["completed"] = self.sendCommand(110)
        self.evaState["eva"]["total_time"] = self.sendCommand(111)
        self.evaState["eva"]["uia"]["started"] = self.sendCommand(112)
        self.evaState["eva"]["uia"]["completed"] = self.sendCommand(113)
        self.evaState["eva"]["uia"]["time"] = self.sendCommand(114)

        self.evaState["eva"]["dcu"]["started"] = self.sendCommand(115)
        self.evaState["eva"]["dcu"]["completed"] = self.sendCommand(116)
        self.evaState["eva"]["dcu"]["time"] = self.sendCommand(117)

        self.evaState["eva"]["rover"]["started"] = self.sendCommand(118)
        self.evaState["eva"]["rover"]["completed"] = self.sendCommand(119)
        self.evaState["eva"]["rover"]["time"] = self.sendCommand(120)

  

        self.evaState["eva"]["spec"]["started"] = self.sendCommand(121)
        self.evaState["eva"]["spec"]["completed"] = self.sendCommand(122)
        self.evaState["eva"]["spec"]["time"] = self.sendCommand(123)







        
        # Collecting AC and environmental system data
        print("Getting environmental control systems data...")
        self.telemetry_data["pr_telemetry"]["ac_heating"] = self.sendCommand(124)
        self.telemetry_data["pr_telemetry"]["ac_cooling"] = self.sendCommand(125)
        self.telemetry_data["pr_telemetry"]["co2_scrubber"] = self.sendCommand(126)
        self.telemetry_data["pr_telemetry"]["lights_on"] = self.sendCommand(127)
        self.telemetry_data["pr_telemetry"]["internal_lights_on"] = self.sendCommand(128)
        
        # Collecting rover control systems data
        print("Getting rover control systems data...")
        self.telemetry_data["pr_telemetry"]["brakes"] = self.sendCommand(129)
        self.telemetry_data["pr_telemetry"]["in_sunlight"] = self.sendCommand(130)
        self.telemetry_data["pr_telemetry"]["throttle"] = self.sendCommand(131)
        self.telemetry_data["pr_telemetry"]["steering"] = self.sendCommand(132)
        
        # Collecting position and orientation data
        print("Getting position and orientation data...")
        self.telemetry_data["pr_telemetry"]["current_pos_x"] = self.sendCommand(133)
        self.telemetry_data["pr_telemetry"]["current_pos_y"] = self.sendCommand(134)
        self.telemetry_data["pr_telemetry"]["current_pos_alt"] = self.sendCommand(135)
        self.telemetry_data["pr_telemetry"]["heading"] = self.sendCommand(136)
        self.telemetry_data["pr_telemetry"]["pitch"] = self.sendCommand(137)
        self.telemetry_data["pr_telemetry"]["roll"] = self.sendCommand(138)
        
        # Collecting movement and terrain data
        print("Getting movement and terrain data...")
        self.telemetry_data["pr_telemetry"]["distance_traveled"] = self.sendCommand(139)
        self.telemetry_data["pr_telemetry"]["speed"] = self.sendCommand(140)
        self.telemetry_data["pr_telemetry"]["surface_incline"] = self.sendCommand(141)
        
        # Collecting oxygen system data
        print("Getting oxygen system data...")
        self.telemetry_data["pr_telemetry"]["oxygen_tank"] = self.sendCommand(142)
        self.telemetry_data["pr_telemetry"]["oxygen_pressure"] = self.sendCommand(143)
        self.telemetry_data["pr_telemetry"]["oxygen_levels"] = self.sendCommand(144)
        
        # Collecting fan and cooling system data
        print("Getting fan and cooling system data...")
        self.telemetry_data["pr_telemetry"]["fan_pri"] = self.sendCommand(145)
        self.telemetry_data["pr_telemetry"]["ac_fan_pri"] = self.sendCommand(146)
        self.telemetry_data["pr_telemetry"]["ac_fan_sec"] = self.sendCommand(147)
        
        # Collecting cabin environment data
        print("Getting cabin environment data...")
        self.telemetry_data["pr_telemetry"]["cabin_pressure"] = self.sendCommand(148)
        self.telemetry_data["pr_telemetry"]["cabin_temperature"] = self.sendCommand(149)
        
        # Collecting power system data
        print("Getting power system data...")
        self.telemetry_data["pr_telemetry"]["battery_level"] = self.sendCommand(150)
        self.telemetry_data["pr_telemetry"]["power_consumption_rate"] = self.sendCommand(151)
        self.telemetry_data["pr_telemetry"]["solar_panel_efficiency"] = self.sendCommand(152)
        
        # Collecting external and coolant data
        print("Getting temperature and coolant data...")
        self.telemetry_data["pr_telemetry"]["external_temp"] = self.sendCommand(153)
        self.telemetry_data["pr_telemetry"]["pr_coolant_level"] = self.sendCommand(154)
        self.telemetry_data["pr_telemetry"]["pr_coolant_pressure"] = self.sendCommand(155)
        self.telemetry_data["pr_telemetry"]["pr_coolant_tank"] = self.sendCommand(156)
        self.telemetry_data["pr_telemetry"]["radiator"] = self.sendCommand(157)
        
        # Collecting power, terrain and solar data
        print("Getting motor, terrain, and solar panel data...")
        self.telemetry_data["pr_telemetry"]["motor_power_consumption"] = self.sendCommand(158)
        self.telemetry_data["pr_telemetry"]["terrain_condition"] = self.sendCommand(159)
        self.telemetry_data["pr_telemetry"]["solar_panel_dust_accum"] = self.sendCommand(160)
        
        # Collecting mission data
        print("Getting mission status data...")
        self.telemetry_data["pr_telemetry"]["mission_elapsed_time"] = self.sendCommand(161)
        self.telemetry_data["pr_telemetry"]["mission_planned_time"] = self.sendCommand(162)
        self.telemetry_data["pr_telemetry"]["point_of_no_return"] = self.sendCommand(163)
        self.telemetry_data["pr_telemetry"]["distance_from_base"] = self.sendCommand(164)
        
        # Collecting destination data
        print("Getting destination data...")
        self.telemetry_data["pr_telemetry"]["switch_dest"] = self.sendCommand(165)
        # self.telemetry_data["pr_telemetry"]["dest_x"] = self.sendCommand(166)
        # self.telemetry_data["pr_telemetry"]["dest_y"] = self.sendCommand(167)
        # self.telemetry_data["pr_telemetry"]["dest_z"] = self.sendCommand(168)

        # Getting lidar data
        print("Getting lidar data...")
        self.telemetry_data["pr_telemetry"]["lidar"] = self.sendCommand(167)
        
        # Collecting maintenance and simulation data
        print("Getting maintenance and simulation data...")
        self.telemetry_data["pr_telemetry"]["dust_wiper"] = self.sendCommand(169)

        time.sleep(1)
        
     
        
        # Save collected data to JSON file
        print("Saving data to JSON file...")
        self.saveJson(self.targetDir, "ROVER_TELEMETRY.json", self.telemetry_data)
        self.saveJson(self.targetDir, "TELEMETRY.json", self.evaTelemetry)
        self.saveJson(self.targetDir, "DCU.json", self.dcu)
        self.saveJson(self.targetDir, "IMU.json", self.imu)
        self.saveJson(self.targetDir, "UIA.json", self.uia)
        self.saveJson(self.targetDir, "ROVER.json", self.rover)
        self.saveJson(self.targetDir, "EVA.json", self.evaState)



        
        print("Data collection complete. Telemetry saved to ROVER_TELEMETRY.json")
        return self.telemetry_data


    # Saves the rover data to a specific directory as a json file.
    def saveJson(self, directory=None, filename="ROVER_TELEMETRY.json", data = None):

        # If no directory is specified, use the current working directory
        if directory is None:
            filepath = filename
        else:
            # Create the directory if it doesn't exist
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            # Combine directory and filename
            filepath = os.path.join(directory, filename)

        # Saves the rover telemetry data to ROVER_TELEMETRY.json if the file
        # does not exist then it is created. 
        # "w" indicates writing mode so the telemetry_data is being 
        # dumped into the file not read.
        with open(filepath, "w") as file:

            # json.dump indicates what is being written to the 
            # ROVER_TELEMETRY.json file indent=4 is just a format to make the 
            # json file easier to read.
            json.dump(data, file, indent=4)


command = Command()
IPAdress = input("Please enter IP address: ")

command.setIPAdress(IPAdress)

while True:
    command.getData()
