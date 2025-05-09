// Import the main React library, which lets us create components.
// Also import the 'useState' Hook, which allows functional components to manage state (data that changes).
import React, { useState } from 'react';

// Import CSS files to style the component. These define how the elements look.
import "./css/SetupCSS.css";
import "./css/MasterCSS.css";

/*
* Setup() - PAGE COMPONENT
*
* Description:
* This is a React functional component. It renders a page where users can enter
* IP addresses for different systems (TSS, DUST, Common Server, EVA1, EVA2) and submit them
* to establish connections via a backend server.
* It includes input validation and displays connection status messages.
*
* Params:
* None
*
* Returns:
* A JSX object representing the HTML structure to be displayed on the page.
*/
function Setup() {
  // --- STATE MANAGEMENT ---
  // 'useState' is a React Hook to add state variables to functional components.
  // It returns an array: [current State Value, function To Update State]

  // 'inputs' state: Stores the current text value inside each input field.
  // Initialized as an object with empty strings for each input.
  const [inputs, setInputs] = useState({
    dustInput: '', // Value for the DUST IP input
    tssInput: '',  // Value for the TSS IP input
    commonServerInput: '', // Value for the Common Server input 
    evaInput: '',   // Value for the EVA 1 input
    eva2Input: '',  // Value for the EVA 2 input
  });

  // 'errors' state: Stores validation error messages for each corresponding input field.
  // Initialized empty. If an input is valid, its corresponding error value will be "".
  const [errors, setErrors] = useState({
    dustInput: '',
    tssInput: '',
    commonServerInput: '', // Error for the Common Server input
    evaInput: '',
    eva2Input: '',
  });

  // 'connectionStatus' state: Tracks the status of communication with the backend server.
  // Used to provide feedback to the user (e.g., show "Connecting...", success/error messages)
  // and disable the button during connection attempts.
  const [connectionStatus, setConnectionStatus] = useState({
    isConnecting: false, // Flag: true if currently waiting for backend response, false otherwise.
    message: '',        // String: Message displayed to the user (e.g., "Connecting...", "Success!", "Error: ...").
    success: null       // Status: null (initial), true (last attempt succeeded), false (last attempt failed).
  });

  // --- IP VALIDATION FUNCTION ---
  // A regular JavaScript function to check if a given string is a valid IP address.
  const validateIp = (value, fieldname) => {
    // value: The string (text) from the input box.
    // fieldname: The name of the input field (e.g., 'tssInput', 'dustInput').

    // Specific requirement: The TSS IP input box *must* have a value.
    if (fieldname === 'tssInput' && !value.trim()) {
      // .trim() removes whitespace from start/end. ! checks if the result is empty.
      return "IP address is required"; // Return error message if TSS IP is empty.
    }
    // Optional fields: If it's *not* the TSS input and it's empty, it's okay.
    // This currently includes the new 'commonServerInput' as optional.
    else if (fieldname !== 'tssInput' && !value.trim()){
      return ""; // Return an empty string, meaning "no error".
    }

    // Regular Expression (Regex) to check the IP format:
    // Must be like: number.number.number.number (e.g., 192.168.1.1)
    const ipRegex = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;

    // Try to match the regex against the input value.
    const ipMatch = value.match(ipRegex);

    // If 'value' doesn't match the pattern (e.g., "abc", "192.168"), ipMatch will be null.
    if (!ipMatch) {
      return "Invalid IP address format"; // Return error message.
    }

    // If format is okay, check if each number part is between 0 and 255.
    const validSegments = ipMatch.slice(1).every(segment => {
      const num = parseInt(segment, 10); // Convert the number string (e.g., "192") to an integer.
      // Check if the number is within the valid range for an IP segment.
      return num >= 0 && num <= 255;
    });

    // If any segment number was outside the 0-255 range...
    if (!validSegments) {
      return "IP segments must be between 0-255"; // Return error message.
    }

    // If all checks passed (format is good, numbers are in range)...
    return ""; // Return empty string, indicating the IP is valid.
  };


  // --- INPUT CHANGE HANDLER ---
  // This function is called EVERY time the user types a character into ANY of the input fields.
  const handleChange = (e) => {
    // 'e' is the event object, containing details about the change.
    // 'e.target' is the specific <input> element that triggered the event.

    // Destructuring assignment: Extracts 'name' and 'value' properties from e.target.
    const { name, value } = e.target;

    // Update the 'inputs' state for the specific input that changed
    setInputs(prev => ({
      ...prev,
      [name]: value
    }));

    // Validate the new value immediately
    const error = validateIp(value, name);

    // Update the 'errors' state for that specific input
    setErrors(prev => ({
      ...prev,
      [name]: error
    }));
  };


  // --- BACKEND CONNECTION FUNCTION ---
  // This function handles sending data for ONE system to the backend server.
  const connectToSystem = async (systemName, ipAddress) => {
    // Basic check: Don't try to connect if the IP is missing (especially for TSS).
    if (!ipAddress && systemName === 'TSS') {
         setConnectionStatus({ isConnecting: false, message: 'TSS IP address is required.', success: false });
         return false; // Indicate failure
    }
    // Skip optional systems if no IP was entered.
    if (!ipAddress && systemName !== 'TSS') {
         console.log(`Skipping connection for ${systemName} (no IP provided).`);
         return true; // Treat as "not failed" since it's optional.
    }

    try {
      setConnectionStatus({
        isConnecting: true,
        message: `Connecting to ${systemName} (${ipAddress})...`,
        success: null
      });

      let endpoint = '';
      let bodyPayload = {};

      // Specific handling for the TSS system.
      if (systemName === 'TSS') {
        endpoint = 'http://localhost:5000/start-connection';
        bodyPayload = { tssIP: ipAddress };
      }
      // *** ADD LOGIC HERE IF/WHEN YOU WANT TO CONNECT "Common Server" ***
      // Example:
      // else if (systemName === 'Common Server') {
      //   endpoint = 'http://localhost:5000/connect-common'; // Needs corresponding backend route
      //   bodyPayload = { commonIp: ipAddress }; // Example payload
      // }
      // Placeholder for handling other systems
      else {
        console.warn(`Connection logic for ${systemName} not implemented.`);
        setConnectionStatus({
             isConnecting: false,
             message: `Connection logic for ${systemName} is not yet implemented.`,
             success: null
        });
        return true;
      }

      console.log(`Sending request to ${endpoint} with payload:`, JSON.stringify(bodyPayload));

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bodyPayload)
      });

      // Handle the server's response (error handling)
      if (!response.ok) {
        let errorMessage = `Server responded with status ${response.status}`;
        let responseBodyText = '';
        try {
            responseBodyText = await response.text();
            console.error(`Raw error response from server for ${systemName}:`, responseBodyText);
            const errorData = JSON.parse(responseBodyText);
            errorMessage = errorData.message || JSON.stringify(errorData);
        } catch (e) {
            errorMessage = `${errorMessage}: ${responseBodyText.substring(0, 200)}`;
        }
        console.error(`Failed to connect to ${systemName}: ${errorMessage}`);
        throw new Error(errorMessage);
      }

      // Handle successful response
      const data = await response.json();
      const successMessage = data.message || `${systemName} connected successfully!`;
      setConnectionStatus({
        isConnecting: false,
        message: successMessage,
        success: true
      });
      console.log(`Success connecting to ${systemName}. Server response:`, data);
      return true;

    } catch (error) {
      // Handle fetch/network errors or errors thrown from response handling
      console.error(`Error during connectToSystem for ${systemName}:`, error);
      setConnectionStatus({
        isConnecting: false,
        message: `Error connecting to ${systemName}: ${error.message}`,
        success: false
      });
      return false;
    }
  }; // --- End connectToSystem ---


  // --- FORM SUBMISSION HANDLER ---
  // Runs when the "Connect Systems" button is clicked.
  const handleSubmit = async (e) => {
    e.preventDefault(); // Stop page refresh

    // Re-validate all inputs before submitting
    let formIsValid = true;
    const newErrors = {};
    // *** Use Object.keys(inputs) which now includes commonServerInput ***
    Object.keys(inputs).forEach(name => {
      const error = validateIp(inputs[name], name);
      newErrors[name] = error;
      if (error) formIsValid = false;
    });
    setErrors(newErrors);
    // --- End Re-validation ---

    setConnectionStatus({ isConnecting: false, message: '', success: null }); // Reset status

    if (formIsValid) {
      console.log("Form is valid. Attempting to connect TSS...");
      // Only connect TSS for now (as per previous logic)
      await connectToSystem('TSS', inputs.tssInput);
      // Add calls to connect other systems here if needed later
      // e.g., await connectToSystem('Common Server', inputs.commonServerInput);
    } else {
      console.log("Form has errors, please fix them.");
      setConnectionStatus({
        isConnecting: false,
        message: 'Please fix the errors in the form before connecting.',
        success: false
      });
    }
  }; // --- End handleSubmit ---


  // --- JSX: RENDERING THE UI ---
  return (
    <div className="themeBackground center_drop">
      <div className="">
        <form className="ip-form" onSubmit={handleSubmit}>
          <h2 className="setup_heading"> Enter IP addresses</h2>

          {/* --- Input Row for DUST IP --- */}
          <div className="form-row">
            <label>DUST IP:</label>
            <div className="input-container">
              <input
                name="dustInput"
                placeholder="192.168.1.1"
                value={inputs.dustInput}
                onChange={handleChange}
                className={errors.dustInput ? "input-error" : ""}
              />
              {errors.dustInput && <div className="error-message">{errors.dustInput}</div>}
            </div>
          </div>

          {/* --- Input Row for TSS IP --- */}
          <div className="form-row">
            <label>TSS IP:</label>
            <div className="input-container">
              <input
                name="tssInput"
                placeholder="192.168.1.1"
                value={inputs.tssInput}
                onChange={handleChange}
                className={errors.tssInput ? "input-error" : ""}
              />
              {errors.tssInput && <div className="error-message">{errors.tssInput}</div>}
            </div>
          </div>

          {}
          <div className="form-row">
            {/* Changed Label */}
            <label>Common Server:</label>
            <div className="input-container">
              <input
                name="commonServerInput"       // Changed name attribute
                placeholder="192.168.1.1"
                value={inputs.commonServerInput} // Bound to new state property
                onChange={handleChange}
                // Check corresponding error state property
                className={errors.commonServerInput ? "input-error" : ""}
              />
              {/* Show error from corresponding error state property */}
              {errors.commonServerInput && <div className="error-message">{errors.commonServerInput}</div>}
            </div>
          </div>
          {}


          {/* --- Input Row for EVA 1 --- */}
          <div className="form-row">
            <label>EVA 1:</label>
            <div className="input-container">
              <input
                name="evaInput"
                placeholder="192.168.1.1"
                value={inputs.evaInput}
                onChange={handleChange}
                className={errors.evaInput ? "input-error" : ""}
              />
              {errors.evaInput && <div className="error-message">{errors.evaInput}</div>}
            </div>
          </div>

          {/* --- Input Row for EVA 2 --- */}
          <div className="form-row">
            <label>EVA 2:</label>
            <div className="input-container">
              <input
                name="eva2Input"
                placeholder="192.168.1.1"
                value={inputs.eva2Input}
                onChange={handleChange}
                className={errors.eva2Input ? "input-error" : ""}
              />
              {errors.eva2Input && <div className="error-message">{errors.eva2Input}</div>}
            </div>
          </div>

          {/* --- Connection Status Display --- */}
          {connectionStatus.message && (
            <div className={`connection-status ${
                connectionStatus.success === true ? 'success'
              : connectionStatus.success === false ? 'error'
              : 'info'
            }`}>
              {connectionStatus.message}
            </div>
          )}

          {/* --- Submit Button --- */}
          <button
            type="submit"
            className="submit-button"
            disabled={connectionStatus.isConnecting}
          >
            {connectionStatus.isConnecting ? 'Connecting...' : 'Connect Systems'}
          </button>
        </form>
      </div>
    </div>
  ); // --- End JSX ---
} // --- End Setup Component ---

// Make the Setup component available to be imported and used in other parts of the application.
export default Setup;