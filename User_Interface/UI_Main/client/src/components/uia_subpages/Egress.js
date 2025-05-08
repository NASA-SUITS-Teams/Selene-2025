import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Collapsible from "./../Collapsible";
import DCU_Front from "./../images/DCU_Front.jpg";
import SUITS_UIA_PANEL from "./../images/SUITS_UIA_PANEL.jpg";
import './../css/UIASubpageCSS.css'

const initialData = {

  "egress_steps": 
  {
        "VERIFY_LTV": 
        {
          "Step_1": 0,
          "Step_2": 0,
          "Step_3": 0,
          "Step_4": 0
        },

        "UIA_TO_DCU": 
        {
          "Step_1": 0,
          "Step_2": 0,
          "Step_3": 0,
          "Step_4": 0
        },

        "Prep_O2":
        {
            "Step_1": 0,
            "Step_2": 0,
            "Step_3": 0,
            "Step_4": 0,
            "Step_5": 0,
            "Step_6": 0,
            "Step_7": 0,
            "Step_8": 0,
            "Step_9": 0,
            "Step_10": 0,
            "Step_11": 0,
            "Step_12": 0
        },

        "END_DEPRESS":
        {
            "Step_1": 0,
            "Step_2": 0,
            "Step_3": 0,
            "Step_4": 0,
            "Step_5": 0,
            "Step_6": 0,
            "Step_7": 0,
            "Step_8": 0,
            "Step_9": 0,
            "Step_10": 0,
            "Step_11": 0
        },

        "DETERMINE_PATH": 
        {
          "Step_1": 0,
          "Step_2": 0,
          "Step_3": 0,
          "Step_4": 0
        },

  }

}

