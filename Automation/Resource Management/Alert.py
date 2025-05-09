from datetime import datetime
# from Prediction import Prediction
# from Log import Log
import json
import os


class Alert:
    def __init__(self):

        # Alert message
        self.alertmessage = {}

        self.alertcount = 0

        # Oxygen values
        self.oxygen = {
                    "oxygen_levels": 00.000000000000000,
                    "oxygen_tank": 0.00000000000000,
                    "oxygen_pressure": 0000.00000000000000,
                }
        
        # Battery values
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
        
        # Cabin temperature value tracking.
        self.temp = {
                    "cabin_temperature": 00.00000000000000,
                }

        # directories for saving and loading telemetry data
        self.savePath = "User_Interface/UI_Main/client/src/telemetry_json/alertsLog.json"
        self.loadPath = "User_Interface/UI_Main/client/src/telemetry_json/allLogs.json"

        # essentialTelemetry contains defaults within a map for all data
        self.essentialTelemetry = {
                    "essential_telemetry": {
                        "mission_elapsed_time": 0.0,
                        "oxygen_levels": 00.000000000000000,
                        "oxygen_tank": 0.00000000000000,
                        "oxygen_pressure": 0000.00000000000000,
                        "battery_level": 00.00000000000000,
                        "power_consumption_rate": 0.0000000000000000000,
                        "solar_panel_efficiency": 0.0,
                        "pr_coolant_tank": 00.00000000000000,
                        "pr_coolant_level": 00.000000000000000,
                        "pr_coolant_pressure": 000.0000000000000,
                        "cabin_temperature": 00.00000000000000,
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
            

    # saveJson is essentially the same as the Resource file's method, however, it handles the allLogs dictionary
    def saveJson(self, directory=None, filename="alertsLog.json", data = None):

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
    # - Logs are stored with unique IDs using alertcount to allow chronological review and traceability.
    # - Supports real-time monitoring and alerting systems by making the state of each resource explicit and structured.



    # Round the values in the telemetry data to two decimal places
    def round_to_two(self, obj):
        if isinstance(obj, dict):
            return {k: self.round_to_two(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.round_to_two(i) for i in obj]
        elif isinstance(obj, float):
            return round(obj, 2)
        else:
            return obj



    def alertMessage(self):
        for i, data in self.currentData.items():
            # Set the all_safe variable's requirements
            all_safe = (data["oxygen_status"] == "SAFE" and 
                        data["battery_status"] == "SAFE" and 
                        data["co2_status"] == "SAFE" and 
                        data["coolant_storage_status"] == "SAFE" and 
                        data["temp_status"] == "SAFE")
            
            # If everything falls in line with all_safe, then we can skip the rest of the code
            if all_safe:
                self.alertmessage[str(self.alertcount)] = {
                    "mission_elapsed_time": round(data["mission_elapsed_time"], 2),
                    f"Log {i}": ["All resources are within safe limits"]
                }
                self.alertcount += 1
                print(self.alertmessage)
                continue

            # Opening line that precedes all resource alerts
            log_messages = [
                f"The following resource(s) are not within safe limits:"
            ]
            
            # Append detailed messages for each unsafe resource (such as caution and warning)
            if data["oxygen_status"] != "SAFE":
                log_messages.append(f"{{'oxygen_status': '{data['oxygen_status']}'}}")
                log_messages.append({
                    "oxygen": self.round_to_two(data['oxygen'])
                })

            if data["battery_status"] != "SAFE":
                log_messages.append(f"{{'battery_status': '{data['battery_status']}'}}")
                log_messages.append({
                    "battery": self.round_to_two(data['battery'])
                })

            if data["co2_status"] != "SAFE":
                log_messages.append(f"{{'co2_status': '{data['co2_status']}'}}")
                log_messages.append({
                    "co2": self.round_to_two(data['co2'])
                })    
                
            if data["coolant_storage_status"] != "SAFE":
                log_messages.append(f"{{'coolant_storage_status': '{data['coolant_storage_status']}'}}")
                log_messages.append({
                    "coolant_storage": self.round_to_two(data['coolant_storage'])
                })
                
            if data["temp_status"] != "SAFE":
                log_messages.append(f"{{'temp_status': '{data['temp_status']}'}}")
                log_messages.append({
                    "temp": self.round_to_two(data['temp'])
                })
                
            # Add the record to alertmessage for logging and review
            self.alertmessage[str(self.alertcount)] = {
                "mission_elapsed_time": round(data["mission_elapsed_time"], 2),
                f"Log {i}": log_messages
            }
            
            self.alertcount += 1

            print(self.alertmessage)
        
        return self.alertmessage


alert = Alert()
alert.loadJson()
alert.alertMessage()
alert.saveJson("User_Interface/UI_Main/client/src/telemetry_json/")