from datetime import datetime
# from Prediction import Prediction
# from Log import Log
import json
import os
import time


class Alert:
    def __init__(self):

        # Alert message
        self.alertmessage = {}

        # Nominal, caution, and warning values for oxygen, battery, CO2, coolant and temperature
        self.oxygen_is_nominal = 0
        self.oxygen_is_caution = 0
        self.oxygen_is_warning = 0
        self.battery_is_nominal = 0
        self.battery_is_caution = 0
        self.battery_is_warning = 0
        self.co2_is_nominal = 0
        self.co2_is_caution = 0
        self.co2_is_warning = 0
        self.coolant_storage_is_nominal = 0
        self.coolant_storage_is_caution = 0
        self.coolant_storage_is_warning = 0
        self.temp_is_nominal = 0
        self.temp_is_caution = 0
        self.temp_is_warning = 0

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

        # Directories for saving and loading telemetry data
        self.savePath = "User_Interface/UI_Main/client/src/telemetry_json/alerts.json"
        self.loadPath = "User_Interface/UI_Main/client/src/telemetry_json/allLogs.json"
        
        # essentialTelemtry contains defaults within a map for all data
        self.essentialTelemetry = {
                    "essential_telemetry": {
                        "mission_elapsed_time": 0.0,
                        "oxygen_levels": 00.00,
                        "oxygen_tank": 0.00,
                        "oxygen_pressure": 0000.00,
                        "battery_level": 00.00,
                        "power_consumption_rate": 0.00,
                        "solar_panel_efficiency": 0.0,
                        "pr_coolant_tank": 00.00,
                        "pr_coolant_level": 00.00,
                        "pr_coolant_pressure": 000.00,
                        "cabin_temperature": 00.00,
                        "co2_scrubber": 0
                    }
                }
        self.currentData = {}

    # loadJson loads the json file and prints the data
    def loadJson(self):
            try:
                with open(self.loadPath, 'r') as file:
                    self.currentData = json.load(file)


            except FileNotFoundError:
                print(f"Error: File {self.loadPath} not found.")
                return None
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON in {self.loadPath}")
                return None
            

    # saveJson is a similar method to the Resource file's, however, it handles the allLogs dictionary
    def saveJson(self, directory=None, filename="alerts.json", data = None):

        if directory is None:
            filepath = filename
        else:
            if not os.path.exists(directory):
                os.makedirs(directory)

            filepath = os.path.join(directory, filename)

        with open(filepath, "w") as file:
            json.dump(self.alertmessage, file, indent=4)

            print(f"Log data saved to {filepath}")
            print("Log Data:")
            print(json.dumps(self.alertmessage, indent=2))
            
    
    # Scans the loaded telemetry data for any unsafe resource conditions.
    # Purpose:
    # - Ensures mission-critical subsystems like oxygen, battery, CO2, coolant, and temperature are within safe thresholds.
    # - If all subsystems report "SAFE", confirms system health with a simple status message.
    # - If any subsystem is outside safe limits, generates a detailed alert log listing which subsystems are affected.
    # - Supports real-time monitoring and alerting systems by making the state of each resource explicit and structured.

    def alertMessage(self):
        for i, data in self.currentData.items():
            # List of boolean values for each resource
            oxygen_messages = {}
            battery_messages = {}
            co2_messages = {}
            coolant_messages = {}
            temp_messages = {}

            # The bools are set to false by default
            self.oxygen_is_nominal = 0
            self.oxygen_is_caution = 0
            self.oxygen_is_warning = 0
            self.battery_is_nominal = 0
            self.battery_is_caution = 0
            self.battery_is_warning = 0
            self.co2_is_nominal = 0
            self.co2_is_caution = 0
            self.co2_is_warning = 0
            self.coolant_storage_is_nominal = 0
            self.coolant_storage_is_caution = 0
            self.coolant_storage_is_warning = 0
            self.temp_is_nominal = 0
            self.temp_is_caution = 0
            self.temp_is_warning = 0
            
            # Append detailed messages for each unsafe resource (such as nominal, caution, warning)
            if data["oxygen_status"] == "CAUTION":
                self.oxygen_is_caution = 1
            elif data["oxygen_status"] == "WARNING":
                self.oxygen_is_warning = 1
            else:
                self.oxygen_is_nominal = 1
                
            if data["battery_status"] == "CAUTION":
                self.battery_is_caution = 1
            elif data["battery_status"] == "WARNING":
                self.battery_is_warning = 1
            else:
                self.battery_is_nominal = 1
                
            if data["co2_status"] == "CAUTION":
                self.co2_is_caution = 1
            elif data["co2_status"] == "WARNING":
                self.co2_is_warning = 1
            else:
                self.co2_is_nominal = 1
                
            if data["coolant_storage_status"] == "CAUTION":
                self.coolant_storage_is_caution = 1
            elif data["coolant_storage_status"] == "WARNING":
                self.coolant_storage_is_warning = 1
            else:
                self.coolant_storage_is_nominal = 1
                
            if data["temp_status"] == "CAUTION":
                self.temp_is_caution = 1
            elif data["temp_status"] == "WARNING":
                self.temp_is_warning = 1
            else:
                self.temp_is_nominal = 1

            # Append within each list the nominal, caution, and warning values
            oxygen_messages = {
                "nominal": self.oxygen_is_nominal,
                "caution": self.oxygen_is_caution,
                "warning": self.oxygen_is_warning
            }
            battery_messages = {
                "nominal": self.battery_is_nominal,
                "caution": self.battery_is_caution,
                "warning": self.battery_is_warning
            }
            co2_messages = {
                "nominal": self.co2_is_nominal,
                "caution": self.co2_is_caution,
                "warning": self.co2_is_warning
            }
            coolant_messages = {
                "nominal": self.coolant_storage_is_nominal,
                "caution": self.coolant_storage_is_caution,
                "warning": self.coolant_storage_is_warning
            }
            temp_messages = {
                "nominal": self.temp_is_nominal,
                "caution": self.temp_is_caution,
                "warning": self.temp_is_warning
            }

            
            # Add the record to alertmessage for logging and review
            self.alertmessage["alerts:"] = {
                "oxygen_alert": oxygen_messages,
                "battery_alert": battery_messages,
                "co2_alert": co2_messages,
                "coolant_alert": coolant_messages,
                "temp_alert": temp_messages,
            }
        return self.alertmessage


alert = Alert()
while True:
    alert.loadJson()
    alert.alertMessage()
    alert.saveJson("User_Interface/UI_Main/client/src/telemetry_json/")

    # Update every 10 seconds
    time.sleep(10)