import React, { useState, useEffect } from "react";

function Collapsible({ title, isComplete, children}) {
  const [isOpen, setIsOpen] = useState(false);

  // Auto-collapse when the step is marked complete
  useEffect(() => {
    if (isComplete) {
      setIsOpen(false);
    }
  }, [isComplete]);

  return (
    <div className="collapsible">
      <button
        className={isComplete ? "collapsible-header complete" : "collapsible-header incomplete"}
        onClick={() => setIsOpen(!isOpen)}
      >
        {title} {isOpen ? "▲" : "▼"}
      </button>
      {isOpen && (
        <div className="collapsible-content">{children}</div>
      )}
    </div>
  );
}

export default Collapsible;
