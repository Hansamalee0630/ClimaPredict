import React, { useState, useRef, useEffect } from 'react';
import { HelpCircle, X } from 'lucide-react';
import './Tooltip.css';

export default function InfoTooltip({ title, children }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    function handleClickOutside(event) {
      if (ref.current && !ref.current.contains(event.target)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="tooltip-container" ref={ref}>
      <button 
        className={`tooltip-trigger ${open ? 'active' : ''}`}
        onClick={() => setOpen(!open)}
        title="More info"
      >
        <HelpCircle size={14} />
      </button>

      {open && (
        <div className="tooltip-popup fade-in-scale">
          <div className="tooltip-header">
            <h4>{title || 'Information'}</h4>
            <button className="tooltip-close" onClick={() => setOpen(false)}>
              <X size={14} />
            </button>
          </div>
          <div className="tooltip-content">
            {children}
          </div>
        </div>
      )}
    </div>
  );
}
