import React from 'react';
import "./css/Mission.css";
/*
* EVA() - **PAGE**
*
* Description:
*      Page component where EVA-specific items will be built
*      and displayed, such as EVA telemetry, tasks, XRF, etc.
*
* Params:
*     None
*
* Returns:
*     A JSX object to be displayed.
*/
function EVA() {
  return (
   
    <div className="Mission">
      

      <div className="Left_column">

        <div className='Unit01_container'>
          <div className="Unit01">
            <h1>Unit 01</h1>
            <p>This is where the vitals of Unit 01 will be displayed.</p>
          </div>
        </div>

        <div className='Unit02_container'>
          <div className="Unit02">
            <h1>Unit 02</h1>
            <p>This is where the vitals of Unit 02 will be displayed.</p>
          </div>
        </div>
      
      </div>

      <div className="Center_column">

        <div className="Warnings_container">
          <div className="Warnings">
            <h1>Warnings</h1>
            <p>This is where Warnings, cautions, & alerts will be displayed.</p>
          </div>
        </div>
        <div className="Tasks_container">
          <div className="Tasks"> 
            <h1>Tasks</h1>
            <p>This is where mission tasks will be displayed.</p>
          </div>
        </div>
        <div className="XRF_container">
          <div className="XRF">
            <h1>X-Ray Data</h1>
            <p>This is where X-ray Spectrometry data will be displayed.</p>
          </div>
        </div>
      
      </div>

      <div className="Right_column">

        <div className="Rover_container">
          <div className="Rover_Telemetry">
            <h1>Rover Telemetry</h1>
            <p>This is where Rover telemetry will be displayed.</p> 
          </div>
        </div>

      </div>

    </div> 
  );
}

export default EVA;