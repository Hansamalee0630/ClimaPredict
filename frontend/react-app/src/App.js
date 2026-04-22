import React, { useEffect, useState } from 'react';
import { getLatest, getHistory } from './services/api';
import Header from './components/Header';
import KPICards from './components/KPICards';
import StatusBanner from './components/StatusBanner';
import HistoryChart from './components/HistoryChart';
import ThresholdControls from './components/ThresholdControls';
import InfoTooltip from './components/InfoTooltip';
import { genForecast } from './components/ForecastGenerator';
import { LayoutGrid, Thermometer, Droplets, Wind, Activity, BrainCircuit, ShieldAlert, ShieldCheck } from 'lucide-react';
import './App.css';

const TABS = [
  { id: 'Overview',       icon: <LayoutGrid size={16} strokeWidth={2.5} />, label: 'Overview'        },
  { id: 'Temperature',    icon: <Thermometer size={16} strokeWidth={2.5} />, label: 'Temperature'     },
  { id: 'Humidity',       icon: <Droplets size={16} strokeWidth={2.5} />, label: 'Humidity'        },
  { id: 'Air Quality',    icon: <Wind size={16} strokeWidth={2.5} />, label: 'Air Quality'     },
  { id: 'Predictive Lab', icon: <Activity size={16} strokeWidth={2.5} />, label: 'Predictive Lab'  },
];

function Tabs({ active, onChange }) {
  return (
    <div className="tabs fade-in" style={{ animationDelay: '0.1s' }}>
      {TABS.map(t => (
        <button
          key={t.id}
          onClick={() => onChange(t.id)}
          className={`tab-btn ${t.id === active ? 'active' : ''}`}
          style={{ display: 'flex', alignItems: 'center', gap: 6 }}
        >
          {t.icon}
          {t.label}
        </button>
      ))}
    </div>
  );
}

// function App() {
//   const [latest, setLatest] = useState(null);
//   const [history, setHistory] = useState([]);
//   const [tab, setTab] = useState('Overview');
//   const [theme, setTheme] = useState(() => localStorage.getItem('clima_theme') || 'dark');
//   const [thresholds, setThresholds] = useState(() => {
//     const raw = localStorage.getItem('clima_thresholds');
//     if (raw) try { return JSON.parse(raw); } catch (e) {}
//     return { tmp_w: 26, tmp_d: 30, hum_w: 50, hum_d: 65, co2_w: 700, co2_d: 1000 };
//   });

//   // Apply theme to root element
//   useEffect(() => {
//     document.documentElement.setAttribute('data-theme', theme);
//     localStorage.setItem('clima_theme', theme);
//   }, [theme]);

//   const toggleTheme = () => setTheme(t => t === 'dark' ? 'light' : 'dark');

//   useEffect(() => {
//     loadData();
//     const id = setInterval(loadData, 30_000);
//     return () => clearInterval(id);
//   }, []);

//   async function loadData() {
//     try { const r1 = await getLatest();    setLatest(r1.data.data); }    catch (e) { console.warn(e); }
//     try { const r2 = await getHistory(72); setHistory(r2.data.data || []); } catch (e) { console.warn(e); }
//   }

//   const forecast    = genForecast(history, 14);
//   const lastReading = latest && latest.data ? latest.data : latest;

//   return (
//     <>
//       <div className="aurora-bg">
//         <div className="aurora-blob blob-1" />
//         <div className="aurora-blob blob-2" />
//         <div className="aurora-blob blob-3" />
//       </div>
//       <div className="container">
//         <Header onRefresh={loadData} theme={theme} onToggleTheme={toggleTheme} />
//         <Tabs active={tab} onChange={setTab} />

//       {/* ── Overview ── */}
//       {tab === 'Overview' && (
//         <div key="overview" className="fade-in">
//           <div style={{ marginBottom: 28 }}>
//             <KPICards history={history} lastReading={lastReading} />
//           </div>

