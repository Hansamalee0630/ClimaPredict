import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
from streamlit_lottie import st_lottie
from datetime import datetime, timedelta, date

# ── PAGE CONFIGURATION ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Clima Predict - Sensor Lab",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── INITIALIZE SESSION STATE FOR THRESHOLDS ──────────────────────────────────
defaults = {
    "tmp_w": 26, "tmp_d": 30,
    "hum_w": 60, "hum_d": 75,
    "co2_w": 700, "co2_d": 1000,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── CSS STYLING (Kept your beautiful Glassmorphism!) ──────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
    --bg: #09090b;
    --bg1: rgba(24, 24, 27, 0.4);
    --bg2: rgba(39, 39, 42, 0.4);
    --a1: #00f0ff;
    --muted: #a1a1aa;
    --border: rgba(255, 255, 255, 0.08);
}

html, body, [class*="css"] { font-family: 'Outfit', sans-serif; color: #e4e4e7; }
[data-testid="stAppViewContainer"] {
    background: var(--bg);
    background-image: radial-gradient(circle at 10% 20%, rgba(0, 240, 255, 0.05) 0%, transparent 40%),
                      radial-gradient(circle at 90% 80%, rgba(255, 0, 85, 0.05) 0%, transparent 40%);
    background-attachment: fixed;
}
[data-testid="stHeader"] { background: rgba(9, 9, 11, 0.5) !important; backdrop-filter: blur(12px) !important; }
.block-container { padding-top: 3.5rem !important; padding-bottom: 2rem !important; }
[data-testid="collapsedControl"] { display: none; }

.kpi-card {
    background: var(--bg1); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border); border-radius: 20px; padding: 24px; position: relative; overflow: hidden;
    height: 165px; display: flex; flex-direction: column; justify-content: space-between;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.kpi-card:hover { transform: translateY(-5px); box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5); border-color: rgba(255, 255, 255, 0.15); }
