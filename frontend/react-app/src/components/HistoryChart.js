import React from 'react';
import Plot from 'react-plotly.js';

const CHART_COLORS = {
  temperature: { hist: '#f97316', fore: '#fb923c', fill: 'rgba(249, 115, 22, 0.08)' },
  humidity:    { hist: '#63dcff', fore: '#38bdf8', fill: 'rgba(99, 220, 255, 0.08)'  },
  co2:         { hist: '#34d399', fore: '#6ee7b7', fill: 'rgba(52, 211, 153, 0.08)'  },
};

export default function HistoryChart({ history, forecast, keyName, title, color, thresholds }) {
  const palette = CHART_COLORS[keyName] || {
    hist: color || '#63dcff',
    fore: '#a78bfa',
    fill: 'rgba(167,139,250,0.08)',
  };

  const hist = (history || [])
    .map(r => {
      let val = r?.dht22?.[keyName] ?? r?.ens160?.[keyName] ?? r?.[keyName];
      if (val == null && keyName === 'co2') val = r?.ens160?.eco2 ?? r?.eco2;
      return { x: new Date(r.server_timestamp), y: val ?? null };
    })
    .filter(r => r.y !== null);

  const fore = forecast || [];

  const histX = hist.map(h => h.x);
  const histY = hist.map(h => h.y);

  const foreX = fore.map(f => new Date(f.timestamp));
  const foreY = fore.map(f => f[keyName]);
  const foreLo = fore.map(f => f[`${keyName}_lo`]);
  const foreHi = fore.map(f => f[`${keyName}_hi`]);

  const traces = [];

  if (histX.length > 0) {
    traces.push({
      x: histX,
      y: histY,
      type: 'scatter',
      mode: 'lines',
      name: 'Historical',
      line: {
        color: palette.hist,
        width: 2.5,
        shape: 'spline',
        smoothing: 0.8,
      },
      hovertemplate: `<b>%{y:.1f}</b><br>%{x|%b %d, %H:%M}<extra>Historical</extra>`,
    });
  }

  if (foreX.length > 0) {
    traces.push({
      x: [...foreX, ...foreX.slice().reverse()],
      y: [...foreHi, ...foreLo.slice().reverse()],
      fill: 'toself',
      fillcolor: palette.fill,
      line: { color: 'rgba(0,0,0,0)' },
      name: 'Confidence Range',
      hoverinfo: 'skip',
      showlegend: true,
    });
    traces.push({
      x: foreX,
      y: foreY,
      type: 'scatter',
      mode: 'lines',
      name: 'Forecast',
      line: {
        color: palette.fore,
        dash: 'dot',
        width: 2.5,
        shape: 'spline',
      },
      hovertemplate: `<b>%{y:.1f}</b><br>%{x|%b %d}<extra>Forecast</extra>`,
    });
  }

  const shapes = [];
  if (thresholds) {
    let warnVal = null;
    let dangerVal = null;
    if (keyName === 'temperature') { warnVal = thresholds.tmp_w; dangerVal = thresholds.tmp_d; }
    else if (keyName === 'humidity') { warnVal = thresholds.hum_w; dangerVal = thresholds.hum_d; }
    else if (keyName === 'co2') { warnVal = thresholds.co2_w; dangerVal = thresholds.co2_d; }
    
    if (dangerVal != null) {
      shapes.push({
        type: 'line', xref: 'paper', x0: 0, x1: 1, yref: 'y', y0: dangerVal, y1: dangerVal,
        line: { color: 'rgba(244, 63, 94, 0.7)', width: 1.5, dash: 'dashdot' }
      });
    }
    if (warnVal != null) {
      shapes.push({
        type: 'line', xref: 'paper', x0: 0, x1: 1, yref: 'y', y0: warnVal, y1: warnVal,
        line: { color: 'rgba(250, 204, 21, 0.7)', width: 1.5, dash: 'dashdot' }
      });
    }
  }

  return (
    <div className="chart-panel fade-in">
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 4 }}>
        <div>
          <div className="chart-title">{title}</div>
          <div className="chart-subtitle">
            {histX.length > 0
              ? `${histX.length} data points · last ${Math.round(histX.length / 6)}h`
              : 'Awaiting data...'}
          </div>
        </div>
        {foreX.length > 0 && (
          <div style={{
            fontSize: 10, fontWeight: 700, color: palette.fore,
            background: `${palette.fill}`, border: `1px solid ${palette.fore}40`,
            padding: '4px 10px', borderRadius: 20, letterSpacing: 0.5,
          }}>
            + {foreX.length}d FORECAST
          </div>
        )}
      </div>

      <Plot
        data={traces}
        layout={{
          uirevision: 'true',
          width: undefined,
          height: 340,
          autosize: true,
          margin: { t: 8, r: 12, l: 44, b: 44 },
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'transparent',
          font: {
            family: "'Inter', sans-serif",
            color: '#6b7a99',
            size: 11,
          },
          hovermode: 'x unified',
          hoverlabel: {
            bgcolor: '#0f1629',
            bordercolor: '#1e2a45',
            font: { family: "'Inter', sans-serif", color: '#e2e8f0', size: 12 },
          },
          xaxis: {
            gridcolor: 'rgba(255,255,255,0.04)',
            zerolinecolor: 'rgba(255,255,255,0.06)',
            tickfont: { size: 10 },
            linecolor: 'rgba(255,255,255,0.06)',
          },
          yaxis: {
            gridcolor: 'rgba(255,255,255,0.04)',
            zerolinecolor: 'rgba(255,255,255,0.06)',
            tickfont: { size: 10 },
            linecolor: 'rgba(255,255,255,0.06)',
          },
          shapes: shapes,
          showlegend: traces.length > 1,
          legend: {
            orientation: 'h',
            y: -0.18,
            x: 0,
            bgcolor: 'transparent',
            font: { size: 11 },
          },
        }}
        useResizeHandler={true}
        style={{ width: '100%', height: '100%' }}
        config={{ displayModeBar: false, responsive: true }}
      />
    </div>
  );
}
