import React from 'react';
import "./css/EVA.css";
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
      
      <div className="Top_Row">
        <div className="Unit01">
          <h1>Unit 01</h1>
          <p>This is where the vitals of Unit 01 will be displayed.</p>
        </div>

        <div className="Unit02">
          <h1>Unit 02</h1>
          <p>This is where the vitals of Unit 02 will be displayed.</p>
        </div>
      </div>

      <div className="Middle_Row">

        <div className="Left_Column">
          <div className="XRF">
            <h1>X-Ray Data</h1>
            <p>This is where X-ray Spectrometry data will be displayed.</p>
          </div>

          <div className="XRF-Log">
            <h1>XRF Data Log</h1>
            <p>This is where previous data will be displayed.</p>
          </div>
        </div>

        <div className="Center_Column">
          <div className="Tasks"> 
            <h1>Tasks</h1>
            <p>This is where mission tasks will be displayed.</p>
          </div>
        </div>

        <div className="Right_Column"> 
          <div className="Warnings">
            <h1>Warnings</h1>
            <p>This is where Warnings, cautions, & alerts will be displayed.</p>
          </div>
        </div>

      </div>

      <div className="Bottom_Row">
        <div className="Rover_Telemetry">
          <h1>Rover Telemetry</h1>
          <p>This is where Rover telemetry will be displayed.</p> 
        </div>
      </div>

    </div> 
  );
}

export default EVA;