/*  
* Egress() - **PAGE**
*
* Description:
*      Page component where specifically egress operations will
*      be displayed 
*
* Params:
*     None
*
* Returns:
*     A JSX object to be displayed.
*/
function Egress() {

  const navigate = useNavigate();
  
  const navUIA = () =>
  {
    navigate('/uia');
  }

  const [stepsData, setStepsData] = useState(initialData);

  const handleCheckboxChange = (section, step) => {
    setStepsData((prevData) => {
      const updatedSection = { ...prevData.egress_steps[section], [step]: prevData.egress_steps[section][step] === 0 ? 1 : 0 };
      return {
        ...prevData,
        egress_steps: {
          ...prevData.egress_steps,
          [section]: updatedSection,
        }
      };
    });
  };

    const isSectionComplete = (section) => {
      return Object.values(section).every(step => step === 1); // All steps must be 1 for completion
    };

    const isAllSectionsComplete = () => {
      // Check if all sections are complete
      return (
        isSectionComplete(stepsData.egress_steps.VERIFY_LTV) &&
        isSectionComplete(stepsData.egress_steps.UIA_TO_DCU) &&
        isSectionComplete(stepsData.egress_steps.Prep_O2) &&
        isSectionComplete(stepsData.egress_steps.END_DEPRESS) &&
        isSectionComplete(stepsData.egress_steps.DETERMINE_PATH)
      );
    };

  return(
    <div className="container theme_background">
       <div className="text-container text-containerbackground_egress" >
        <h2>Egress Operations</h2>
        <p>
          This section showcases the egress operations involved in our system. 
        </p>

        <Collapsible title="Verify LTV Coordination" isComplete={isSectionComplete(stepsData.egress_steps.VERIFY_LTV)} >
          <label className="checkbox-container">
            <span>PR 1. Verify ping has been received from LTV</span>
            <input 
              type="checkbox"
              checked={stepsData.egress_steps.VERIFY_LTV.Step_1 === 1}
              onChange={() => handleCheckboxChange('VERIFY_LTV', 'Step_1')}     
            />
            <span className="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span>PR 2. Verify worksite POI locations have been provided by LTV</span>
            <input 
              type="checkbox"
              checked={stepsData.egress_steps.VERIFY_LTV.Step_2 === 1}
              onChange={() => handleCheckboxChange('VERIFY_LTV', 'Step_2')}     
            />
            <span className="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span>PR 3. Verify that EV1 has received LTV POIs</span>
            <input 
              type="checkbox"
              checked={stepsData.egress_steps.VERIFY_LTV.Step_3 === 1}
              onChange={() => handleCheckboxChange('VERIFY_LTV', 'Step_3')}     
            />
            <span className="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span>PR 4. Announce that PR operations are complete, will now begin monitoring EVA.</span>
          </label>
          <label className="checkbox-container">
            <span>Turning operations over to EVA.</span>
            <input 
              type="checkbox"
              checked={stepsData.egress_steps.VERIFY_LTV.Step_4 === 1}
              onChange={() => handleCheckboxChange('VERIFY_LTV', 'Step_4')}     
            />
            <span className="checkmark"></span>
          </label>

        </Collapsible>

        <Collapsible title="Connect UIA to DCU and Start Depress" isComplete={isSectionComplete(stepsData.egress_steps.UIA_TO_DCU)} >
          <label className="checkbox-container">
            <span>UIA and DCU 1. V1 verify umbilical connection from UIA to DCU</span>
            <input 
              type="checkbox"
              checked={stepsData.egress_steps.UIA_TO_DCU.Step_1 === 1}
              onChange={() => handleCheckboxChange('UIA_TO_DCU', 'Step_1')}     
            />
            <span className="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span>UIA 2. EV-1, EMU PWR – ON</span>
            <input 
              type="checkbox"
              checked={stepsData.egress_steps.UIA_TO_DCU.Step_2 === 1}
              onChange={() => handleCheckboxChange('UIA_TO_DCU', 'Step_2')}     
            />
            <span className="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span>DCU 3. BATT – UMB</span>
            <input 
              type="checkbox"
              checked={stepsData.egress_steps.UIA_TO_DCU.Step_3 === 1}
              onChange={() => handleCheckboxChange('UIA_TO_DCU', 'Step_3')}     
            />
            <span className="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span>UIA 4. DEPRESS PUMP PWR – ON</span>
            <input 
              type="checkbox"
              checked={stepsData.egress_steps.UIA_TO_DCU.Step_4 === 1}
              onChange={() => handleCheckboxChange('UIA_TO_DCU', 'Step_4')}     
            />
            <span className="checkmark"></span>
          </label>
        </Collapsible>

        <Collapsible title="Prep O2 Tanks" isComplete={isSectionComplete(stepsData.egress_steps.Prep_O2)}>
          <label className="checkbox-container">
            <span>UIA 1. OXYGEN O2 VENT – OPEN </span>
            <input type="checkbox" 
            checked={stepsData.egress_steps.Prep_O2.Step_1 === 1}
            onChange={() => handleCheckboxChange('Prep_O2', 'Step_1')} />
            <span className="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span>HMD2. Wait until both Primary and Secondary OXY tanks are less than 10psi</span>
            <input type="checkbox"
            checked={stepsData.egress_steps.Prep_O2.Step_2 === 1}
            onChange={() => handleCheckboxChange('Prep_O2', 'Step_2')} />
            <span class="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span>UIA 3. OXYGEN O2 VENT – CLOSE </span>
            <input type="checkbox" 
            checked={stepsData.egress_steps.Prep_O2.Step_3 === 1}
            onChange={() => handleCheckboxChange('Prep_O2', 'Step_3')} />
            <span class="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span> DCU 4. OXY – PRI</span>
            <input type="checkbox" 
            checked={stepsData.egress_steps.Prep_O2.Step_4 === 1}
            onChange={() => handleCheckboxChange('Prep_O2', 'Step_4')} />
            <span class="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span>UIA 5. OXYGEN EMU-1 – OPEN</span>
            <input type="checkbox" 
            checked={stepsData.egress_steps.Prep_O2.Step_5 === 1}
            onChange={() => handleCheckboxChange('Prep_O2', 'Step_5')}/>
            <span class="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span>HMD 6. Wait until EV1 and EV2 Primary O2 tanks greater than 3000 psi </span>
            <input type="checkbox" 
            checked={stepsData.egress_steps.Prep_O2.Step_6 === 1}
            onChange={() => handleCheckboxChange('Prep_O2', 'Step_6')} />
            <span class="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span>UIA 7. OXYGEN EMU-1 – CLOSE </span>
            <input type="checkbox" 
            checked={stepsData.egress_steps.Prep_O2.Step_7 === 1}
            onChange={() => handleCheckboxChange('Prep_O2', 'Step_7')} />
            <span class="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span> DCU 8. OXY – SEC</span>
            <input type="checkbox" 
            checked={stepsData.egress_steps.Prep_O2.Step_8 === 1}
            onChange={() => handleCheckboxChange('Prep_O2', 'Step_8')} />
            <span class="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span>UIA 9. OXYGEN EMU-1 – OPEN</span>
            <input type="checkbox"
            checked={stepsData.egress_steps.Prep_O2.Step_9 === 1}
            onChange={() => handleCheckboxChange('Prep_O2', 'Step_9')} />
            <span class="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span>HMD 10. Wait until EV1 and EV2 Secondary O2 tanks greater than 3000 psi</span>
            <input type="checkbox" 
            checked={stepsData.egress_steps.Prep_O2.Step_10 === 1}
            onChange={() => handleCheckboxChange('Prep_O2', 'Step_10')}/>
            <span class="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span>UIA 11. OXYGEN EMU-1 – CLOSE </span>
            <input type="checkbox" 
            checked={stepsData.egress_steps.Prep_O2.Step_11 === 1}
            onChange={() => handleCheckboxChange('Prep_O2', 'Step_11')} />
            <span class="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span>DCU 12. OXY – PRI</span>
            <input type="checkbox"
            checked={stepsData.egress_steps.Prep_O2.Step_12 === 1}
            onChange={() => handleCheckboxChange('Prep_O2', 'Step_12')}/>
            <span class="checkmark"></span>
          </label>

        </Collapsible>

        <Collapsible title="END Depress, Check Switches and Disconnect" isComplete={isSectionComplete(stepsData.egress_steps.END_DEPRESS)}>

        <label className="checkbox-container">
            <span>HMD 1. Wait until SUIT PRESSURE, O2 Pressure = 4 </span>
            <input type="checkbox" 
            checked={stepsData.egress_steps.END_DEPRESS.Step_1 === 1}
            onChange={() => handleCheckboxChange('END_DEPRESS', 'Step_1')}/>
            <span class="checkmark"></span>
         </label>

         <label className="checkbox-container">
            <span>UIA 2. DEPRESS PUMP PWR – OFF </span>
            <input type="checkbox" 
            checked={stepsData.egress_steps.END_DEPRESS.Step_2 === 1}
            onChange={() => handleCheckboxChange('END_DEPRESS', 'Step_2')}/>
            <span class="checkmark"></span>
         </label>

         <label className="checkbox-container">
            <span>DCU 3. BATT – LOCAL </span>
            <input type="checkbox" 
            checked={stepsData.egress_steps.END_DEPRESS.Step_3 === 1}
            onChange={() => handleCheckboxChange('END_DEPRESS', 'Step_3')}/>
            <span class="checkmark"></span>
         </label>

         <label className="checkbox-container">
            <span>UIA 4. EV-1 EMU PWR - OFF </span>
            <input type="checkbox" 
            checked={stepsData.egress_steps.END_DEPRESS.Step_4 === 1}
            onChange={() => handleCheckboxChange('END_DEPRESS', 'Step_4')}/>
            <span class="checkmark"></span>
         </label>

         <label className="checkbox-container">
            <span> DCU 5. Verify OXY – PRI</span>
            <input type="checkbox" 
            checked={stepsData.egress_steps.END_DEPRESS.Step_5 === 1}
            onChange={() => handleCheckboxChange('END_DEPRESS', 'Step_5')}/>
            <span class="checkmark"></span>
         </label>

         <label className="checkbox-container">
            <span>DCU 6. Verify COMMS – A</span>
            <input type="checkbox" 
            checked={stepsData.egress_steps.END_DEPRESS.Step_6 === 1}
            onChange={() => handleCheckboxChange('END_DEPRESS', 'Step_6')}/>
            <span class="checkmark"></span>
         </label>

         <label className="checkbox-container">
            <span>DCU 7. Verify FAN – PRI</span>
            <input type="checkbox" 
            checked={stepsData.egress_steps.END_DEPRESS.Step_7 === 1}
            onChange={() => handleCheckboxChange('END_DEPRESS', 'Step_7')}/>
            <span class="checkmark"></span>
         </label>

         <label className="checkbox-container">
            <span>DCU 8. Verify PUMP – CLOSE</span>
            <input type="checkbox" 
            checked={stepsData.egress_steps.END_DEPRESS.Step_8 === 1}
            onChange={() => handleCheckboxChange('END_DEPRESS', 'Step_8')}/>
            <span class="checkmark"></span>
         </label>

         <label className="checkbox-container">
            <span>DCU 9. Verify CO2 – A</span>
            <input type="checkbox" 
            checked={stepsData.egress_steps.END_DEPRESS.Step_9 === 1}
            onChange={() => handleCheckboxChange('END_DEPRESS', 'Step_9')}/>
            <span class="checkmark"></span>
         </label>

         <label className="checkbox-container">
            <span>UIA and DCU 10. EV1 and EV2 disconnect UIA and DCU umbilical</span>
            <input type="checkbox" 
            checked={stepsData.egress_steps.END_DEPRESS.Step_10 === 1}
            onChange={() => handleCheckboxChange('END_DEPRESS', 'Step_10')}/>
            <span class="checkmark"></span>
         </label>

         <label>
         <span>DCU 11. Verify Comms are working between DCU and PR.</span>
         </label>
          
         <label className="checkbox-container">
            <span>“EV1 to PR, comm check, can you hear me?” PR respond appropriately.</span>
            <input type="checkbox" 
            checked={stepsData.egress_steps.END_DEPRESS.Step_11 === 1}
            onChange={() => handleCheckboxChange('END_DEPRESS', 'Step_11')}/>
            <span class="checkmark"></span>
         </label>

        </Collapsible>

        <Collapsible title="Determine Navigation Path" isComplete={isSectionComplete(stepsData.egress_steps.DETERMINE_PATH)} >
          <label className="checkbox-container">
            <span>EV1 1. Drop pins and determine best path for each POI provided by LTV</span>
            <input 
              type="checkbox"
              checked={stepsData.egress_steps.DETERMINE_PATH.Step_1 === 1}
              onChange={() => handleCheckboxChange('DETERMINE_PATH', 'Step_1')}     
            />
            <span className="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span>EV1 2. Verify the path has been generated. Wait for go from PR</span>
            <input 
              type="checkbox"
              checked={stepsData.egress_steps.DETERMINE_PATH.Step_2 === 1}
              onChange={() => handleCheckboxChange('DETERMINE_PATH', 'Step_2')}     
            />
            <span className="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span>PR 3. Unlock Airlock, announce all clear for EV</span>
            <input 
              type="checkbox"
              checked={stepsData.egress_steps.DETERMINE_PATH.Step_3 === 1}
              onChange={() => handleCheckboxChange('DETERMINE_PATH', 'Step_3')}     
            />
            <span className="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span>EV 4. Exit airlock and begin navigation to worksite</span>
            <input 
              type="checkbox"
              checked={stepsData.egress_steps.DETERMINE_PATH.Step_4 === 1}
              onChange={() => handleCheckboxChange('DETERMINE_PATH', 'Step_4')}     
            />
            <span className="checkmark"></span>
          </label>

        </Collapsible>

        {/* Display the completion message once all sections are complete */}
    {isAllSectionsComplete() && (
      <div className="completion-message">
        <p class="bold-text">All Egress Steps Completed!</p>
      </div>
    )}
    
      <div>
            <button className="egressback_button" onClick={navUIA}> Go back to UIA page</button>
      </div>
      </div>

      
      
      <div className="image-column">
        <div className="image-container image-containerbackground_egress">
          <img className="DCUFront_image" src={DCU_Front} alt="DCU Front" />
        </div>

        <div className="image-container image-containerbackground_egress">
          <img className="SUITS_UIA_PANEL_image" src={SUITS_UIA_PANEL} alt="Panel" />
        </div>
      </div>
    </div>
    
  );
}

export default Egress;