from flask import Flask, request, jsonify
from flask_cors import CORS
from theCommand import Command # Import your existing Command class
import threading # To potentially run data fetching in the background
import time

command_instance = Command()
data_fetching_active = False
data_fetching_thread = None

# --- Flask App Setup ---
app = Flask(__name__)
# Allow requests from React app's origin
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# --- API Endpoint to Set IP and Start Connection ---
@app.route('/start-connection', methods=['POST'])
def handle_start_connection():
    global command_instance, data_fetching_active, data_fetching_thread

    data = request.get_json()
    if not data or 'tssIP' not in data:
        return jsonify({"status": "error", "message": "Missing tssIP in request"}), 400

    tss_ip = data['tssIP']
    print(f"Received request to connect to TSS IP: {tss_ip}")

    try:
        # Use the global instance and set the IP address
        command_instance.setIPAdress(tss_ip)
        print(f"TSS IP set to: {command_instance.IP_address}")

        
        if not data_fetching_active:
             print("Attempting to start data fetching...")
             # Simple check: Ping the TSS (replace with a real check if possible)
             # This is a placeholder - UDP is connectionless, so 'pinging' isn't straightforward.
             try:
                 # Send a simple command to see if it errors immediately
                 # Using command 58 (eva_time) as an example
                 test_result = command_instance.send_command(58)
                 print(f"Initial command test successful. Result: {test_result}")

                 def run_get_data_loop():
                     global data_fetching_active
                     print("Background data fetching loop started.")
                     data_fetching_active = True
                     while data_fetching_active:
                         try:
                             command_instance.getData()
                             print("getData() cycle complete.")
                             time.sleep(1) # Adjust sleep time as needed
                         except Exception as e:
                             print(f"Error during getData() loop: {e}")
                             # Decide if you want to stop on error
                             data_fetching_active = False
                             break
                     print("Background data fetching loop stopped.")

                 # Stop any existing thread before starting a new one
                 if data_fetching_thread and data_fetching_thread.is_alive():
                      data_fetching_active = False # Signal the old thread to stop
                      data_fetching_thread.join(timeout=2) # Wait briefly for it

                 data_fetching_thread = threading.Thread(target=run_get_data_loop, daemon=True)
                 data_fetching_thread.start()

                 response_data = {"status": "success", "message": f"Connection to {tss_ip} initiated, data fetching started."}

             except socket.error as e:
                 print(f"Failed to send initial command to TSS: {e}")
                 response_data = {"status": "error", "message": f"Failed to connect or send initial command to TSS at {tss_ip}. Error: {e}"}
                 return jsonify(response_data), 500 # Internal Server Error
             except Exception as e:
                 print(f"An unexpected error occurred: {e}")
                 response_data = {"status": "error", "message": f"An unexpected error occurred: {e}"}
                 return jsonify(response_data), 500 # Internal Server Error

        else:
             print("Data fetching is already active.")
             response_data = {"status": "info", "message": f"TSS IP updated to {tss_ip}. Data fetching was already running."}


        return jsonify(response_data), 200

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- API Endpoint to Stop Data Fetching (Optional) ---
@app.route('/stop-connection', methods=['POST'])
def handle_stop_connection():
    global data_fetching_active, data_fetching_thread
    print("Received request to stop data fetching.")
    if data_fetching_active:
        data_fetching_active = False
        if data_fetching_thread and data_fetching_thread.is_alive():
            data_fetching_thread.join(timeout=5) # Wait for the thread to finish
        print("Data fetching stopped.")
        return jsonify({"status": "success", "message": "Data fetching stopped."}), 200
    else:
        print("Data fetching was not active.")
        return jsonify({"status": "info", "message": "Data fetching was not active."}), 200


# --- Run the Flask Server ---
if __name__ == '__main__':
    # host='0.0.0.0' makes it accessible from other devices on your network
    # debug=True provides auto-reloading and more error details during development
    app.run(host='0.0.0.0', port=5000, debug=True)