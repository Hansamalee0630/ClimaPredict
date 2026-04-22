import React from 'react';
import { Thermometer, Droplets, Wind, Activity } from 'lucide-react';
import InfoTooltip from './InfoTooltip';

const CARDS = [
  {
    key: 'temperature',
    title: 'Temperature',
    unit: '°C',
    icon: <Thermometer color="#f97316" />,
    gradient: 'linear-gradient(135deg, #f97316, #ef4444)',
    glowColor: 'rgba(249, 115, 22, 0.25)',
    badgeBg: 'rgba(249, 115, 22, 0.12)',
    badgeColor: '#fb923c',
    borderColor: 'rgba(249, 115, 22, 0.2)',
    iconBg: 'rgba(249, 115, 22, 0.15)',
  },
  {
    key: 'humidity',
    title: 'Humidity',
    unit: '%',
    icon: <Droplets color="#38bdf8" />,
    gradient: 'linear-gradient(135deg, #63dcff, #3b82f6)',
    glowColor: 'rgba(99, 220, 255, 0.25)',
    badgeBg: 'rgba(99, 220, 255, 0.12)',
    badgeColor: '#63dcff',
    borderColor: 'rgba(99, 220, 255, 0.2)',
    iconBg: 'rgba(99, 220, 255, 0.15)',
  },
  {
    key: 'co2',
    title: 'CO₂ Level',
    unit: 'ppm',
    icon: <Wind color="#10b981" />,
    gradient: 'linear-gradient(135deg, #34d399, #10b981)',
    glowColor: 'rgba(52, 211, 153, 0.25)',
    badgeBg: 'rgba(52, 211, 153, 0.12)',
    badgeColor: '#34d399',
    borderColor: 'rgba(52, 211, 153, 0.2)',
    iconBg: 'rgba(52, 211, 153, 0.15)',
  },
];

function Card({ title, value, unit, badge, index, meta }) {
  return (
    <div
      className="kpi-card fade-in"
      style={{
        animationDelay: `${index * 0.1}s`,
        borderColor: meta.borderColor,
      }}
    >
      {/* Top gradient bar */}
      <div className="accent-bar" style={{ background: meta.gradient }} />

      {/* Icon */}
      <div
        className="kpi-icon"
        style={{
          background: meta.iconBg,
          boxShadow: `0 4px 12px ${meta.glowColor}`,
        }}
      >
        {meta.icon}
      </div>

      <div className="kpi-label">{title}</div>
      <div className="kpi-val">
        <span>{value}</span>
        <span className="kpi-unit">{unit}</span>
      </div>

      <div
        className="kpi-badge"
        style={{
          background: meta.badgeBg,
          color: meta.badgeColor,
          border: `1px solid ${meta.borderColor}`,
          display: 'inline-flex',
          alignItems: 'center',
          gap: 4
        }}
      >
        <Activity size={12} strokeWidth={3} /> {badge}
      </div>
    </div>
  );
}

export default function KPICards({ history, lastReading }) {
  const mean = (arr, key) => {
    if (!arr || arr.length === 0) return '--';
    const vals = arr
      .map(r => {
        const v = r?.dht22?.[key] ?? r?.ens160?.[key] ?? r?.[key];
        return typeof v === 'number' ? v : null;
      })
      .filter(x => x != null);
    if (vals.length === 0) return '--';
    return (vals.reduce((a, b) => a + b, 0) / vals.length).toFixed(
      key === 'temperature' ? 1 : 0
    );
  };

  const values = [
    mean(history, 'temperature'),
    mean(history, 'humidity'),
    mean(history, 'eco2') !== '--' ? mean(history, 'eco2') : mean(history, 'co2'),
  ];

  return (
    <>
      <div className="section-header" style={{ marginBottom: 16 }}>
        <span className="section-label" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          Live KPI Metrics
          <InfoTooltip title="KPI Metrics">
            <p>Calculates the <strong>grand mean</strong> (average) across the entire 72-hour loaded historical dataset.</p>
          </InfoTooltip>
        </span>
        <div className="section-line" />
      </div>
      <div className="kpi-grid">
        {CARDS.map((card, i) => (
          <Card
            key={card.key}
            title={card.title}
            value={values[i]}
            unit={card.unit}
            badge="72h Average"
            index={i}
            meta={card}
          />
        ))}
      </div>
    </>
  );
}
