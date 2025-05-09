import json
from sklearn.linear_model import LinearRegression
import os
import time

class Prediction:
    THRESHOLDS = {
        'oxygen_levels': {'critical': 0.10, 'warning': 0.25, 'caution': 0.45, 'safe': None},
        'oxygen_tank': {'critical': 0.10, 'warning': 0.25, 'caution': 0.45, 'safe': None},
        'oxygen_pressure': {'critical': 0.10, 'warning': 0.25, 'caution': 0.45, 'safe': None},
        'battery_level': {'critical': 0.10, 'warning': 0.25, 'caution': 0.45, 'safe': None},
        'power_consumption_rate': {'critical': 0.45, 'warning': 0.25, 'caution': 0.10, 'safe': None},
        'pr_coolant_tank': {'critical': 0.10, 'warning': 0.25, 'caution': 0.45, 'safe': None},
        'pr_coolant_level': {'critical': 0.10, 'warning': 0.25, 'caution': 0.45, 'safe': None},
        'pr_coolant_pressure': {'critical': 0.10, 'warning': 0.25, 'caution': 0.45, 'safe': None},
        'cabin_temperature': {'critical': 0.10, 'warning': 0.25, 'caution': 0.45, 'safe': None},
    }
    
    TELEMETRY_PATHS = {
        'oxygen_levels': ('oxygen', 'oxygen_levels'),
        'oxygen_tank': ('oxygen', 'oxygen_tank'),
        'oxygen_pressure': ('oxygen', 'oxygen_pressure'),
        'battery_level': ('battery', 'battery_level'),
        'power_consumption_rate': ('battery', 'power_consumption_rate'),
        'pr_coolant_tank': ('coolant_storage', 'pr_coolant_tank'),
        'pr_coolant_level': ('coolant_storage', 'pr_coolant_level'),
        'pr_coolant_pressure': ('coolant_storage', 'pr_coolant_pressure'),
        'cabin_temperature': ('temp', 'cabin_temperature'),
    }
 
    def __init__(self):       
        # temporary path
        self.loadPath = "User_Interface/UI_Main/client/src/telemetry_json/allLogs.json"
        self.outputPath = "User_Interface/UI_Main/client/src/telemetry_json/ResourcePrediction.json"
        
        # holds (timestamp, scaled value) in the list in the value of the key-value pair for each variable
        '''
        {
            'oxygen_tank': [
                (0, 0.98), 
                (1, 0.97), 
                (2, 0.96), 
                ...
            ],
        }
        '''
        #initialize telemetry_trends for each parameter in THRESHOLDS
        self.telemetry_data = {key: [] for key in self.THRESHOLDS}

        # re-scales raw telemetry values into normalized/meaningful outputs/units
        self.multipliers = {
            'oxygen_levels':            0.01 * 5,     # from logStatus: oxygen_levels * 0.01 * 5
            'oxygen_tank':              0.01,         # oxygen_tank * 0.01
            'oxygen_pressure':          0.0001 * 3.3, # oxygen_pressure * 0.0001 * 3.3
            'battery_level':            0.01,         # battery_level * 0.01
            'power_consumption_rate':   2000,         # power_consumption_rate * 2000      
            'pr_coolant_tank':          0.01,         # pr_coolant_tank * 0.01
            'pr_coolant_level':         0.01 * 2.25,  # pr_coolant_level * 0.01 * 2.25
            'pr_coolant_pressure':      0.001 * 3.2,  # pr_coolant_pressure * 0.001 * 3.2
            'cabin_temperature':        0.01 * 7.25,  # temp → cabin_temperature * 0.01 * 7.25
            'co2_scrubber':             0.01,         # if you later decide to scale CO₂
        }

    # Loads Json file from a specific directory.
    def loadJson(self):
            try:
                with open(self.loadPath, "r") as file:
                    self.currentData = json.load(file)
            except FileNotFoundError:
                print(f"Error: File {self.loadPath} not found.")
                self.currentData = {}
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON in {self.loadPath}")
                self.currentData = {}
            
    def getValues(self):
        """Get the values from the log file"""
        for time_str, snapshot in self.currentData.items():
            try:
                timestamp = int(time_str)
            except ValueError:
                continue
            
            for param, (section, field) in self.TELEMETRY_PATHS.items():
                try:
                    raw_value = snapshot[section][field]
                    if isinstance(raw_value, (int, float)):
                        scaled_value = raw_value * self.multipliers[param]
                        self.telemetry_data[param].append((timestamp, scaled_value))
                except (KeyError, TypeError):
                    continue
                
    def predict_threshold_crossings(self):
        """Run linear regression and estimate time-to-threshold for each telemetry parameter."""
        prediction = {}
        for param, values in self.telemetry_data.items():
            if len(values) < 2:
                continue
            
            # x is time steps as a 2d list, y is telemetry values
            # prepares data like so: X = [[0], [1], [2]], y = [0.98, 0.97, 0.96] for oxygen level for example
            X = [[t] for t, _ in values]
            y = [v for _, v in values]
            model = LinearRegression().fit(X, y)

            slope = model.coef_[0]
            intercept = model.intercept_
            current_time = values[-1][0]
            
            status_messages = []
            times = {}
            
            for level in ['critical', 'warning', 'caution']:
                threshold = self.THRESHOLDS[param][level]
                if threshold is not None and slope != 0:
                    # this is the regression equation (threshold = slope * t + intercept)
                    t_cross = (threshold - intercept) / slope
                    if t_cross >= current_time:
                        # convert time to hours, mins, seconds
                        seconds_to = round(t_cross - current_time, 2)
                        times[level] = round(t_cross, 2)
                        hours = int(seconds_to // 3600)
                        minutes = int((seconds_to % 3600) // 60)
                        seconds = round(seconds_to % 60, 2)

                        parts = []
                        if hours > 0:
                            parts.append(f"{hours}h")
                        if minutes > 0 or hours > 0:
                            parts.append(f"{minutes}m")
                        parts.append(f"{seconds}s")

                        formatted_time = " ".join(parts)

                        status_messages.append(f"Projected to hit {level.upper()} in {formatted_time}")


            if times:
                prediction[param] = {
                    'slope': round(slope, 5),
                    'intercept': round(intercept, 5),
                    'threshold_cross_times': times,
                    'status_messages': status_messages
                }

        return prediction
    
    def run_interval_predictions(self, interval=20):
        """Process every `interval` ticks instead of all at once."""
        sorted_keys = sorted(self.currentData.keys(), key=lambda k: int(k))  # ensure correct order of appended data

        temp_telemetry_data = {key: [] for key in self.THRESHOLDS}  # local batch storage

        for i, time_str in enumerate(sorted_keys):
            try:
                timestamp = int(time_str)
                snapshot = self.currentData[time_str]
            except (ValueError, KeyError):
                continue

            for param, (section, field) in self.TELEMETRY_PATHS.items():
                try:
                    raw_value = snapshot[section][field]
                    if isinstance(raw_value, (int, float)):
                        scaled_value = raw_value * self.multipliers[param]
                        temp_telemetry_data[param].append((timestamp, scaled_value))
                except (KeyError, TypeError):
                    continue

            #every N ticks, run prediction and save
            if (i + 1) % interval == 0 or i == len(sorted_keys) - 1:
                self.telemetry_data = temp_telemetry_data.copy()
                predictions = self.predict_threshold_crossings()
                self.save_predictions(predictions, tick=timestamp)
    
    def turn_back(self, base_return_time: float = 120.0) -> dict:
        """
        Evaluates if any resource is projected to hit WARNING or CRITICAL 
        within `base_return_time` seconds.
        Returns a dictionary with 'return_to_base': True/False and reasons.
        """
        decision = {
            "return_to_base": False,
            "reasons": []
        }

        predictions = self.predict_threshold_crossings()

        for param, data in predictions.items():
            threshold_times = data.get("threshold_cross_times", {})
            current_time = self.telemetry_data[param][-1][0]

            for level in ["critical", "warning"]:
                if level in threshold_times:
                    t_cross = threshold_times[level]
                    seconds_to_cross = t_cross - current_time

                    if seconds_to_cross <= base_return_time:
                        decision["return_to_base"] = True
                        minutes = int(seconds_to_cross // 60)
                        seconds = round(seconds_to_cross % 60, 2)
                        readable_time = f"{minutes}m {seconds}s" if minutes else f"{seconds}s"
                        reason = f"{param} will hit {level.upper()} in {readable_time}"
                        decision["reasons"].append(reason)

        return decision
    
    def save_predictions(self, predictions, tick=None):        
        try:
            history = []
            
            if os.path.exists(self.outputPath):
                with open(self.outputPath, "r") as file:
                    try:
                        history = json.load(file)
                        if not isinstance(history, list):
                            print("overwriting non-list Json file.")
                            history = []
                    except json.JSONDecodeError:
                        print("existing json file is invalid. Overwriting.")
                        history = []
            else:
                history = []
            
            turn_back_decision = self.turn_back(base_return_time=120)

            entry = {
                "tick": tick,
                "predictions": predictions,
                "turn_back_decision": turn_back_decision
            }
            history.append(entry)

            with open(self.outputPath, "w") as file:
                json.dump(history, file, indent=4)
        except Exception as e:
            print(f"Error saving predictions: {e}")
        

if __name__ == "__main__":
    demo = Prediction()
    demo.loadJson()
    demo.run_interval_predictions(interval=20)
    
    # time of last modification
    # last_modified = 0
    
    # may also use watchdog
    # while True:
    #     try:
    #         # getmtime returns the last modification time (compares last time modified to current modified time)
    #         current_modified = os.path.getmtime(demo.loadPath)
    #         # looking for file modification
    #         if current_modified != last_modified:
    #             demo.loadJson()
    #             demo.run_interval_predictions(interval=20)
    #             last_modified = current_modified
    #         time.sleep(5)  # check every 5 seconds
    #     except KeyboardInterrupt:
    #         break
    #     except Exception as e:
    #         time.sleep(5)


### Goal:
# populate individual parameter maps with values from log.
# dataframe from dictionary for each parameter.
# create linear regression model for each parameter.
# fit the model to the data.
# make predictions based on the critical, warning, and caution values for each parameter.
# store the predictions in a json file.
