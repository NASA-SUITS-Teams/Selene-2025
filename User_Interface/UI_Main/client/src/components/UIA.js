import React from 'react';
import './css/UIACSS.css'

/*
* UIA() - **PAGE**
*
* Description:
*      Page component where UIA tasks and procedures will be
*      displayed.
*
* Params:
*     None
*
* Returns:
*     A JSX object to be displayed which shows two sections
*     for egress/ingress with relevant buttons
*/
function UIA() {
  return(
    <div className='UIA_container'>
      <div className='egress_container'>
        <div>
          <button className="egress_button">Egress</button>
        </div>
      </div>
      <div className='ingress_container'>
        <div>
          <button className='ingress_button'>Ingress</button>

        </div>
      </div>
    </div>
  )
}

export default UIA;