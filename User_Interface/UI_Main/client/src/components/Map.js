import React from "react";
import { useState } from "react";
import "./css/MapCSS.css";
import "./css/MasterCSS.css";
import ROCK_YARD_MAP from "./../components/images/PR_MAP_RAW.jpg";

/*
 * Map() - **PAGE**
 *
 * Description:
 *      Page component where Map-specific items will be built
 *      and displayed, such as 2D map, LTV items, etc.
 *
 * Params:
 *     None
 *
 * Returns:
 *     A JSX object to be displayed.
 */

function Map() {
  const [expandedContainer, setExpandedContainer] = useState(null);

  const resizeit = (id) => {
    setExpandedContainer(expandedContainer === id ? null : id);
  };

  const isVisible = (id) => {
    return expandedContainer === null || expandedContainer === id;
  };

  return (
    <div className="body">
      <div className="LeftContainer">
        <div
          className="ParentContainerEVA"
          style={{ flexDirection: expandedContainer ? "column" : "row" }}
        >
          {isVisible("container1") && (
            <div
              className="EVA"
              id="container1"
              style={{
                width: expandedContainer === "container1" ? "100%" : "50%",
                height: expandedContainer === "container1" ? "50vh" : "25vh",
              }}
            >
              <h1>EVA1 CAM</h1>
              <div className="resize">
                <button onClick={() => resizeit("container1")} type="button">
                  {expandedContainer === "container1" ? "Collapse" : "Expand"}
                </button>
              </div>
            </div>
          )}

          {isVisible("container2") && (
            <div
              className="EVA"
              id="container2"
              style={{
                width: expandedContainer === "container2" ? "100%" : "50%",
                height: expandedContainer === "container2" ? "50vh" : "25vh",
              }}
            >
              <h1>EVA2 CAM</h1>
              <div className="resize">
                <button onClick={() => resizeit("container2")} type="button">
                  {expandedContainer === "container2" ? "Collapse" : "Expand"}
                </button>
              </div>
            </div>
          )}
        </div>

        <div
          className="ParentContainerLTV"
          style={{ flexDirection: expandedContainer ? "column" : "row" }}
        >
          {isVisible("container3") && (
            <div
              className="LTV"
              id="container3"
              style={{
                width: expandedContainer === "container3" ? "100%" : "50%",
                height: expandedContainer === "container3" ? "50vh" : "25vh",
              }}
            >
              <h1>LTV TEL</h1>
              <div className="resize">
                <button onClick={() => resizeit("container3")} type="button">
                  {expandedContainer === "container3" ? "Collapse" : "Expand"}
                </button>
              </div>
            </div>
          )}

          {isVisible("container4") && (
            <div
              className="LTV"
              id="container4"
              style={{
                width: expandedContainer === "container4" ? "100%" : "50%",
                height: expandedContainer === "container4" ? "50vh" : "25vh",
              }}
            >
              <h1>LTV CAM</h1>
              <div className="resize">
                <button onClick={() => resizeit("container4")} type="button">
                  {expandedContainer === "container4" ? "Collapse" : "Expand"}
                </button>
              </div>
            </div>
          )}
        </div>

        {expandedContainer === null && (
          <div className="ControlContainer">
            <div className="Controls"></div>
            <h1>Control</h1>
            <div className="arrow-up"></div>
            <div className="arrow-down"></div>
            <div className="arrow-left"></div>
            <div className="arrow-right"></div>
            <div className="arrow-nw"></div>
            <div className="arrow-ne"></div>
            <div className="arrow-sw"></div>
            <div className="arrow-se"></div>
          </div>
        )}
      </div>

      <div className="right_container">
        <div className="timers">
          <p>Mission Timer: HH:MM:SS</p>
          <p>Section Timer: HH:MM:SS</p>
        </div>

        <div className="map_container">
          <img
            className="map-image-container"
            src={ROCK_YARD_MAP}
            alt="Rock yard map"
          />

          <div className="grid-overlay">
            {Array.from({ length: 70 * 110 }).map((_, idx) => (
              <div key={idx} className="grid-cell" />
            ))}
          </div>
        </div>

        <div className="map_controls">
          <button>Add POI</button>
        </div>
      </div>
    </div>
  );
}

export default Map;
