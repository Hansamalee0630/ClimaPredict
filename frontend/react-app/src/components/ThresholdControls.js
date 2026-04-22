import React, { useState, useEffect } from 'react';
import InfoTooltip from './InfoTooltip';
import { Settings, Thermometer, Droplets, Wind } from 'lucide-react';

const GROUPS = [
  {
    label: 'Temperature',
    icon: <Thermometer size={14} />,
    color: '#f97316',
    sliders: [
      { key: 'tmp_w', label: 'Warning Threshold', min: 15, max: 40, step: 1, unit: '°C', type: 'warn' },
      { key: 'tmp_d', label: 'Danger Threshold',  min: 18, max: 45, step: 1, unit: '°C', type: 'danger' },
    ],
  },
  {
    label: 'Humidity',
    icon: <Droplets size={14} />,
    color: '#63dcff',
    sliders: [
      { key: 'hum_w', label: 'Warning Threshold', min: 30, max: 85, step: 1, unit: '%', type: 'warn' },
      { key: 'hum_d', label: 'Danger Threshold',  min: 40, max: 95, step: 1, unit: '%', type: 'danger' },
    ],
  },
  {
    label: 'CO₂',
    icon: <Wind size={14} />,
    color: '#34d399',
    sliders: [
      { key: 'co2_w', label: 'Warning Threshold', min: 300, max: 1500, step: 10, unit: 'ppm', type: 'warn' },
      { key: 'co2_d', label: 'Danger Threshold',  min: 500, max: 2500, step: 10, unit: 'ppm', type: 'danger' },
    ],
  },
];

function Slider({ config, value, onChange }) {
  const typeColor = config.type === 'danger' ? '#f87171' : '#fbbf24';
  const pct = ((value - config.min) / (config.max - config.min)) * 100;

  return (
    <div className="slider-wrap">
      <div className="slider-header">
        <div className="slider-label">
          <span style={{
            display: 'inline-block',
            width: 6, height: 6,
            borderRadius: '50%',
            background: typeColor,
            marginRight: 6,
            verticalAlign: 'middle',
          }} />
          {config.label}
        </div>
        <div className="slider-value">{value}{config.unit}</div>
      </div>
      <div style={{ position: 'relative' }}>
        <input
          type="range"
          min={config.min}
          max={config.max}
          step={config.step}
          value={value}
          onChange={e => onChange(Number(e.target.value))}
          style={{
            width: '100%',
            background: `linear-gradient(90deg, ${typeColor} ${pct}%, rgba(255,255,255,0.08) ${pct}%)`,
          }}
        />
      </div>
    </div>
  );
}

export default function ThresholdControls({ thresholds, onChange }) {
  const [local, setLocal] = useState(thresholds);

  useEffect(() => setLocal(thresholds), [thresholds]);

  useEffect(() => {
    localStorage.setItem('clima_thresholds', JSON.stringify(local));
  }, [local]);

  const update = (key, val) => {
    const n = { ...local, [key]: val };
    setLocal(n);
    onChange(n);
  };

  return (
    <div className="threshold-panel fade-in">
      <div className="threshold-title">
        <div className="threshold-title-icon"><Settings size={14} color="#fff" /></div>
        Alert Controls
        <InfoTooltip title="Alert Configurator">
          <p>Drag the sliders to adjust the thresholds for warning labels and color bands.</p>
          <p>These values are persistently saved and will determine the visual <strong>warning bounds</strong> on the tracking charts as well as the <strong>danger capacity</strong> progress bars on the Overview page.</p>
        </InfoTooltip>
      </div>
      <p className="threshold-desc">
        Configure thresholds to trigger dashboard warnings and status updates in real-time.
      </p>

      {GROUPS.map((group, gi) => (
        <div key={group.label}>
          {gi > 0 && <div className="threshold-divider" />}

          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 14 }}>
            <div style={{
              width: 26, height: 26, borderRadius: 8,
              background: `${group.color}18`,
              border: `1px solid ${group.color}30`,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 13,
            }}>
              {group.icon}
            </div>
            <span style={{ fontSize: 12, fontWeight: 700, color: group.color, letterSpacing: 0.5 }}>
              {group.label.toUpperCase()}
            </span>
          </div>

          {group.sliders.map(slider => (
            <Slider
              key={slider.key}
              config={slider}
              value={local[slider.key]}
              onChange={v => update(slider.key, v)}
            />
          ))}
        </div>
      ))}
    </div>
  );
}
