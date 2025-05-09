import csv
from datetime import datetime
# from Alert import Alert
import json
import os

class LogData:
    def __init__(self):
        # allLogs contains all the logs of the resources
        self.allLogs = {}

        self.index = 0

        self.current_time = 0.0

        self.status = {
            "oyggen": "SAFE",
            "battery": "SAFE",
            "co2": "SAFE",
            "coolant_storage": "SAFE",
            "temp": "SAFE",
        }

        self.oxygen = {
                    "oxygen_levels": 00.000000000000000,
                    "oxygen_tank": 0.00000000000000,
                    "oxygen_pressure": 0000.00000000000000,
                }
        self.battery ={
                "battery_level": 00.00000000000000,
                "power_consumption_rate": 0.0000000000000000000,
                "solar_panel_efficiency": 0.0,
                }
        # CO2 level tracking.
        self.co2 = {
                    "co2_scrubber": 0
                }

        # Coolant accounts for the water resource as well.
        self.coolant_storage = {
                    "pr_coolant_tank": 00.00000000000000,
                    "pr_coolant_level": 00.000000000000000,
                    "pr_coolant_pressure": 000.0000000000000,

                }
        
        self.temp = {
                    "cabin_temperature": 00.00000000000000,
                }

        # directories for saving and loading telemetry data
        self.savePath = "User_Interface/UI_Main/client/src/telemetry_json/log.json"
        self.loadPath = "User_Interface/UI_Main/client/src/telemetry_json/Essential_Telemetry.json"


    # Loads Json file from a specific directory.
    def loadJson(self):
            
            try:
                with open(self.loadPath, "r") as file:
                    print(f"Loading telemetry data from {self.loadPath}")
                    self.currentData = json.load(file)
                    print("JSON Data:")
                    print(json.dumps(self.currentData, indent=2))


            except FileNotFoundError:
                print(f"Error: File {self.loadPath} not found.")
                return None
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON in {self.loadPath}")
                return None
            

    # --NEEDS Prediction.py to be implemented--
    #def addAlert(self):
        # Unimplemented. Will rely on updated Prediction values and Alert class.
    #   self.file1.write(self.alert.timestamp, ": ", self.alert.resource,", ", self.alert.criticality, self.alert.alertmessage)
            

    def _log_values(self):
       # current_time variable looks into essential_telemetry map and mission_elapsed_time key
       self.current_time = self.currentData["essential_telemetry"].get("mission_elapsed_time")
       self.oxygen["oxygen_levels"] = self.currentData["essential_telemetry"].get("oxygen_levels")
       self.oxygen["oxygen_tank"] = self.currentData["essential_telemetry"].get("oxygen_tank")
       self.oxygen["oxygen_pressure"] = self.currentData["essential_telemetry"].get("oxygen_pressure")

       self.battery["battery_level"] = self.currentData["essential_telemetry"].get("battery_level")
       self.battery["power_consumption_rate"] = self.currentData["essential_telemetry"].get("power_consumption_rate")
       self.battery["solar_panel_efficiency"] = self.currentData["essential_telemetry"].get("solar_panel_efficiency")
       
       self.co2["co2_scrubber"] = self.currentData["essential_telemetry"].get("co2_scrubber")
       self.coolant_storage["pr_coolant_tank"] = self.currentData["essential_telemetry"].get("pr_coolant_tank")
       self.coolant_storage["pr_coolant_level"] = self.currentData["essential_telemetry"].get("pr_coolant_level")
       self.coolant_storage["pr_coolant_pressure"] = self.currentData["essential_telemetry"].get("pr_coolant_pressure")
       self.temp["cabin_temperature"] = self.currentData["essential_telemetry"].get("cabin_temperature")

       self.logStatus()

       # log_entry contains a temporary copy of all major resources needed to be logged
       log_entry = {
           "mission_elapsed_time": self.current_time,
           "oxygen_status": self.status["oxygen"],
           "oxygen": self.oxygen.copy(),
            "battery_status": self.status["battery"],
            "battery": self.battery.copy(),
            "co2_status": self.status["co2"],
            "co2": self.co2.copy(),
            "coolant_storage_status": self.status["coolant_storage"],
            "coolant_storage": self.coolant_storage.copy(),
            "temp_status": self.status["temp"],
            "temp": self.temp.copy()
       }

        # allLogs contains the log entry copy within the current available index
       self.allLogs[self.index] = log_entry

        # self.index is moved to the next empty spot in the allLogs dictionary
       self.index += 1


    # 1 - Key for stats of log one, 2 - Key for stats of log two, etc.
    # def retrieve_past_data(self, variable, limit=None):
        #Retrieve past data for a specific variable.
        # data = []
        # with open(self.log_file, mode='r') as file:
        #     reader = csv.reader(file)
        #     for row in reader:  
        #         timestamp = row[0]

        #         if variable == 'o2_pri_storage':
        #             value = row[1]
                
        #         elif variable == 'o2_sec_storage':
        #             value = row[2]

        #         elif variable == 'o2_pri_pressure':
        #             value = row[3]

        #         elif variable == 'o2_sec_pressure':
        #             value = row[4]

        #         elif variable == 'battery':
        #             value = row[5]

        #         elif variable == 'water':
        #             value = row[6]

        #         elif variable == 'co2':
        #             value = row[7]

        #         elif variable == 'coolant':
        #             value = row[8]
                
        #         elif variable == 'temp':
        #             value = row[9]

        #         else:
        #             raise ValueError("Invalid variable specified.")
        #         data.append((timestamp, value))

        # if limit is not None:    # Gets all data from a variable 
        #     data = data[-limit:] # If user does not specify a limit

        # return data

    # saveJson is essential the same as method from the Resource file, however, it handles the allLogs dictionary
    def saveJson(self, directory=None, filename="allLogs.json", data = None):

        if directory is None:
            filepath = filename
        else:
            if not os.path.exists(directory):
                os.makedirs(directory)

            filepath = os.path.join(directory, filename)

        with open(filepath, "w") as file:
            json.dump(self.allLogs, file, indent=4)
            print(f"Log data saved to {filepath}")
            print("Log Data:")
            print(json.dumps(self.allLogs, indent=2))

    def logStatus(self):
        # Caution 45%, Warning 25%, Critical 10%

        # Whenver any resource is below 45%, it is considered a caution.
        # Whenver any resource is below 25%, it is considered a warning.
        # Whenver any resource is below 10%, it is considered a critical.
        # This is to make the status consistent for now as a prototype.

        # The values are multiplied by 0.01 to convert them to a percentage.
        # Some of the resources are multiplied by a factor to convert them to percentage 1.00 to 0.00 
        # because of some of the default values for these resources would be 
        # 0.209 or .000005 for example if they were not multiplied by a factor of some sort.
        
        if self.oxygen["oxygen_levels"] * 0.01 * 5 < 0.10:
            self.status["oxygen"] = "CRITICAL"
        elif self.oxygen["oxygen_levels"] * 0.01 * 5< 0.25:
            self.status["oxygen"] = "WARNING"
        elif self.oxygen["oxygen_levels"] * 0.01 * 5< 0.45:
            self.status["oxygen"] = "CAUTION"
        

        elif self.oxygen["oxygen_tank"] * 0.01< 0.10:
            self.status["oxygen"] = "CRITICAL"
        elif self.oxygen["oxygen_tank"] * 0.01< 0.25:
            self.status["oxygen"] = "WARNING"
        elif self.oxygen["oxygen_tank"] * 0.01< 0.45:
            self.status["oxygen"] = "CAUTION"

        elif self.oxygen["oxygen_pressure"] * 0.0001 * 3.3< 0.10:
            self.status["oxygen"] = "CRITICAL"
        elif self.oxygen["oxygen_pressure"] * 0.0001 * 3.3< 0.25:
            self.status["oxygen"] = "WARNING"
        elif self.oxygen["oxygen_pressure"] * 0.0001 * 3.3< 0.45:
            self.status["oxygen"] = "CAUTION"
        else:
            self.status["oxygen"] = "SAFE"
        
        
        if self.battery["battery_level"] * 0.01< 0.10:
            self.status["battery"] = "CRITICAL"
        elif self.battery["battery_level"] * 0.01< 0.25:
            self.status["battery"] = "WARNING"
        elif self.battery["battery_level"] * 0.01< 0.45:
            self.status["battery"] = "CAUTION"
        
        
        
        elif self.battery["power_consumption_rate"] * 2000 < 0.10:
            self.status["battery"] = "CRITICAL"
        elif self.battery["power_consumption_rate"] * 2000< 0.25:
            self.status["battery"] = "WARNING"
        elif self.battery["power_consumption_rate"] * 2000< 0.45:
            self.status["battery"] = "CAUTION"
        

        # Solar panel efficiency seems to always be at zero so this is 
        # commented out for now.

        # elif self.battery["solar_panel_efficiency"] * 0.01< 0.10:
        #     self.status["battery"] = "CRITICAL"
        # elif self.battery["solar_panel_efficiency"] * 0.01< 0.25:
        #     self.status["battery"] = "WARNING"
        # elif self.battery["solar_panel_efficiency"] * 0.01< 0.45:
        #     self.status["battery"] = "CAUTION"

        else:
            self.status["battery"] = "SAFE"
        
        # CO2 scrubber efficiency is always at 0.0 so this is commented out for now.
        # if self.co2["co2_scrubber"] * 0.01> 0.90:
        #     self.status["co2"] = "CRITICAL"
        # elif self.co2["co2_scrubber"] * 0.01 > 0.65:
        #     self.status["co2"] = "WARNING"
        # elif self.co2["co2_scrubber"] * 0.01 > 0.45:
        #     self.status["co2"] = "CAUTION"
        # else:
        #     self.status["co2"] = "SAFE"
        

        if self.coolant_storage["pr_coolant_tank"] * 0.01< 0.10:
            self.status["coolant_storage"] = "CRITICAL"
        elif self.coolant_storage["pr_coolant_tank"] * 0.01< 0.25:
            self.status["coolant_storage"] = "WARNING"
        
        elif self.coolant_storage["pr_coolant_tank"] * 0.01< 0.45:
            self.status["coolant_storage"] = "CAUTION"
        
        

        elif self.coolant_storage["pr_coolant_level"] * 0.01 * 2.25< 0.10:
            self.status["coolant_storage"] = "CRITICAL"
        elif self.coolant_storage["pr_coolant_level"] * 0.01 * 2.25< 0.25:
            self.status["coolant_storage"] = "WARNING"
        
        elif self.coolant_storage["pr_coolant_level"] * 0.01 * 2.25< 0.45:
            self.status["coolant_storage"] = "CAUTION"
        

        elif self.coolant_storage["pr_coolant_pressure"] * 0.001 * 3.2< 0.10:
            self.status["coolant_storage"] = "CRITICAL"
        elif self.coolant_storage["pr_coolant_pressure"] * 0.001 * 3.2< 0.25:
            self.status["coolant_storage"] = "WARNING"
        
        elif self.coolant_storage["pr_coolant_pressure"] * 0.001 * 3.2< 0.45:
            self.status["coolant_storage"] = "CAUTION"
        else:
            self.status["coolant_storage"] = "SAFE"
        
        
        if self.temp["cabin_temperature"] * 0.01 * 7.25< 0.10:
            self.status["temp"] = "CRITICAL"
        elif self.temp["cabin_temperature"] * 0.01 * 7.25< 0.25:
            self.status["temp"] = "WARNING"
        
        elif self.temp["cabin_temperature"] * 0.01 * 7.25< 0.45:
            self.status["temp"] = "CAUTION"
        else:
            self.status["temp"] = "SAFE"
       


log = LogData()
log.loadJson()
log._log_values()
log.saveJson("User_Interface/UI_Main/client/src/telemetry_json/")
log._log_values()
log.saveJson("User_Interface/UI_Main/client/src/telemetry_json/")
log._log_values()
log.saveJson("User_Interface/UI_Main/client/src/telemetry_json/")
log._log_values()
log.saveJson("User_Interface/UI_Main/client/src/telemetry_json/")
