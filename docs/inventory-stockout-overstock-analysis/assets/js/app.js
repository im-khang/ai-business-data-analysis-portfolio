const DATA_PATH = './assets/data/';
const chartTheme = {
  paper_bgcolor: "#ffffff",
  plot_bgcolor: "#f8fafc",
  font: { color: "#1d1d1f", family: "-apple-system, BlinkMacSystemFont, 'SF Pro Text', Inter, system-ui, sans-serif" },
  hoverlabel: { bgcolor: "#111827", font: { color: "#ffffff" } }
};
const chartConfig = {responsive: true, displaylogo: false};

async function loadJson(name) {
  const response = await fetch(`${DATA_PATH}${name}`);
  if (!response.ok) throw new Error(`Failed to load ${name}: ${response.status}`);
  return response.json();
}

function number(value) { return Number(value).toLocaleString(); }
function pct(value) { return `${Number(value).toFixed(2)}%`; }

function renderCards(kpis) {
  const cards = [
    ['Delivered orders', number(kpis.delivered_orders), 'Evidence base for SLA sizing'],
    ['Late delivered orders', number(kpis.late_orders), 'Primary exposure volume'],
    ['Late delivery rate', pct(kpis.late_delivery_rate_pct), 'Portfolio KPI for SLA risk'],
    ['Avg delivery days', Number(kpis.avg_delivery_days).toFixed(2), 'Baseline customer wait'],
    ['Avg days late among late orders', Number(kpis.avg_days_late_late_orders).toFixed(2), 'Severity among missed promises'],
  ];
  document.getElementById('kpi-cards').innerHTML = cards.map(([label, value, note]) => `<article class="card"><span>${label}</span><strong>${value}</strong><em>${note}</em></article>`).join('');
}

function layout(title, extra = {}) {
  return {title, ...chartTheme, margin: {t: 48, r: 24, b: 90, l: 60}, ...extra};
}

function ensurePlotly() {
  if (!window.Plotly) throw new Error('Plotly library failed to load; check CDN access before reviewing dashboard charts.');
}

function renderDelayBands(rows) {
  Plotly.newPlot('delay-bands', [{type: 'bar', x: rows.map(r => r.delay_band), y: rows.map(r => r.orders), marker: {color: '#38bdf8'}, hovertemplate: '%{x}<br>Orders: %{y:,}<extra></extra>'}], layout('Orders by delivery delay band'), chartConfig);
}

function renderReviewImpact(rows) {
  Plotly.newPlot('review-impact', [{type: 'bar', x: rows.map(r => r.delay_band), y: rows.map(r => r.avg_review_score), marker: {color: rows.map(r => r.late_delivery_flag ? '#f59e0b' : '#22c55e')}, hovertemplate: '%{x}<br>Avg review: %{y:.2f}<extra></extra>'}], layout('Average review score by delay band', {yaxis: {range: [0,5]}}), chartConfig);
}

function renderMonthly(rows) {
  Plotly.newPlot('monthly-trend', [{type: 'scatter', mode: 'lines+markers', x: rows.map(r => r.purchase_month), y: rows.map(r => r.late_rate_pct), line: {color: '#ef4444'}, hovertemplate: '%{x}<br>Late rate: %{y:.2f}%<extra></extra>'}], layout('Monthly late-delivery rate'), chartConfig);
}

function renderRiskSegments(rows) {
  const labels = rows.map(r => `${r.seller_state || 'NA'} → ${r.customer_state || 'NA'} · ${r.category || 'Unknown'}`);
  Plotly.newPlot('risk-segments', [{type: 'bar', orientation: 'h', x: rows.map(r => r.late_orders), y: labels, marker: {color: rows.map(r => r.late_rate_pct), colorscale: 'YlOrRd'}, text: rows.map(r => `${r.late_rate_pct}% late`), hovertemplate: '%{y}<br>Late orders: %{x:,}<br>%{text}<br>Investigation candidate, not proven cause<extra></extra>'}], layout('Top investigation candidates by late orders', {margin: {t: 48, r: 24, b: 60, l: 260}, yaxis: {automargin: true}}), chartConfig);
}

async function main() {
  try {
    ensurePlotly();
    const [kpis, delayBands, reviewImpact, riskSegments, monthlyTrend, metadata] = await Promise.all(['kpis.json','delay_bands.json','review_impact.json','risk_segments.json','monthly_sla_trend.json','build_metadata.json'].map(loadJson));
    renderCards(kpis); renderDelayBands(delayBands); renderReviewImpact(reviewImpact); renderMonthly(monthlyTrend); renderRiskSegments(riskSegments);
    document.getElementById('build-note').textContent = `${metadata.privacy_note} Generated: ${metadata.generated_at_utc}.`;
  } catch (error) {
    const box = document.getElementById('error');
    box.hidden = false;
    box.textContent = `Dashboard data-load error: ${error.message}`;
  }
}

main();