//           <div style={{ display: 'grid', gridTemplateColumns: '1fr 340px', gap: 24, alignItems: 'start' }}>
//             <div>
//               <StatusBanner
//                 label="CO₂"
//                 value={lastReading?.ens160?.eco2 ?? lastReading?.co2 ?? 0}
//                 warn={thresholds.co2_w}
//                 danger={thresholds.co2_d}
//                 unit="ppm"
//               />
//               <HistoryChart
//                 history={history}
//                 forecast={forecast}
//                 keyName="co2"
//                 title="CO₂ History (ppm)"
//                 color="#34d399"
//               />
//             </div>
//             <div>
//               <ThresholdControls thresholds={thresholds} onChange={t => setThresholds(t)} />
//             </div>
//           </div>
//         </div>
//       )}

//       {/* ── Temperature ── */}
//       {tab === 'Temperature' && (
//         <div key="temp" className="panel fade-in">
//           <div className="section-header" style={{ marginBottom: 20 }}>
//             <span className="section-label" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
//               <Thermometer size={14} /> Temperature Monitor
//               <InfoTooltip title="Temperature Monitor">
//                 <p>Real-time readings streaming directly from the local DHT-22 sensor node.</p>
//                 <p>The chart below displays up to 72 hours of rolling historical data.</p>
//               </InfoTooltip>
//             </span>
//             <div className="section-line" />
//           </div>
//           <StatusBanner
//             label="Temperature"
//             value={lastReading?.dht22?.temperature ?? 0}
//             warn={thresholds.tmp_w}
//             danger={thresholds.tmp_d}
//             unit="°C"
//           />
//           <HistoryChart
//             history={history}
//             forecast={forecast}
//             keyName="temperature"
//             title="Temperature (°C)"
//             color="#f97316"
//           />
//         </div>
//       )}

//       {/* ── Humidity ── */}
//       {tab === 'Humidity' && (
//         <div key="hum" className="panel fade-in">
//           <div className="section-header" style={{ marginBottom: 20 }}>
//             <span className="section-label" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
//               <Droplets size={14} /> Humidity Monitor
//               <InfoTooltip title="Humidity Monitor">
//                 <p>Measures the amount of water vapor present in the air.</p>
//                 <p>High humidity can lead to mold growth and device issues. Values between <strong>30-60%</strong> are generally considered comfortable.</p>
//               </InfoTooltip>
//             </span>
//             <div className="section-line" />
//           </div>
//           <StatusBanner
//             label="Humidity"
//             value={lastReading?.dht22?.humidity ?? 0}
//             warn={thresholds.hum_w}
//             danger={thresholds.hum_d}
//             unit="%"
//           />
//           <HistoryChart
//             history={history}
//             forecast={forecast}
//             keyName="humidity"
//             title="Humidity (%)"
//             color="#63dcff"
//           />
//         </div>
//       )}

//       {/* ── Air Quality ── */}
//       {tab === 'Air Quality' && (
//         <div key="air" className="panel fade-in">
//           <div className="section-header" style={{ marginBottom: 20 }}>
//             <span className="section-label" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
//               <Wind size={14} /> Air Quality Monitor
//               <InfoTooltip title="CO₂ / Air Quality">
//                 <p>Estimates ambient Equivalent Carbon Dioxide (eCO₂) levels.</p>
//                 <p>Readings above <strong>1000 ppm</strong> indicate poor ventilation and may cause drowsiness. Ensure proper airflow if values spike.</p>
//               </InfoTooltip>
//             </span>
//             <div className="section-line" />
//           </div>
//           <StatusBanner
//             label="CO₂"
//             value={lastReading?.ens160?.eco2 ?? lastReading?.co2 ?? 0}
//             warn={thresholds.co2_w}
//             danger={thresholds.co2_d}
//             unit="ppm"
//           />
//           <HistoryChart
//             history={history}
//             forecast={forecast}
//             keyName="co2"
//             title="CO₂ (ppm)"
//             color="#34d399"
//           />
//         </div>
//       )}

