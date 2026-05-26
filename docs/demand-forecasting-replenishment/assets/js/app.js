/* global Plotly */
const DATA_PATH = 'assets/data/';
const CHART_THEME = {
  paper_bgcolor: '#ffffff',
  plot_bgcolor: '#f8fafc',
  font: { color: '#1d1d1f', family: '-apple-system, BlinkMacSystemFont, \"SF Pro Text\", Inter, system-ui, sans-serif' },
  hoverlabel: { bgcolor: '#111827', font: { color: '#ffffff' } }
};

let queueData = [];

function escapeHTML(value) {
  return String(value ?? '').replace(/[&<>"']/g, (char) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[char]));
}

function fmtNumber(value, digits = 1, suffix = '') {
  const num = Number(value);
  return Number.isFinite(num) ? `${num.toFixed(digits)}${suffix}` : 'N/A';
}

async function loadJSON(name) {
  const resp = await fetch(`${DATA_PATH}${name}`);
  if (!resp.ok) {
    if (resp.status === 404) return null;
    throw new Error(`Failed to load ${name}: ${resp.status}`);
  }
  return resp.json();
}

function ensurePlotly() {
  if (!window.Plotly) {
    throw new Error('Plotly library failed to load; check CDN access before reviewing dashboard charts.');
  }
}

function showEmptyState(msg) {
  const hero = document.querySelector('.hero');
  if (!hero) return;
  const existing = hero.querySelector('.empty-state');
  if (existing) existing.remove();
  const banner = document.createElement('div');
  banner.className = 'empty-state';
  banner.setAttribute('role', 'alert');
  banner.innerHTML = `<p><strong>Dashboard data not published yet.</strong><br>${msg || 'Run the export pipeline with local Favorita data to generate this dashboard.'}</p>`;
  hero.appendChild(banner);
}

function renderKPIs(kpis) {
  if (!kpis) return;
  const container = document.getElementById('kpi-container');
  container.innerHTML = '';
  const items = [
    { val: kpis.items_in_queue, label: 'Items in planner queue' },
    { val: kpis.avg_wape_pct != null ? `${kpis.avg_wape_pct}%` : 'N/A', label: 'Avg WAPE %' },
    { val: kpis.avg_bias_pct != null ? `${kpis.avg_bias_pct>=0?'+':''}${kpis.avg_bias_pct}%` : 'N/A', label: 'Avg Bias %' },
    { val: kpis.avg_forecast_score != null ? kpis.avg_forecast_score : 'N/A', label: 'Avg Forecast Score' },
    { val: kpis.top_exception_score != null ? kpis.top_exception_score : 'N/A', label: 'Top Exception Score' },
  ];
  items.forEach(item => {
    const card = document.createElement('article');
    card.className = 'kpi-card';
    card.innerHTML = `<strong>${escapeHTML(item.val)}</strong><span>${escapeHTML(item.label)}</span>`;
    container.appendChild(card);
  });
  const caveat = document.getElementById('kpi-caveat');
  if (caveat && kpis.planning_caveat) caveat.textContent = kpis.planning_caveat;
}

function renderChartEmptyState(el, msg) {
  if (!el) return;
  el.removeAttribute('role');
  el.removeAttribute('aria-label');
  el.innerHTML = `<div class="empty-state" role="status">${escapeHTML(msg)}</div>`;
}

function renderForecastAccuracy(accuracy) {
  const el = document.getElementById('accuracy-chart');
  if (!accuracy || !accuracy.rows || !accuracy.rows.length) {
    renderChartEmptyState(el, 'Forecast accuracy data is not published yet.');
    return;
  }
  const rows = accuracy.rows;
  const families = [...new Set(rows.map(r => r.family))].slice(0, 8);
  const traces = families.map(fam => {
    const subset = rows.filter(r => r.family === fam).sort((a, b) => a.wape_pct - b.wape_pct);
    return { x: subset.map(r => r.wape_pct), y: subset.map(r => r.forecast_score),
      mode: 'markers', type: 'scatter', name: fam,
      marker: { size: 8 },
      hovertemplate: `<b>${fam}</b><br>WAPE: %{x:.1f}%<br>Score: %{y}<extra></extra>` };
  });
  const layout = { title: 'Forecast Score vs WAPE % by Product Family',
    xaxis: { title: 'WAPE %' }, yaxis: { title: 'Forecast Score' },
    showlegend: true, legend: { orientation: 'h' },
    ...CHART_THEME };
  const config = { responsive: true, displayModeBar: false };
  Plotly.newPlot(el, traces, layout, config);
}

function renderPlannerQueue(queue) {
  const tbody = document.querySelector('#queue-table tbody');
  if (!queue || !queue.rows || !queue.rows.length) {
    if (tbody) {
      tbody.innerHTML = '<tr><td colspan="8"><div class="empty-state" role="status">No planner exceptions generated. Run the pipeline with real demand data.</div></td></tr>';
    }
    return;
  }
  queueData = queue.rows;
  tbody.innerHTML = '';
  const reasonClass = (rc) => {
    if (rc.includes('risk') || rc.includes('error')) return 'risk';
    if (rc.includes('bias')) return 'bias';
    return '';
  };
  queue.rows.slice(0, 25).forEach(row => {
    const tr = document.createElement('tr');
    const reasons = (row.reason_codes || []).map(rc => `<span class="reason-chip ${reasonClass(rc)}">${escapeHTML(rc)}</span>`).join('');
    const bias = Number(row.bias_pct);
    tr.innerHTML = `<td>${escapeHTML(row.store_nbr)} / ${escapeHTML(row.item_nbr)}</td>
      <td>${escapeHTML(row.family)}</td>
      <td>${fmtNumber(row.exception_score)}</td>
      <td>${fmtNumber(row.wape_pct, 1, '%')}</td>
      <td>${Number.isFinite(bias) ? `${bias >= 0 ? '+' : ''}${bias.toFixed(1)}%` : 'N/A'}</td>
      <td>${escapeHTML(row.abc_class)} / ${escapeHTML(row.xyz_class)}</td>
      <td>${reasons}</td>
      <td>${escapeHTML(row.recommended_action)}</td>`;
    tbody.appendChild(tr);
  });
}

function renderSegments(segments) {
  const el = document.getElementById('segments-chart');
  if (!segments || !segments.rows || !segments.rows.length) {
    renderChartEmptyState(el, 'ABC/XYZ segment data is not published yet.');
    return;
  }
  const rows = segments.rows;
  const x = rows.map(r => `${r.abc_class}-${r.xyz_class}`);
  const y = rows.map(r => r.items || 0);
  Plotly.newPlot(el, [{ x, y, type: 'bar', marker: { color: '#0071e3' } }],
    { title: 'Items per ABC-XYZ Segment', xaxis: { title: 'Segment' }, yaxis: { title: 'Item Count' },
      ...CHART_THEME }, { responsive: true, displayModeBar: false });
}

function renderAssumptions(assumptions) {
  const el = document.getElementById('assumptions-content');
  if (!assumptions) return;
  const items = [
    { label: 'Lead time (days)', val: assumptions.lead_time_days },
    { label: 'Service level', val: assumptions.service_level_assumption },
    { label: 'Review policy', val: assumptions.review_policy },
    { label: 'Inventory data limit', val: assumptions.inventory_limit },
    { label: 'Zero-demand handling', val: assumptions.zero_demand_handling },
  ];
  el.innerHTML = items.map(i => `<tr><td><strong>${escapeHTML(i.label)}</strong></td><td>${escapeHTML(i.val)}</td></tr>`).join('');
}

function renderMetadata(metadata) {
  const el = document.getElementById('metadata-content');
  if (!metadata) return;
  el.innerHTML = `<tr><td><strong>Dataset</strong></td><td>${escapeHTML(metadata.dataset || 'N/A')}</td></tr>
    <tr><td><strong>Generated</strong></td><td>${escapeHTML(metadata.generated_at_utc || 'N/A')}</td></tr>
    <tr><td><strong>Planner metrics</strong></td><td>${escapeHTML(metadata.row_counts?.planner_metrics ?? 'N/A')}</td></tr>
    <tr><td><strong>Planner queue size</strong></td><td>${escapeHTML(metadata.row_counts?.planner_queue ?? 'N/A')}</td></tr>
    <tr><td><strong>JSON total (bytes)</strong></td><td>${escapeHTML(metadata.json_total_bytes != null ? metadata.json_total_bytes.toLocaleString() : 'N/A')}</td></tr>
    <tr><td><strong>Max JSON file (bytes)</strong></td><td>${escapeHTML(metadata.json_max_file_bytes != null ? metadata.json_max_file_bytes.toLocaleString() : 'N/A')}</td></tr>
    <tr><td><strong>Caveat</strong></td><td>${escapeHTML(metadata.caveat || 'N/A')}</td></tr>`;
}

async function init() {
  let hasData = false;
  try {
    ensurePlotly();
    const [kpis, accuracy, queue, segments, assumptions, metadata] = await Promise.all([
      loadJSON('kpis.json'),
      loadJSON('forecast_accuracy.json'),
      loadJSON('planner_queue.json'),
      loadJSON('segments.json'),
      loadJSON('assumptions.json'),
      loadJSON('build_metadata.json'),
    ]);
    if (!kpis && !queue) {
      showEmptyState(null);
      return;
    }
    hasData = true;
    renderKPIs(kpis);
    renderForecastAccuracy(accuracy);
    renderPlannerQueue(queue);
    renderSegments(segments);
    renderAssumptions(assumptions);
    renderMetadata(metadata);
  } catch (err) {
    console.error('Dashboard init error:', err);
    showEmptyState(err.message);
    return;
  }
  if (!hasData) {
    showEmptyState(null);
  }
}

document.addEventListener('DOMContentLoaded', init);
