
import json
import os
import time

# Gets the monitored values for resources and stores and processes them here.
class Resource:

# oxygen has primary storage, secondary storage, primary partial pressure, and secondary partial pressure
# battery has time left
# water has amount left
# co2 has amount left
# coolant_storage has amount left
    def __init__(self):
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


        # Co2 levels are indicated through the co2 scrubber. 
        self.co2 = 0

        # Coolant accounts for the water resource as well.
        self.coolant_storage = {
            "pr_coolant_tank": 00.00000000000000,
            "pr_coolant_level": 00.000000000000000,
            "pr_coolant_pressure": 000.0000000000000,

        }
        self.temp = 00.000000000000000,

        self.path = "User_Interface/UI_Main/client/src/telemetry_json/ROVER_TELEMETRY.json"
        self.savePath = "User_Interface/UI_Main/client/src/telemetry_json/"
        self.macPath = "../../User_Interface/UI_Main/client/src/telemetry_json/"

        self.essentialTelemetry = {
            "essential_telemetry": {
                "mission_elapsed_time": 0000.0,
                "oxygen_levels": 00.000000000000000,
                "oxygen_tank": 0.00000000000000,
                "oxygen_pressure": 0000.00000000000000,
                "battery_level": 00.00000000000000,
                "power_consumption_rate": 0.0000000000000000000,
                "solar_panel_efficiency": 0.0,
                "pr_coolant_tank": 00.00000000000000,
                "pr_coolant_level": 00.000000000000000,
                "pr_coolant_pressure": 000.0000000000000,

            }
        }

        self.currentData = None
        self.oldDataFile = None

    # Saves the rover data to a specific directory as a json file.
    def saveJson(self, directory=None, filename="Essential_Telemetry.json", data = None):

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
            print(f"essential Telemetry data saved to {filepath}")
            print("essential Telemetry Data:")
            print(json.dumps(self.currentData, indent=2))


    def loadJson(self):
         
        try:
            with open(self.path, 'r') as file:
                print(f"Loading telemetry data from {self.path}")
                self.currentData = json.load(file)
                print("JSON Data:")
                print(json.dumps(self.currentData, indent=2))


        except FileNotFoundError:
            print(f"Error: File {self.path} not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {self.path}")
            return None
        
    def monitorData(self):
        print(f"Monitoring file: ROVER_TELEMETRY.json")

        currentFileModificationTime = os.path.getmtime(self.path)
        # Check if the file has been modified since last check
        if self.oldDataFile is None or currentFileModificationTime != self.oldDataFile:
            print("\n--- File Updated ---")
            self.loadJson()  # Reload the JSON data
            self.oldDataFile = currentFileModificationTime
        time.sleep(1)


        # Stores the old version of the Json file.
        # self.oldDataFile = os.path.getmtime(self.path)


        # try: 
        #     self.currentData = os.path.getmtime(self.path)

        #     # Checks if the JSON file has been updated.
        #     # If so, the new Json file will be processed instead.
        #     if self.currentData != self.oldDataFile:
        #         print("\n--- File Updated ---")
        #         data = self.loadJson(self.path)

        #         if data is not None:
        #             print("Updated JSON Data:")

        #         self.oldDataFile = self.currentData

        #     # Checks the JSON file every second.
        #     time.sleep(1)


        # except KeyboardInterrupt:
        #     print("\n--- Monitoring Stopped ---")


    # Extracts the specific telemetry data from the JSON file.
    def processData(self):

        # Processes the oxygen data from the Rover Telemetry JSON file.
        self.oxygen["oxygen_levels"] = self.currentData["pr_telemetry"].get("oxygen_levels")
        print(f"Oxygen Levels: {self.oxygen['oxygen_levels']}")
        self.oxygen["oxygen_tank"] = self.currentData["pr_telemetry"].get("oxygen_tank")
        print(f"Oxygen Tank: {self.oxygen['oxygen_tank']}")
        self.oxygen["oxygen_pressure"] = self.currentData["pr_telemetry"].get("oxygen_pressure")
        print(f"Oxygen Pressure: {self.oxygen['oxygen_pressure']}")

        # Processes the battery data from the Rover Telemetry JSON file.
        self.battery["battery_level"] = self.currentData["pr_telemetry"].get("battery_level")
        print(f"Battery Level: {self.battery}")
        self.battery["power_consumption_rate"] = self.currentData["pr_telemetry"].get("power_consumption_rate")
        print(f"Power Consumption Rate: {self.battery['power_consumption_rate']}")
        self.battery["solar_panel_efficiency"] = self.currentData["pr_telemetry"].get("solar_panel_efficiency")
        print(f"Solar Panel Efficiency: {self.battery['solar_panel_efficiency']}")

        # Processes the temperature data from the Rover Telemetry JSON file.
        self.temp = self.currentData["pr_telemetry"].get("cabin_temperature")
        print(f"Cabin temperature: {self.temp}")

        # Processes the coolant storage data from the Rover Telemetry JSON file.
        self.coolant_storage["pr_coolant_tank"] = self.currentData["pr_telemetry"].get("pr_coolant_tank")
        print(f"Coolant Tank: {self.coolant_storage['pr_coolant_tank']}")
        self.coolant_storage["pr_coolant_level"] = self.currentData["pr_telemetry"].get("pr_coolant_level")
        print(f"Coolant Level: {self.coolant_storage['pr_coolant_level']}")
        self.coolant_storage["pr_coolant_pressure"] = self.currentData["pr_telemetry"].get("pr_coolant_pressure")

        # Processes the CO2 data from the Rover Telemetry JSON file.
        self.co2 = self.currentData["pr_telemetry"].get("co2_scrubber")
        print(f"CO2 Scrubber: {self.co2}")


        # Saves the processed telemetry data to the Essential_Telemetry.json file.
        self.essentialTelemetry["essential_telemetry"]["oxygen_levels"] = self.oxygen["oxygen_levels"]
        self.essentialTelemetry["essential_telemetry"]["oxygen_tank"] = self.oxygen["oxygen_tank"]
        self.essentialTelemetry["essential_telemetry"]["oxygen_pressure"] = self.oxygen["oxygen_pressure"]
        self.essentialTelemetry["essential_telemetry"]["battery_level"] = self.battery["battery_level"]
        self.essentialTelemetry["essential_telemetry"]["power_consumption_rate"] = self.battery["power_consumption_rate"]
        self.essentialTelemetry["essential_telemetry"]["solar_panel_efficiency"] = self.battery["solar_panel_efficiency"]
        self.essentialTelemetry["essential_telemetry"]["pr_coolant_tank"] = self.coolant_storage["pr_coolant_tank"]
        self.essentialTelemetry["essential_telemetry"]["pr_coolant_level"] = self.coolant_storage["pr_coolant_level"]
        self.essentialTelemetry["essential_telemetry"]["pr_coolant_pressure"] = self.coolant_storage["pr_coolant_pressure"]
        self.essentialTelemetry["essential_telemetry"]["cabin_temperature"] = self.temp
        self.essentialTelemetry["essential_telemetry"]["co2_scrubber"] = self.co2
        
        ## Add mission elapsed time to the essential telemetry data
        print("Getting the mission elapsed time")
        self.essentialTelemetry["essential_telemetry"]["mission_elapsed_time"] = self.currentData["pr_telemetry"].get("mission_elapsed_time")
        self.saveJson(self.savePath, "Essential_Telemetry.json", self.essentialTelemetry)

    


    # def getOxygen(self):
    #     return self.oxygen
    
    # def getBattery(self):
    #     return self.battery
    
    # def getWater(self):
    #     return self.water
    
    # def getCo2(self):
    #     return self.co2
    
    # def getCoolantStorage(self):
    #     return self.coolant_storage
    
    # def getTemp(self):
    #     return self.temp
    

# resource = Resource()

# resource.loadJson()

# while True:
#     resource.processData()
#     resource.monitorData()
    