//       {/* ── Predictive Lab ── */}
//       {tab === 'Predictive Lab' && (
//         <div key="pred" className="panel fade-in">
//           <div className="pred-header">
//             <div>
//               <div className="section-header" style={{ marginBottom: 6 }}>
//                 <span className="section-label" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
//                   <Activity size={14} /> Predictive Lab
//                   <InfoTooltip title="AI Predictive Lab">
//                     <p>The Predictive Lab uses moving averages and statistical variance over the past 72-hours to forecast conditions up to <strong>14 days</strong> ahead.</p>
//                     <p>The shaded glowing areas represent the high/low confidence boundaries for the projections.</p>
//                   </InfoTooltip>
//                 </span>
//                 <div className="section-line" />
//               </div>
//               <p style={{ color: 'var(--muted)', fontSize: 13, marginTop: 4, lineHeight: 1.6 }}>
//                 14-day forecast generated from recent historical hourly medians using statistical smoothing.
//               </p>
//             </div>
//             <div className="pred-badge">AI Forecast</div>
//           </div>

//           <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginTop: 20 }}>
//             <HistoryChart history={history} forecast={forecast} keyName="temperature" title="Temperature Forecast (°C)" />
//             <HistoryChart history={history} forecast={forecast} keyName="humidity"    title="Humidity Forecast (%)" />
//           </div>
//           <div style={{ marginTop: 20 }}>
//             <HistoryChart history={history} forecast={forecast} keyName="co2" title="CO₂ Forecast Overview (ppm)" />
//           </div>
//         </div>
//       )}
//     </div>
//     </>
//   );
// }

