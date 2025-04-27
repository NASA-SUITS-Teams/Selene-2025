import React from 'react';
import { NavLink } from 'react-router-dom';  // Import NavLink
import AlertsJSON from './../telemetry_json/alerts.json'
import './css/NavbarCSS.css';

/*
* Navbar() - **Component**
*
* Description:
*      Navbar component to facilitate seamless traversal between
*      different pages while indicating active page.
*      Additionally, there exists a notification system for
*      displaying notification across the application.
*
* Params:
*     None
*
* Returns:
*     A JSX object to be displayed.
*/
function Navbar() {

  // Determines whether there is an active caution or not
  const isCaution = (AlertsJSON) => 
  {
    let cautTally = 0;

    // Oxygen caution detection
    if(AlertsJSON.alerts.oxygen_alert.caution)
      {cautTally++;}

    // Battery caution detection
    if(AlertsJSON.alerts.battery_alert.caution)
      {cautTally++;}

    // Water caution detection
    if(AlertsJSON.alerts.water_alert.caution)
      {cautTally++;}

    // CO2 caution detection
    if(AlertsJSON.alerts.co2_alert.caution) 
      {cautTally++;}

    return cautTally > 0;
  }

  // Determines which caution specifically is active
  const fetchCaution = (AlertsJSON) =>
  {
        let cautTally = 0;
    
    // Oxygen caution detection
    if(AlertsJSON.alerts.oxygen_alert.caution)
      {cautTally++;}

    // Battery caution detection
    if(AlertsJSON.alerts.battery_alert.caution)
      {cautTally++;}

    // Water caution detection
    if(AlertsJSON.alerts.water_alert.caution)
      {cautTally++;}

    // CO2 caution detection
    if(AlertsJSON.alerts.co2_alert.caution) 
      {cautTally++;}

    if(cautTally > 1)
    {return "CAUTION: MULTIPLE";}

    // Oxygen caution
    else if(AlertsJSON.alerts.oxygen_alert.caution)
      {return "CAUTION: OXYGEN";}

    // Battery caution
    else if(AlertsJSON.alerts.battery_alert.caution)
      {return "CAUTION: BATTERY";}

    // Water caution
    else if(AlertsJSON.alerts.water_alert.caution)
      {return "CAUTION: WATER";}

    // CO2 caution
    else if(AlertsJSON.alerts.co2_alert.caution) 
      {return "CAUTION: CO2";}
  }

  // Determines whether there is an active warning or not
const isWarning = (AlertsJSON) => 
  {
    let warnTally = 0;

    // Oxygen warning detection
    if(AlertsJSON.alerts.oxygen_alert.warning)
      {warnTally++;}
  
    // Battery warning detection
    if(AlertsJSON.alerts.battery_alert.warning)
      {warnTally++;}
  
    // Water warning detection
    if(AlertsJSON.alerts.water_alert.warning)
      {warnTally++;}
  
    // CO2 warning detection
    if(AlertsJSON.alerts.co2_alert.warning) 
      {warnTally++;}
  
    return warnTally > 0;
  }
  
  // Determines which warning specifically is active
  const fetchWarning = (AlertsJSON) =>
  {
    let warnTally = 0;

    // Oxygen warning detection
    if(AlertsJSON.alerts.oxygen_alert.warning)
      {warnTally++;}
  
    // Battery warning detection
    if(AlertsJSON.alerts.battery_alert.warning)
      {warnTally++;}
  
    // Water warning detection
    if(AlertsJSON.alerts.water_alert.warning)
      {warnTally++;}
  
    // CO2 warning detection
    if(AlertsJSON.alerts.co2_alert.warning) 
      {warnTally++;}

    if(warnTally > 1)
    {return "WARNING: MULTIPLE";}
    
    // Oxygen warning
    else if(AlertsJSON.alerts.oxygen_alert.warning)
      {return "WARNING: OXYGEN";}
  
    // Battery warning
    else if(AlertsJSON.alerts.battery_alert.warning)
      {return "WARNING: BATTERY";}
  
    // Water warning
    else if(AlertsJSON.alerts.water_alert.warning)
      {return "WARNING: WATER";}
  
    // CO2 warning
    else if(AlertsJSON.alerts.co2_alert.warning) 
      {return "WARNING: CO2";}
  }
  


  return (
    <div className="navbar">
      <div>
        <NavLink 
          to="/mission" 
          className={(
            { isActive }) => 
            {
              if(isActive) 
                if(isWarning(AlertsJSON))
                  return 'navbar-item active-link warn-noti';
                else if(isCaution(AlertsJSON))
                  return 'navbar-item active-link caut-noti';
                else
                  return 'navbar-item active-link'

              else
                if(isWarning(AlertsJSON))
                  return 'navbar-item warn-noti';
                else if(isCaution(AlertsJSON))
                  return 'navbar-item caut-noti';
                else
                  return 'navbar-item'
              }
            }
        >
          Mission
        </NavLink>
        <NavLink 
          to="/map" 
          className={({ isActive }) => (isActive ? 'navbar-item active-link' : 'navbar-item')}
        >
          Map
        </NavLink>
        <NavLink 
          to="/uia" 
          className={({ isActive }) => (isActive ? 'navbar-item active-link' : 'navbar-item')}
        >
          UIA
        </NavLink>
        <NavLink 
          to="/setup" 
          className={({ isActive }) => (isActive ? 'navbar-item active-link' : 'navbar-item')}
        >
          Setup
        </NavLink>

      </div>

      <div className='alert-container'>
        <div className={(isWarning(AlertsJSON) ? "noti warn-noti" : "")}>
          <p>{(isWarning(AlertsJSON) ? fetchWarning(AlertsJSON) : "")}</p>
        </div>
        
        <div className={(isCaution(AlertsJSON) ? "noti caut-noti" : "")}>
          <p>{(isCaution(AlertsJSON) ? fetchCaution(AlertsJSON) : "")}</p>
        </div>
      </div>
      

      <h2 className="team-title">Team Selene</h2>
    </div>
  );
}

export default Navbar;
