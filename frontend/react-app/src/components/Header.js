import React, { useState, useEffect } from 'react';
import { Leaf, Sun, Moon, RotateCcw, RefreshCcw, Activity, Wifi, Brain, Lock, Zap, Clock } from 'lucide-react';

export default function Header({ onRefresh, theme, onToggleTheme, dateFrom, setDateFrom, dateTo, setDateTo }) {
  const [time, setTime] = useState(new Date());
  const [spinning, setSpinning] = useState(false);
  const isLight = theme === 'light';

  useEffect(() => {
    const id = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(id);
  }, []);

  const handleRefresh = () => {
    setSpinning(true);
    onRefresh();
    setTimeout(() => setSpinning(false), 1000);
  };

  const tickerItems = [
    <><Activity size={14} /> LIVE SENSOR STREAM ACTIVE</>,
    <><Wifi size={14} /> MQTT CONNECTED</>,
    <><Brain size={14} /> PREDICTIVE MODEL READY</>,
    <><Lock size={14} /> DATA SECURED & ENCRYPTED</>,
    <><Zap size={14} /> AUTO-REFRESH: 30s</>,
    <><Clock size={14} /> {time.toLocaleTimeString()}</>,
  ];

  return (
    <div className="fade-in" style={{ marginBottom: 0 }}>
      <div className="header">
        <div className="title">
          <div className="title-icon"><Leaf size={24} color="#fff" /></div>
          <div>
            <h1>Clima Predict</h1>
            <div className="subtitle">
              <span className="live-dot" />
              Live Sensor Analytics · {time.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })}
            </div>
          </div>
        </div>

        <div className="controls">
          {/* Date Range Picker */}
          <div className="date-picker-group">
            <div className="date-picker-wrap">
              <span className="date-picker-label">From</span>
              <input 
                type="date" 
                className="date-input" 
                value={dateFrom} 
                onChange={(e) => setDateFrom(e.target.value)}
              />
            </div>
            <div className="date-picker-wrap">
              <span className="date-picker-label">To</span>
              <input 
                type="date" 
                className="date-input" 
                value={dateTo} 
                onChange={(e) => setDateTo(e.target.value)}
              />
            </div>
          </div>

          {/* Theme Toggle */}
          <button className="theme-toggle" onClick={onToggleTheme} title={`Switch to ${isLight ? 'dark' : 'light'} mode`}>
            <div className={`theme-toggle-track ${isLight ? 'light' : 'dark'}`}>
              <div className={`theme-toggle-thumb ${isLight ? 'light' : 'dark'}`} />
            </div>
            {isLight ? 
              <span style={{display: 'flex', alignItems: 'center', gap: 4}}><Sun size={14} /> Light</span> : 
              <span style={{display: 'flex', alignItems: 'center', gap: 4}}><Moon size={14} /> Dark</span>
            }
          </button>

          <button className="btn ghost" onClick={() => window.location.reload()}>
            <RotateCcw size={14} style={{ marginRight: 6 }} /> Reload
          </button>
          <button
            className="btn"
            onClick={handleRefresh}
            style={{ position: 'relative', overflow: 'hidden' }}
          >
            <span style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'transform 0.5s ease',
              transform: spinning ? 'rotate(360deg)' : 'rotate(0deg)',
              marginRight: 6
            }}>
              <RefreshCcw size={14} />
            </span>
            Refresh Data
          </button>
        </div>
      </div>

      {/* Live ticker */}
      <div className="ticker-wrap">
        <div className="ticker-track">
          {[...tickerItems, ...tickerItems].map((item, i) => (
            <span key={i} className="ticker-item" style={{display: 'inline-flex', alignItems: 'center', gap: 6}}>
              {item}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
