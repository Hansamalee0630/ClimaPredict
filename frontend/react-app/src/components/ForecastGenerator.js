// // Lightweight forecast generator ported from the Streamlit JS side
// export function genForecast(history, daysAhead=14){
//   if(!history || history.length < 10) return [];

//   // Parse timestamps and bucket by hour
//   const parsed = history.map(r => {
//     let t = r?.dht22?.temperature ?? r?.temperature;
//     let h = r?.dht22?.humidity ?? r?.humidity;
//     let p = r?.bmp280?.pressure_hpa ?? r?.pressure;
//     let c = r?.ens160?.eco2 ?? r?.eco2 ?? r?.co2;
//     return {
//       ts: new Date(r.server_timestamp),
//       temperature: t != null && !isNaN(Number(t)) ? Number(t) : NaN,
//       humidity: h != null && !isNaN(Number(h)) ? Number(h) : NaN,
//       pressure: p != null && !isNaN(Number(p)) ? Number(p) : NaN,
//       co2: c != null && !isNaN(Number(c)) ? Number(c) : NaN
//     };
//   }).filter(r=>!isNaN(r.ts.getTime()));

//   const hours = {}; // hour -> arrays per metric
//   parsed.forEach(p=>{
//     const h = p.ts.getHours();
//     if(!hours[h]) hours[h] = {temperature:[], humidity:[], pressure:[], co2:[]};
//     if(isFinite(p.temperature)) hours[h].temperature.push(p.temperature);
//     if(isFinite(p.humidity)) hours[h].humidity.push(p.humidity);
//     if(isFinite(p.pressure)) hours[h].pressure.push(p.pressure);
//     if(isFinite(p.co2)) hours[h].co2.push(p.co2);
//   });

//   const median = (arr)=>{ if(!arr||arr.length===0) return null; const s = arr.slice().sort((a,b)=>a-b); const m=Math.floor(s.length/2); return s.length%2? s[m] : (s[m-1]+s[m])/2 }
//   const std = (arr)=>{ if(!arr||arr.length===0) return 0; const mu = arr.reduce((a,b)=>a+b,0)/arr.length; return Math.sqrt(arr.reduce((s,x)=>s+(x-mu)*(x-mu),0)/arr.length) }

//   const hourly = {};
//   for(let h=0; h<24; h++){
//     const bucket = hours[h] || {temperature:[],humidity:[],pressure:[],co2:[]};
//     hourly[h] = {
//       temperature_m: median(bucket.temperature), temperature_s: std(bucket.temperature),
//       humidity_m: median(bucket.humidity), humidity_s: std(bucket.humidity),
//       pressure_m: median(bucket.pressure), pressure_s: std(bucket.pressure),
//       co2_m: median(bucket.co2), co2_s: std(bucket.co2)
//     };
//   }

//   // Generate rows for future periods (15-minute steps)
//   const rows = [];
//   const now = new Date();
//   const start = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 0, 0, 0, 0);
//   const steps = daysAhead * 24 * 4;
//   for(let i=0;i<steps;i++){
//     const ts = new Date(start.getTime() + i * 15 * 60 * 1000);
//     const h = ts.getHours();
//     const info = hourly[h];
//     const makeVal = (m,s)=> (m===null? null : parseFloat((m).toFixed(2)) );
//     rows.push({
//       timestamp: ts.toISOString(),
//       temperature: makeVal(info.temperature_m), temperature_lo: makeVal(info.temperature_m - 1.5*info.temperature_s), temperature_hi: makeVal(info.temperature_m + 1.5*info.temperature_s),
//       humidity: makeVal(info.humidity_m), humidity_lo: makeVal(info.humidity_m - 1.5*info.humidity_s), humidity_hi: makeVal(info.humidity_m + 1.5*info.humidity_s),
//       pressure: makeVal(info.pressure_m), pressure_lo: makeVal(info.pressure_m - 1.5*info.pressure_s), pressure_hi: makeVal(info.pressure_m + 1.5*info.pressure_s),
//       co2: makeVal(info.co2_m), co2_lo: makeVal(info.co2_m - 1.5*info.co2_s), co2_hi: makeVal(info.co2_m + 1.5*info.co2_s),
//     });
//   }
//   return rows;
// }