function App() {
  const [latest, setLatest] = useState(null);
  const [history, setHistory] = useState([]);
  const [tab, setTab] = useState('Overview');
  const [theme, setTheme] = useState(() => localStorage.getItem('clima_theme') || 'dark');
  const [thresholds, setThresholds] = useState(() => {
    const raw = localStorage.getItem('clima_thresholds');
    if (raw) try { return JSON.parse(raw); } catch (e) {}
    return { tmp_w: 26, tmp_d: 30, hum_w: 50, hum_d: 65, co2_w: 700, co2_d: 1000 };
  });

  // Apply theme to root element
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('clima_theme', theme);
  }, [theme]);

  const toggleTheme = () => setTheme(t => t === 'dark' ? 'light' : 'dark');

  useEffect(() => {
    loadData();
    const id = setInterval(loadData, 5000); // SPED UP TO 5 SECONDS FOR LIVE DEMO
    return () => clearInterval(id);
  }, []);

  async function loadData() {
    try { const r1 = await getLatest();    setLatest(r1.data.data ? r1.data.data : r1.data); }    catch (e) { console.warn(e); }
    try { const r2 = await getHistory(72); setHistory(r2.data.data || []); } catch (e) { console.warn(e); }
  }

  const forecast    = genForecast(history, 14);
  const lastReading = latest;
  
  // EXTRACT AI DATA FROM FLASK BACKEND
  const mlInsights = lastReading?.ml_insights;

  return (
    <>
      <div className="aurora-bg">
        <div className="aurora-blob blob-1" />
        <div className="aurora-blob blob-2" />
        <div className="aurora-blob blob-3" />
      </div>
      <div className="container">
        <Header onRefresh={loadData} theme={theme} onToggleTheme={toggleTheme} />
        <Tabs active={tab} onChange={setTab} />

      {/* ── Overview ── */}
      {tab === 'Overview' && (
        <div key="overview" className="fade-in">
          <div style={{ marginBottom: 28 }}>
            <KPICards history={history} lastReading={lastReading} />
          </div>

          {/* ── NEW: AI INSIGHTS GRID ── */}
          {mlInsights && (
             <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24, marginBottom: 28 }}>
               
               {/* 1-Hour Forecast Card */}
               <div style={{ background: 'rgba(139, 92, 246, 0.1)', border: '1px solid rgba(139, 92, 246, 0.3)', borderRadius: 16, padding: 20, backdropFilter: 'blur(10px)' }}>
                 <div style={{ display: 'flex', alignItems: 'center', gap: 8, color: '#c4b5fd', marginBottom: 12 }}>
                    <BrainCircuit size={18} />
                    <span style={{ fontSize: 13, fontWeight: 600, letterSpacing: 1 }}>AI 1-HOUR FORECAST</span>
                 </div>
                 <div style={{ fontSize: 36, fontWeight: 800, color: '#a78bfa' }}>
                    {mlInsights.predicted_co2_1hr ? mlInsights.predicted_co2_1hr : "---"} 
                    <span style={{ fontSize: 16, fontWeight: 400, marginLeft: 4 }}>ppm</span>
                 </div>
                 <div style={{ fontSize: 12, color: '#8b5cf6', marginTop: 8 }}>Based on Random Forest Temporal Analysis</div>
               </div>

               {/* Anomaly Detection Card */}
               <div style={{ 
                  background: mlInsights.is_anomaly ? 'rgba(244, 63, 94, 0.1)' : 'rgba(16, 185, 129, 0.1)', 
                  border: `1px solid ${mlInsights.is_anomaly ? 'rgba(244, 63, 94, 0.3)' : 'rgba(16, 185, 129, 0.3)'}`, 
                  borderRadius: 16, padding: 20, backdropFilter: 'blur(10px)' 
               }}>
                 <div style={{ display: 'flex', alignItems: 'center', gap: 8, color: mlInsights.is_anomaly ? '#fda4af' : '#6ee7b7', marginBottom: 12 }}>
                    {mlInsights.is_anomaly ? <ShieldAlert size={18} /> : <ShieldCheck size={18} />}
                    <span style={{ fontSize: 13, fontWeight: 600, letterSpacing: 1 }}>ISOLATION FOREST ANOMALY</span>
                 </div>
                 <div style={{ fontSize: 24, fontWeight: 700, color: mlInsights.is_anomaly ? '#f43f5e' : '#10b981', marginTop: 6 }}>
                    {mlInsights.is_anomaly ? "🚨 ANOMALY DETECTED" : "🛡️ ENVIRONMENT NORMAL"}
                 </div>
                 <div style={{ fontSize: 12, color: mlInsights.is_anomaly ? '#fb7185' : '#34d399', marginTop: 12 }}>
                    {mlInsights.is_anomaly ? "Unnatural environmental spike registered." : "No anomalies detected by AI model."}
                 </div>
               </div>

             </div>
          )}

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 340px', gap: 24, alignItems: 'start' }}>
            <div>
              <StatusBanner
                label="CO₂"
                value={lastReading?.ens160?.eco2 ?? lastReading?.co2 ?? 0}
                warn={thresholds.co2_w}
                danger={thresholds.co2_d}
                unit="ppm"
              />
              <HistoryChart
                history={history}
                forecast={forecast}
                keyName="co2"
                title="CO₂ History (ppm)"
                color="#34d399"
              />
            </div>
            <div>
              <ThresholdControls thresholds={thresholds} onChange={t => setThresholds(t)} />
            </div>
          </div>
        </div>
      )}

      {/* ── Temperature ── */}
      {tab === 'Temperature' && (
        <div key="temp" className="panel fade-in">
          <div className="section-header" style={{ marginBottom: 20 }}>
            <span className="section-label" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <Thermometer size={14} /> Temperature Monitor
              <InfoTooltip title="Temperature Monitor">
                <p>Real-time readings streaming directly from the local DHT-22 sensor node.</p>
                <p>The chart below displays up to 72 hours of rolling historical data.</p>
              </InfoTooltip>
            </span>
            <div className="section-line" />
          </div>
          <StatusBanner
            label="Temperature"
            value={lastReading?.dht22?.temperature ?? 0}
            warn={thresholds.tmp_w}
            danger={thresholds.tmp_d}
            unit="°C"
          />
          <HistoryChart
            history={history}
            forecast={forecast}
            keyName="temperature"
            title="Temperature (°C)"
            color="#f97316"
          />
        </div>
      )}

      {/* ── Humidity ── */}
      {tab === 'Humidity' && (
        <div key="hum" className="panel fade-in">
          <div className="section-header" style={{ marginBottom: 20 }}>
            <span className="section-label" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <Droplets size={14} /> Humidity Monitor
              <InfoTooltip title="Humidity Monitor">
                <p>Measures the amount of water vapor present in the air.</p>
                <p>High humidity can lead to mold growth and device issues. Values between <strong>30-60%</strong> are generally considered comfortable.</p>
              </InfoTooltip>
            </span>
            <div className="section-line" />
          </div>
          <StatusBanner
            label="Humidity"
            value={lastReading?.dht22?.humidity ?? 0}
            warn={thresholds.hum_w}
            danger={thresholds.hum_d}
            unit="%"
          />
          <HistoryChart
            history={history}
            forecast={forecast}
            keyName="humidity"
            title="Humidity (%)"
            color="#63dcff"
          />
        </div>
      )}

      {/* ── Air Quality ── */}
      {tab === 'Air Quality' && (
        <div key="air" className="panel fade-in">
          <div className="section-header" style={{ marginBottom: 20 }}>
            <span className="section-label" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <Wind size={14} /> Air Quality Monitor
              <InfoTooltip title="CO₂ / Air Quality">
                <p>Estimates ambient Equivalent Carbon Dioxide (eCO₂) levels.</p>
                <p>Readings above <strong>1000 ppm</strong> indicate poor ventilation and may cause drowsiness. Ensure proper airflow if values spike.</p>
              </InfoTooltip>
            </span>
            <div className="section-line" />
          </div>
          <StatusBanner
            label="CO₂"
            value={lastReading?.ens160?.eco2 ?? lastReading?.co2 ?? 0}
            warn={thresholds.co2_w}
            danger={thresholds.co2_d}
            unit="ppm"
          />
          <HistoryChart
            history={history}
            forecast={forecast}
            keyName="co2"
            title="CO₂ (ppm)"
            color="#34d399"
          />
        </div>
      )}

      {/* ── Predictive Lab ── */}
      {tab === 'Predictive Lab' && (
        <div key="pred" className="panel fade-in">
          <div className="pred-header">
            <div>
              <div className="section-header" style={{ marginBottom: 6 }}>
                <span className="section-label" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                  <Activity size={14} /> Predictive Lab
                  <InfoTooltip title="AI Predictive Lab">
                    <p>The Predictive Lab uses moving averages and statistical variance over the past 72-hours to forecast conditions up to <strong>14 days</strong> ahead.</p>
                    <p>The shaded glowing areas represent the high/low confidence boundaries for the projections.</p>
                  </InfoTooltip>
                </span>
                <div className="section-line" />
              </div>
              <p style={{ color: 'var(--muted)', fontSize: 13, marginTop: 4, lineHeight: 1.6 }}>
                14-day forecast generated from recent historical hourly medians using statistical smoothing.
              </p>
            </div>
            <div className="pred-badge">AI Forecast</div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginTop: 20 }}>
            <HistoryChart history={history} forecast={forecast} keyName="temperature" title="Temperature Forecast (°C)" />
            <HistoryChart history={history} forecast={forecast} keyName="humidity"    title="Humidity Forecast (%)" />
          </div>
          <div style={{ marginTop: 20 }}>
            <HistoryChart history={history} forecast={forecast} keyName="co2" title="CO₂ Forecast Overview (ppm)" />
          </div>
        </div>
      )}
    </div>
    </>
  );
}

export default App;
