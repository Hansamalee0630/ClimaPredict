import React from 'react';
import { CheckCircle, AlertTriangle, XCircle, Loader } from 'lucide-react';

const STATUS_CONFIG = {
  SAFE: {
    color: '#34d399',
    bg: 'rgba(52, 211, 153, 0.1)',
    border: 'rgba(52, 211, 153, 0.25)',
    glow: '0 0 0 4px rgba(52, 211, 153, 0.15)',
    icon: <CheckCircle size={14} />,
    label: 'SAFE',
  },
  WARNING: {
    color: '#fbbf24',
    bg: 'rgba(251, 191, 36, 0.1)',
    border: 'rgba(251, 191, 36, 0.3)',
    glow: '0 0 0 4px rgba(251, 191, 36, 0.15)',
    icon: <AlertTriangle size={14} />,
    label: 'WARNING',
  },
  DANGER: {
    color: '#f87171',
    bg: 'rgba(248, 113, 113, 0.1)',
    border: 'rgba(248, 113, 113, 0.3)',
    glow: '0 0 0 4px rgba(248, 113, 113, 0.2)',
    icon: <XCircle size={14} />,
    label: 'DANGER',
  },
  LOADING: {
    color: '#6b7a99',
    bg: 'rgba(107, 122, 153, 0.08)',
    border: 'rgba(107, 122, 153, 0.15)',
    glow: 'none',
    icon: <Loader size={14} />,
    label: 'NO DATA',
  },
};

export default function StatusBanner({ label, value, warn, danger, unit }) {
  let statusKey = 'SAFE';
  if (value === 0 || value === null || value === undefined) {
    statusKey = 'LOADING';
  } else if (value >= danger) {
    statusKey = 'DANGER';
  } else if (value >= warn) {
    statusKey = 'WARNING';
  }

  const cfg = STATUS_CONFIG[statusKey];

  return (
    <div
      className="status-banner fade-in"
      style={{
        borderColor: cfg.border,
        background: `linear-gradient(135deg, ${cfg.bg}, rgba(255,255,255,0.01))`,
      }}
    >
      <div>
        <div className="status-banner-label">{label} · Live Reading</div>
        <div className="status-banner-value">
          <span style={{ color: cfg.color }}>
            {value === 0 ? '—' : value}
          </span>
          <span style={{ fontSize: 16, color: 'var(--muted)', fontWeight: 500 }}>{unit}</span>
        </div>
        <div className="status-thresholds">
          Warn: {warn}{unit} &nbsp;·&nbsp; Danger: {danger}{unit}
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 8 }}>
        <div
          className="status-badge"
          style={{
            color: cfg.color,
            background: cfg.bg,
            border: `1px solid ${cfg.border}`,
            boxShadow: cfg.glow,
            display: 'inline-flex',
            alignItems: 'center',
            gap: 6
          }}
        >
          {cfg.icon}
          {cfg.label}
        </div>

        {/* Mini progress bar */}
        {value > 0 && (
          <div style={{ width: 120 }}>
            <div style={{ height: 4, background: 'rgba(255,255,255,0.06)', borderRadius: 4, overflow: 'hidden' }}>
              <div
                style={{
                  height: '100%',
                  width: `${Math.min((value / danger) * 100, 100)}%`,
                  background: `linear-gradient(90deg, ${cfg.color}, ${cfg.color}aa)`,
                  borderRadius: 4,
                  transition: 'width 0.8s cubic-bezier(0.4, 0, 0.2, 1)',
                  boxShadow: `0 0 8px ${cfg.color}55`,
                }}
              />
            </div>
            <div style={{ fontSize: 10, color: 'var(--muted)', marginTop: 4, textAlign: 'right', fontFamily: "'JetBrains Mono', monospace" }}>
              {Math.min(Math.round((value / danger) * 100), 100)}% of limit
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