// Lightweight forecast generator ported from the Streamlit JS side
export function genForecast(history, daysAhead = 14) {
  if (!history || history.length < 10) return [];

  // Parse timestamps and bucket by hour
  const parsed = history.map(r => {
    let t = r?.dht22?.temperature ?? r?.temperature;
    let h = r?.dht22?.humidity ?? r?.humidity;
    let p = r?.bmp280?.pressure_hpa ?? r?.pressure;
    let c = r?.ens160?.eco2 ?? r?.eco2 ?? r?.co2;
    return {
      ts: new Date(r.server_timestamp),
      temperature: t != null && !isNaN(Number(t)) ? Number(t) : NaN,
      humidity: h != null && !isNaN(Number(h)) ? Number(h) : NaN,
      pressure: p != null && !isNaN(Number(p)) ? Number(p) : NaN,
      co2: c != null && !isNaN(Number(c)) ? Number(c) : NaN
    };
  }).filter(r => !isNaN(r.ts.getTime()));

  const hours = {}; // hour -> arrays per metric
  parsed.forEach(p => {
    const h = p.ts.getHours();
    if (!hours[h]) hours[h] = { temperature: [], humidity: [], pressure: [], co2: [] };
    if (isFinite(p.temperature)) hours[h].temperature.push(p.temperature);
    if (isFinite(p.humidity)) hours[h].humidity.push(p.humidity);
    if (isFinite(p.pressure)) hours[h].pressure.push(p.pressure);
    if (isFinite(p.co2)) hours[h].co2.push(p.co2);
  });

  const median = (arr) => { if (!arr || arr.length === 0) return null; const s = arr.slice().sort((a, b) => a - b); const m = Math.floor(s.length / 2); return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2 }
  const std = (arr) => { if (!arr || arr.length === 0) return 0; const mu = arr.reduce((a, b) => a + b, 0) / arr.length; return Math.sqrt(arr.reduce((s, x) => s + (x - mu) * (x - mu), 0) / arr.length) }

  const hourly = {};
  for (let h = 0; h < 24; h++) {
    const bucket = hours[h] || { temperature: [], humidity: [], pressure: [], co2: [] };
    hourly[h] = {
      temperature_m: median(bucket.temperature), temperature_s: std(bucket.temperature),
      humidity_m: median(bucket.humidity), humidity_s: std(bucket.humidity),
      pressure_m: median(bucket.pressure), pressure_s: std(bucket.pressure),
      co2_m: median(bucket.co2), co2_s: std(bucket.co2)
    };
  }

  // --- GAP FILLING (Forward Fill) ---
  let lastGood = {
    temperature_m: 25, temperature_s: 1,
    humidity_m: 50, humidity_s: 5,
    pressure_m: 1013, pressure_s: 2,
    co2_m: 600, co2_s: 50
  };

  for (let h = 0; h < 24; h++) {
    if (hourly[h].co2_m !== null) {
      lastGood = { ...hourly[h] };
      break;
    }
  }

  for (let h = 0; h < 24; h++) {
    if (hourly[h].co2_m === null) {
      hourly[h] = { ...lastGood };
    } else {
      lastGood = { ...hourly[h] };
    }
  }

  // --- NEW CODE: Generate rows for future periods (HOURLY STEPS) ---
  const rows = [];
  const now = new Date();

  // Start the forecast at the top of the next hour
  const start = new Date(now.getFullYear(), now.getMonth(), now.getDate(), now.getHours() + 1, 0, 0, 0);

  // 1 point per hour, 24 points per day
  const steps = daysAhead * 24;

  for (let i = 0; i < steps; i++) {
    // Step forward by 60 minutes instead of 15
    const ts = new Date(start.getTime() + i * 60 * 60 * 1000);
    const h = ts.getHours();
    const info = hourly[h];

    const makeVal = (m) => parseFloat((m).toFixed(2));

    rows.push({
      timestamp: ts.toISOString(),
      temperature: makeVal(info.temperature_m), temperature_lo: makeVal(info.temperature_m - 1.5 * info.temperature_s), temperature_hi: makeVal(info.temperature_m + 1.5 * info.temperature_s),
      humidity: makeVal(info.humidity_m), humidity_lo: makeVal(info.humidity_m - 1.5 * info.humidity_s), humidity_hi: makeVal(info.humidity_m + 1.5 * info.humidity_s),
      pressure: makeVal(info.pressure_m), pressure_lo: makeVal(info.pressure_m - 1.5 * info.pressure_s), pressure_hi: makeVal(info.pressure_m + 1.5 * info.pressure_s),
      co2: makeVal(info.co2_m), co2_lo: makeVal(info.co2_m - 1.5 * info.co2_s), co2_hi: makeVal(info.co2_m + 1.5 * info.co2_s),
    });
  }
  return rows;
}