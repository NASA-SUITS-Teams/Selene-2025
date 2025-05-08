import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import DCU_Front from './../images/DCU_Front.jpg'
import SUITS_UIA_PANEL from "./../images/SUITS_UIA_PANEL.jpg";
import './../css/MasterCSS.css'
import './../css/UIACSS.css'
import './../css/UIASubpageCSS.css'
import Collapsible from "./../Collapsible";

const initialData = {
"ingress_steps":
{

      "UIA_TO_DCU": 
      {
        "Step_1": 0,
        "Step_2": 0,
        "Step_3": 0
      },

      "Vent_O2_Tanks":
      {
          "Step_1": 0,
          "Step_2": 0,
          "Step_3": 0
      },

      "Empty_Water_Tanks": 
      {
        "Step_1": 0,
        "Step_2": 0,
        "Step_3": 0,
        "Step_4": 0
      },

      "Disconnect_UIA_DCU": 
      {
        "Step_1": 0,
        "Step_2": 0
      },      


  }

}
/*
* Ingress() - **PAGE**
*
* Description:
*      Page component where specifically ingress operations will
*      be displayed 
*
* Params:
*     None
*
* Returns:
*     A JSX object to be displayed.
*/
function Ingress() {
  const navigate = useNavigate();
    
    const navUIA = () =>
    {
      navigate('/uia');
    }

  const [stepsData, setStepsData] = useState(initialData);
  
    const handleCheckboxChange = (section, step) => {
      setStepsData((prevData) => {
        const updatedSection = { ...prevData.ingress_steps[section], [step]: prevData.ingress_steps[section][step] === 0 ? 1 : 0 };
        return {
          ...prevData,
          ingress_steps: {
            ...prevData.ingress_steps,
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
          isSectionComplete(stepsData.ingress_steps.UIA_TO_DCU) &&
          isSectionComplete(stepsData.ingress_steps.Vent_O2_Tanks) &&
          isSectionComplete(stepsData.ingress_steps.Empty_Water_Tanks) &&
          isSectionComplete(stepsData.ingress_steps.Disconnect_UIA_DCU)
        );
      };
  
  return(    
    <div className="container theme_background">
    <div className="text-container text-containerbackground_ingress">
     <h2>Ingress Operations</h2>
     <p>
       This section showcases the Ingress operations involved in our system. 
     </p>


     <Collapsible title="END Depress, Check Switches and Disconnect" isComplete={isSectionComplete(stepsData.ingress_steps.UIA_TO_DCU)} >
     <label className="checkbox-container">
            <span>UIA and DCU 1. EV1 connect UIA and DCU umbilical</span>
            <input type="checkbox" 
            checked={stepsData.ingress_steps.UIA_TO_DCU.Step_1 === 1}
            onChange={() => handleCheckboxChange('UIA_TO_DCU', 'Step_1')}/>
            <span class="checkmark"></span>
      </label>

      <label className="checkbox-container">
            <span>UIA 2. EV-1 EMU PWR - ON</span>
            <input type="checkbox" 
            checked={stepsData.ingress_steps.UIA_TO_DCU.Step_2 === 1}
            onChange={() => handleCheckboxChange('UIA_TO_DCU', 'Step_2')}/>
            <span class="checkmark"></span>
      </label>

      <label className="checkbox-container">
            <span>DCU 3. BATT - UMB</span>
            <input type="checkbox" 
            checked={stepsData.ingress_steps.UIA_TO_DCU.Step_3 === 1}
            onChange={() => handleCheckboxChange('UIA_TO_DCU', 'Step_3')}/>
            <span class="checkmark"></span>
      </label>

     </Collapsible> 


     <Collapsible title="Vent O2 Tanks" isComplete={isSectionComplete(stepsData.ingress_steps.Vent_O2_Tanks)}>
       <label className="checkbox-container">
              <span>UIA 1. OXYGEN O2 VENT - OPEN</span>
              <input type="checkbox" 
              checked={stepsData.ingress_steps.Vent_O2_Tanks.Step_1 === 1}
              onChange={() => handleCheckboxChange('Vent_O2_Tanks', 'Step_1')}/>
              <span class="checkmark"></span>
        </label>

        <label className="checkbox-container">
              <span>HMD 2. Wait until both Primary and Secondary OXY tanks are less than 10 psi</span>
              <input type="checkbox" 
              checked={stepsData.ingress_steps.Vent_O2_Tanks.Step_2 === 1}
              onChange={() => handleCheckboxChange('Vent_O2_Tanks', 'Step_2')}/>
              <span class="checkmark"></span>
        </label>

        <label className="checkbox-container">
              <span>UIA 3. OXYGEN O2 VENT - CLOSE</span>
              <input type="checkbox" 
              checked={stepsData.ingress_steps.Vent_O2_Tanks.Step_3 === 1}
              onChange={() => handleCheckboxChange('Vent_O2_Tanks', 'Step_3')}/>
              <span class="checkmark"></span>
        </label>


     </Collapsible>

     <Collapsible title="Empty Water Tanks" isComplete={isSectionComplete(stepsData.ingress_steps.Empty_Water_Tanks)}>

         <label className="checkbox-container">
            <span>DCU 1. PUMP – OPEN</span>
            <input 
              type="checkbox"
              checked={stepsData.ingress_steps.Empty_Water_Tanks.Step_1 === 1}
              onChange={() => handleCheckboxChange('Empty_Water_Tanks', 'Step_1')}     
            />
            <span className="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span>UIA 2. EV-1 WASTER WATER - OPEN</span>
            <input 
              type="checkbox"
              checked={stepsData.ingress_steps.Empty_Water_Tanks.Step_2 === 1}
              onChange={() => handleCheckboxChange('Empty_Water_Tanks', 'Step_2')}     
            />
            <span className="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span>HMD 3. Wait until both Primary and Secondary OXY tanks are less than 10 psi</span>
            <input 
              type="checkbox"
              checked={stepsData.ingress_steps.Empty_Water_Tanks.Step_3 === 1}
              onChange={() => handleCheckboxChange('Empty_Water_Tanks', 'Step_3')}     
            />
            <span className="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span>UIA 4. EV-1 WASTER WATER - CLOSE</span>
            <input 
              type="checkbox"
              checked={stepsData.ingress_steps.Empty_Water_Tanks.Step_4 === 1}
              onChange={() => handleCheckboxChange('Empty_Water_Tanks', 'Step_4')}     
            />
            <span className="checkmark"></span>
          </label>

     
     </Collapsible>

     <Collapsible title="Disconnect UIA from DCU" isComplete={isSectionComplete(stepsData.ingress_steps.Disconnect_UIA_DCU)}>

         <label className="checkbox-container">
            <span>UIA 1. EV-1 EMU PWR - OFF</span>
            <input 
              type="checkbox"
              checked={stepsData.ingress_steps.Disconnect_UIA_DCU.Step_1 === 1}
              onChange={() => handleCheckboxChange('Disconnect_UIA_DCU', 'Step_1')}     
            />
            <span className="checkmark"></span>
          </label>

          <label className="checkbox-container">
            <span>DCU 2. EV-1 disconnect umbilical</span>
            <input 
              type="checkbox"
              checked={stepsData.ingress_steps.Disconnect_UIA_DCU.Step_2 === 1}
              onChange={() => handleCheckboxChange('Disconnect_UIA_DCU', 'Step_2')}     
            />
            <span className="checkmark"></span>
          </label>

      </Collapsible>
          {/* Display the completion message once all sections are complete */}
    {isAllSectionsComplete() && (
      <div className="completion-message">
        <p class="bold-text">All Ingress Steps Completed!</p>
      </div>
    )}
    <div>
            <button className="ingressback_button" onClick={navUIA}>Go back to UIA page</button>
      </div>

   </div>
   
   <div className="image-column">
     <div className="image-container image-containerbackground_ingress">
       <img className="DCUFront_image" src={DCU_Front} alt="DCU Front" />
     </div>

     <div className="image-container image-containerbackground_ingress">
       <img className="SUITS_UIA_PANEL_image" src={SUITS_UIA_PANEL} alt="Panel" />
     </div>
   </div>
 </div>
  )
}

export default Ingress;