.kpi-card::before { content:''; position:absolute; top:0; left:0; right:0; height:4px; opacity: 0.8; }
.kc-teal::before   { background: linear-gradient(90deg, #00f0ff, #005ce6); box-shadow: 0 0 10px #00f0ff; }
.kc-indigo::before { background: linear-gradient(90deg, #8b5cf6, #d946ef); box-shadow: 0 0 10px #8b5cf6; }
.kc-amber::before  { background: linear-gradient(90deg, #f59e0b, #ef4444); box-shadow: 0 0 10px #f59e0b; }

.kpi-header { display: flex; justify-content: space-between; align-items: flex-start; }
.kpi-label { font-family:'JetBrains Mono', monospace; font-size:12px; letter-spacing:1px; text-transform:uppercase; color:#d4d4d8; font-weight: 500;}
.kpi-val   { font-family:'Outfit', sans-serif; font-size:48px; font-weight:700; line-height:1; color: #ffffff; text-shadow: 0 0 20px rgba(255,255,255,0.1); }
.kpi-unit  { font-family:'JetBrains Mono', monospace; font-size:14px; color:var(--muted); margin-left:6px; font-weight: 400; }

.stat-badge {
    font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700; letter-spacing: 1.5px;
    padding: 6px 12px; border-radius: 30px; text-transform: uppercase; box-shadow: 0 0 10px rgba(0,0,0,0.2) inset;
}
.sb-low  { background: rgba(0, 240, 255, 0.1); color: #00f0ff; border: 1px solid rgba(0, 240, 255, 0.3); }
.sb-med  { background: rgba(245, 158, 11, 0.1); color: #fcd34d; border: 1px solid rgba(245, 158, 11, 0.3); }
.sb-high { background: rgba(244, 63, 94, 0.1); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.3); }

.sh { font-family:'JetBrains Mono', monospace; font-size:12px; letter-spacing:3px; text-transform:uppercase; color:var(--muted); border-left: 3px solid var(--a1); padding-left:14px; margin: 40px 0 20px; }

.stTabs [data-baseweb="tab-list"] { gap: 16px; background: transparent; border: none; padding-bottom: 16px; }
.stTabs [data-baseweb="tab"] { font-family: 'Outfit', sans-serif !important; font-size: 15px !important; font-weight: 500 !important; color: var(--muted) !important; background: var(--bg1) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; padding: 12px 28px !important; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important; backdrop-filter: blur(10px); }
.stTabs [data-baseweb="tab"]:hover { transform: translateY(-2px); border-color: rgba(255,255,255,0.3) !important; color: #fff !important; }
.stTabs [aria-selected="true"] { background: rgba(255,255,255,0.05) !important; border-color: var(--a1) !important; color: #fff !important; box-shadow: 0 0 15px rgba(0,240,255,0.2), inset 0 0 10px rgba(0,240,255,0.1) !important; text-shadow: 0 0 8px rgba(0,240,255,0.5); }

.status-banner { padding: 20px 24px; border-radius: 16px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; border: 1px solid; backdrop-filter: blur(16px); }
.status-low { background: rgba(0, 240, 255, 0.05); border-color: rgba(0, 240, 255, 0.2); color: #00f0ff; }
.status-med { background: rgba(245, 158, 11, 0.05); border-color: rgba(245, 158, 11, 0.2); color: #fcd34d; }
.status-high { background: rgba(244, 63, 94, 0.05); border-color: rgba(244, 63, 94, 0.2); color: #fb7185; }
.tab-desc { font-size: 16px; color: #a1a1aa; margin-bottom: 30px; line-height: 1.6; font-weight: 300; }
</style>
""", unsafe_allow_html=True)

# ── API LOGIC & DATA FETCHING ────────────────────────────────────────────────
API_LATEST = "http://127.0.0.1:5000/api/latest"
API_HISTORY = "http://127.0.0.1:5000/api/history"

TODAY         = date.today()
FORECAST_DAYS = 14          

PARAMS = {
    "temperature": dict(color="#00f0ff"),
    "humidity":    dict(color="#8b5cf6"),
    "pressure":    dict(color="#fbbf24"),
    "co2":         dict(color="#f59e0b"),
}

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

@st.cache_data(ttl=5)
def fetch_historical_data():
    """Fetches real history from Flask API"""
    try:
        response = requests.get(f"{API_HISTORY}?hours=72") # Get last 3 days
        if response.status_code == 200:
            raw_data = response.json()["data"]
            flat_data = []
            for row in raw_data:
                flat_data.append({
                    "timestamp": row.get("server_timestamp"),
                    "temperature": row.get("dht22", {}).get("temperature"),
                    "humidity": row.get("dht22", {}).get("humidity"),
                    "co2": row.get("ens160", {}).get("eco2"),
                    "pressure": row.get("bmp280", {}).get("pressure_hpa")
                })
            df = pd.DataFrame(flat_data)
            if not df.empty:
                # df['timestamp'] = pd.to_datetime(df['timestamp'])
                df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize(None)
                # Drop rows where everything is NaN (warmup period)
                df = df.dropna(subset=['temperature', 'co2'], how='all')
                return df
    except Exception as e:
        pass
    # Empty fallback so it doesn't crash
    return pd.DataFrame(columns=["timestamp", "temperature", "humidity", "co2", "pressure"])

@st.cache_data(ttl=60)
def gen_forecast(hist_df, days_ahead=14):
    """Generates a predictive forecast based on real API data"""
    if hist_df.empty or len(hist_df) < 10:
        return pd.DataFrame(columns=["timestamp", "temperature", "humidity", "co2", "pressure"])
        
    basis  = hist_df.copy()
    basis["hour"] = basis["timestamp"].dt.hour
    cols = ["temperature","humidity","pressure","co2"]
    
    # Calculate trends based on real data
    hourly_median = basis.groupby("hour")[cols].median().fillna(method='ffill').fillna(method='bfill')
    hourly_std    = basis.groupby("hour")[cols].std().fillna(1)
    
    rows = []
    for i in range(days_ahead * 24 * 4):
        ts = datetime.combine(TODAY, datetime.min.time()) + timedelta(minutes=i*15)
        h = ts.hour
        row = {"timestamp": ts}
        for c in cols:
            base_val = hourly_median.loc[h, c] if h in hourly_median.index else basis[c].median()
            row[c] = round(float(base_val), 2)
            row[f"{c}_lo"] = round(float(base_val - 1.5 * (hourly_std.loc[h, c] if h in hourly_std.index else 1)), 2)
            row[f"{c}_hi"] = round(float(base_val + 1.5 * (hourly_std.loc[h, c] if h in hourly_std.index else 1)), 2)
        rows.append(row)
    return pd.DataFrame(rows)

def PL(**kw):
    base = dict(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Outfit", color="#a1a1aa"), margin=dict(l=10, r=10, t=40, b=10),
        hovermode="x unified", dragmode="zoom",
        xaxis=dict(gridcolor="rgba(255,255,255,0.03)", showgrid=True, zeroline=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.03)", showgrid=True, zeroline=False)
    )
    base.update(kw)
    return base

# ── CENTERED HEADER ──────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; margin-top: 10px; margin-bottom: 30px;">
    <div style="font-size: 65px; line-height: 1; margin-bottom: 15px; filter: drop-shadow(0 0 20px rgba(0,240,255,0.4));">🌿</div>
    <div style="font-family: 'Outfit', sans-serif; font-size: 52px; font-weight: 800; letter-spacing: 4px; line-height: 1.1; background: -webkit-linear-gradient(45deg, #00f0ff, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 0 30px rgba(0,240,255,0.2);">CLIMA PREDICT</div>
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 14px; color: #a1a1aa; letter-spacing: 8px; margin-top: 12px; font-weight: 500;">LIVE SENSOR ANALYTICS DASHBOARD</div>
</div>
""", unsafe_allow_html=True)

# ── GLOBAL FILTERS ───────────────────────────────────────────────────────────
c_spacer1, c_refresh, c_spacer2 = st.columns([4, 2, 4])
with c_refresh:
    st.markdown(f'<div style="font-family:\'JetBrains Mono\';font-size:11px;color:#a1a1aa;margin-bottom:8px;text-align:center;">LAST SYNC: {datetime.now().strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)
    if st.button("⟳ Sync with Database", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
st.markdown("<br>", unsafe_allow_html=True)

# ── PREPARE DATA ──────────────────────────────────────────────────────────────
df_h = fetch_historical_data()
df_f = gen_forecast(df_h, FORECAST_DAYS)

actual_cols = ["timestamp","temperature","humidity","pressure","co2"]
if not df_h.empty:
    df_combined = pd.concat([df_h[actual_cols], df_f[actual_cols] if not df_f.empty else pd.DataFrame(columns=actual_cols)], ignore_index=True).sort_values("timestamp")
    df = df_h.copy()
    # Get newest valid reading
    last_reading = df.iloc[-1].fillna(0)
else:
    df = pd.DataFrame(columns=actual_cols)
    last_reading = {"temperature": 0, "humidity": 0, "co2": 0, "pressure": 0}

# ── HELPER FUNCTIONS ──────────────────────────────────────────────────────────
def get_status_info(val, warn, danger):
    if pd.isna(val) or val == 0: return "LOADING", "sb-low"
    if val >= danger: return "DANGER", "sb-high"
    if val >= warn: return "MODERATE", "sb-med"
    return "SAFE", "sb-low"

def render_status_banner(val, warn, danger, unit, label):
    if pd.isna(val) or val == 0:
        val_str = "--"
        cls, status, icon = "status-low", "AWAITING SENSOR DATA", "⏳"
    elif val >= danger:
        val_str = f"{val:.1f}"
        cls, status, icon = "status-high", "DANGER (Critical)", "🚨"
    elif val >= warn:
        val_str = f"{val:.1f}"
        cls, status, icon = "status-med", "MODERATE (Warning)", "⚠️"
    else:
        val_str = f"{val:.1f}"
        cls, status, icon = "status-low", "SAFE (Stable)", "✅"
    
    st.markdown(f"""
    <div class="status-banner {cls}">
        <div>
            <div style="font-size: 0.85rem; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; font-weight:500; opacity: 0.8;">Current {label}</div>
            <div style="font-size: 2rem; font-weight: 700; margin-top: 4px;">{val_str} <span style="font-size:1.1rem; font-weight: 400; opacity: 0.8;">{unit}</span></div>
        </div>
        <div style="text-align:right;">
            <div style="font-size: 1.3rem; font-weight: 700; margin-bottom: 4px;">{icon} {status}</div>
            <div style="font-size: 0.85rem; opacity: 0.7; font-family: 'JetBrains Mono', monospace;">Warn {warn}{unit} | Danger {danger}{unit}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def kpi_cards():
    t_val = df['temperature'].mean() if not df.empty else 0
    h_val = df['humidity'].mean() if not df.empty else 0
    c_val = df['co2'].mean() if not df.empty else 0

    cards = [
        ("kc-teal", "🌡️", "TEMPERATURE", f"{t_val:.1f}" if t_val else "--", "°C", *get_status_info(t_val, st.session_state.tmp_w, st.session_state.tmp_d)),
        ("kc-indigo", "💧", "HUMIDITY", f"{h_val:.1f}" if h_val else "--", "%", *get_status_info(h_val, st.session_state.hum_w, st.session_state.hum_d)),
        ("kc-amber", "💨", "CO₂", f"{c_val:.0f}" if c_val else "--", "ppm", *get_status_info(c_val, st.session_state.co2_w, st.session_state.co2_d)),
    ]
    
    cols = st.columns(len(cards))
    for col_, (cls, icon, lbl, val, unit, s_text, s_cls) in zip(cols, cards):
        with col_:
            st.markdown(f"""
            <div class="kpi-card {cls}">
                <div class="kpi-header">
                    <div class="kpi-label">{icon} {lbl}</div>
                    <div class="stat-badge {s_cls}">{s_text}</div>
                </div>
                <div>
                    <span class="kpi-val">{val}</span><span class="kpi-unit">{unit}</span>
                </div>
            </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

def plot_forecast_chart(col_key, color, title, unit, warn_val, danger_val):
    fig = go.Figure()
    
    if not df_h.empty:
        dh_s = df_h.sort_values("timestamp")
        fig.add_trace(go.Scatter(
            x=dh_s["timestamp"], y=dh_s[col_key].rolling(4,min_periods=1).mean(), 
            name="Historical (API)", line=dict(color=color,width=2.5), fill="tozeroy", 
            fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},.05)"
        ))
        
    if not df_f.empty:
        dfs = df_f.sort_values("timestamp")
        fig.add_trace(go.Scatter(
            x=pd.concat([dfs["timestamp"],dfs["timestamp"][::-1]]), 
            y=pd.concat([dfs[f"{col_key}_hi"],dfs[f"{col_key}_lo"][::-1]]), 
            fill="toself", fillcolor="rgba(167,139,250,.08)", line=dict(color="rgba(0,0,0,0)"), 
            name="ML Confidence"
        ))
        fig.add_trace(go.Scatter(
            x=dfs["timestamp"], y=dfs[col_key], name="ML Forecast", 
            line=dict(color="#a78bfa",width=2,dash="dot")
        ))
    
    if warn_val:
        fig.add_hline(y=warn_val, line_dash="dash", line_color="#ffd166")
        fig.add_annotation(x=0.01, y=warn_val, xref="paper", yref="y", text="Warn", showarrow=False, font=dict(color="#ffd166", size=10), yanchor="bottom")
        
    if danger_val:
        fig.add_hline(y=danger_val, line_dash="dash", line_color="#ff5e7e")
        fig.add_annotation(x=0.01, y=danger_val, xref="paper", yref="y", text="Danger", showarrow=False, font=dict(color="#ff5e7e", size=10), yanchor="bottom")
    
    today_dt = datetime.now()
    fig.add_vline(x=today_dt, line_dash="dash", line_color="#72d0ff", opacity=0.8)
    fig.add_annotation(x=today_dt, y=1.02, xref="x", yref="paper", text="LIVE", showarrow=False, font=dict(color="#72d0ff", size=10, family="JetBrains Mono"))
    
    if title == "Humidity":
        fig.add_hline(y=60, line_dash="dash", line_width=3, line_color="#ff5e7e")
        fig.add_annotation(x=0.5, y=60, xref="paper", yref="y", text="EPA Mold Risk Limit (60% RH)", showarrow=False, font=dict(color="#ff5e7e", size=13), yanchor="bottom")

    fig.update_layout(title=f"{title} Predictive Model", height=340, **PL())
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ── MAIN TABS ─────────────────────────────────────────────────────────────────
tab_overview, tab_temp, tab_humid, tab_air, tab_forecast = st.tabs([
    "Summary", "Temperature", "Humidity", "Air Quality", " Predictive Lab"
])

# ══════════════════════════════════════════════════════════════════════════════
# OVERVIEW TAB
# ══════════════════════════════════════════════════════════════════════════════
with tab_overview:
    # Adding the Lottie Animation Polish!
    col_lottie, col_desc = st.columns([1, 4])
    with col_lottie:
        lottie_url = "https://assets3.lottiefiles.com/packages/lf20_1mzzZk.json" # Clean Data/IoT Animation
        lottie_json = load_lottieurl(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, height=120, key="iot_lottie")
    with col_desc:
        st.markdown('<div class="tab-desc" style="margin-top:20px;">A live, high-level snapshot of current sensor readings from the edge device. The system automatically fetches metrics from MongoDB Atlas and calculates their current severity status based on global thresholds.</div>', unsafe_allow_html=True)
    
    if df_h.empty:
        st.warning("⏳ No data found in the MongoDB Database yet. Ensure your ESP32 and mqtt_to_mongo.py script are running.")
    
    st.markdown('<div class="sh">Current Environmental Status</div>', unsafe_allow_html=True)
    kpi_cards()

    st.markdown('<div class="sh" style="margin-top: 40px;">System Health & Network Topology</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:var(--bg1); border:1px solid var(--border); border-radius:16px; overflow:hidden; backdrop-filter:blur(10px);">
    <table style="width:100%; border-collapse:collapse; font-size:14px;">
        <tr style="border-bottom:1px solid var(--border); color:#a1a1aa; text-align:left; background:rgba(0,0,0,0.2);">
            <th style="padding:16px; font-weight:500;">Device ID</th><th style="padding:16px; font-weight:500;">Location</th><th style="padding:16px; font-weight:500;">Status</th><th style="padding:16px; font-weight:500;">Last Seen</th>
        </tr>
        <tr style="border-bottom:1px solid var(--border); transition: background 0.2s;">
            <td style="padding:16px; color:#e4e4e7;">ENS160_Room402</td><td style="padding:16px; color:#a1a1aa;">Main Lab</td><td style="padding:16px;"><span style="color:#00f0ff; font-weight:600; text-shadow:0 0 10px rgba(0,240,255,0.4);">● Online</span></td><td style="padding:16px; font-family:'JetBrains Mono', monospace; font-size:12px; color:#a1a1aa;">Live via API</td>
        </tr>
        <tr>
            <td style="padding:16px; color:#e4e4e7;">DHT22_Room402</td><td style="padding:16px; color:#a1a1aa;">Main Lab</td><td style="padding:16px;"><span style="color:#00f0ff; font-weight:600; text-shadow:0 0 10px rgba(0,240,255,0.4);">● Online</span></td><td style="padding:16px; font-family:'JetBrains Mono', monospace; font-size:12px; color:#a1a1aa;">Live via API</td>
        </tr>
    </table>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TEMPERATURE TAB
# ══════════════════════════════════════════════════════════════════════════════
with tab_temp:
    with st.expander("Adjust Temperature Thresholds"):
        c1, c2 = st.columns(2)
        st.session_state.tmp_w = c1.slider("Warning Level (°C)", 18, 40, st.session_state.tmp_w, 1)
        st.session_state.tmp_d = c2.slider("Danger Level (°C)", 20, 45, st.session_state.tmp_d, 1)

    render_status_banner(last_reading.get('temperature', 0), st.session_state.tmp_w, st.session_state.tmp_d, "°C", "Temperature")
    plot_forecast_chart("temperature", "#00f0ff", "Temperature", "°C", st.session_state.tmp_w, st.session_state.tmp_d)

# ══════════════════════════════════════════════════════════════════════════════
# HUMIDITY TAB
# ══════════════════════════════════════════════════════════════════════════════
with tab_humid:
    with st.expander("Adjust Humidity Thresholds"):
        c1, c2 = st.columns(2)
        st.session_state.hum_w = c1.slider("Warning Level (%)", 30, 85, st.session_state.hum_w, 5)
        st.session_state.hum_d = c2.slider("Danger Level (%)", 40, 95, st.session_state.hum_d, 5)

    render_status_banner(last_reading.get('humidity', 0), st.session_state.hum_w, st.session_state.hum_d, "%", "Humidity")
    plot_forecast_chart("humidity", "#8b5cf6", "Humidity", "%", st.session_state.hum_w, st.session_state.hum_d)
    
# ══════════════════════════════════════════════════════════════════════════════
# AIR QUALITY TAB (CO2)
# ══════════════════════════════════════════════════════════════════════════════
with tab_air:
    with st.expander("Adjust CO₂ Thresholds"):
        c1, c2 = st.columns(2)
        st.session_state.co2_w = c1.slider("Warning Level (ppm)", 400, 1500, st.session_state.co2_w, 50)
        st.session_state.co2_d = c2.slider("Danger Level (ppm)", 500, 2000, st.session_state.co2_d, 50)

    current_co2 = last_reading.get('co2', 0)
    render_status_banner(current_co2, st.session_state.co2_w, st.session_state.co2_d, "ppm", "CO₂")
    
    if current_co2 >= st.session_state.co2_d:
        st.markdown('<div style="padding:15px; background:rgba(244, 63, 94, 0.15); border:1px solid #fb7185; color:#fb7185; border-radius:8px; margin-bottom:15px;"><b>🚨 HAZARD: Cognitive decline active. Vacate or ventilate immediately.</b></div>', unsafe_allow_html=True)
    elif current_co2 >= st.session_state.co2_w:
        st.markdown('<div style="padding:15px; background:rgba(245, 158, 11, 0.15); border:1px solid #fcd34d; color:#fcd34d; border-radius:8px; margin-bottom:15px;"><b>⚠️ Action Recommended: Open Windows for 10 Minutes.</b></div>', unsafe_allow_html=True)
           
    plot_forecast_chart("co2", "#f59e0b", "CO₂", "ppm", st.session_state.co2_w, st.session_state.co2_d)


# ══════════════════════════════════════════════════════════════════════════════
# PREDICTIVE LAB TAB
# ══════════════════════════════════════════════════════════════════════════════
with tab_forecast:
    st.info("**Tip:** This tab provides a holistic overlay of all predicted parameters to identify correlations.")
    
    fore_param = st.multiselect("Select parameters to overlay:", ["temperature", "humidity", "co2"], default=["temperature", "humidity"])
    
    if fore_param:
        fig_multi = go.Figure()
        dfs = df_f.sort_values("timestamp") if not df_f.empty else pd.DataFrame()
        dh_s = df_h.sort_values("timestamp") if not df_h.empty else pd.DataFrame()
        
        for p in fore_param:
            color = PARAMS[p]["color"]
            if not dh_s.empty:
                fig_multi.add_trace(go.Scatter(x=dh_s["timestamp"], y=dh_s[p].rolling(4,min_periods=1).mean(), name=f"{p.title()} (Hist)", line=dict(color=color,width=2)))
            if not dfs.empty:
                fig_multi.add_trace(go.Scatter(x=dfs["timestamp"], y=dfs[p], name=f"{p.title()} (Fore)", line=dict(color=color,width=2,dash="dot")))
        
        fig_multi.update_layout(height=450, **PL())
        st.plotly_chart(fig_multi, use_container_width=True, config={"displayModeBar": False})
        
        if not df_h.empty:
            csv_data = df_h.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Real Historical Data to CSV", data=csv_data, file_name="live_clima_data.csv", mime="text/csv")