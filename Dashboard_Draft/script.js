// Initialize Icons
lucide.createIcons();

// Chart Defaults
Chart.defaults.color = '#94a3b8';
Chart.defaults.font.family = "'Outfit', sans-serif";
Chart.defaults.scale.grid.color = 'rgba(255, 255, 255, 0.05)';



// ─── Seasonal Shading Plugin (draws subtle bg on winter/summer weeks) ──────────
const seasonalShadingPlugin = {
    id: 'seasonalShading',
    beforeDatasetsDraw(chart) {
        const { ctx, chartArea, scales } = chart;
        if (!chartArea || !scales.x) return;
        const monthData = chart.config.options._monthData || [];
        ctx.save();
        monthData.forEach((month, i) => {
            let color = null;
            if ([11, 0, 1, 2].includes(month)) color = 'rgba(56, 189, 248, 0.07)';  // Winter
            else if ([5, 6, 7].includes(month)) color = 'rgba(251, 191, 36, 0.07)'; // Summer
            if (!color) return;
            // Chart.js 4: use getPixelForValue with the tick index
            const x0 = scales.x.getPixelForValue(i);
            const x1 = i < monthData.length - 1 ? scales.x.getPixelForValue(i + 1) : chartArea.right;
            ctx.fillStyle = color;
            ctx.fillRect(x0, chartArea.top, x1 - x0, chartArea.bottom - chartArea.top);
        });
        ctx.restore();
    }
};

// ─── ISO Week Number (W1–W52) ─────────────────────────────────────────────────
function getISOWeek(d) {
    const date = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    date.setUTCDate(date.getUTCDate() + 4 - (date.getUTCDay() || 7));
    const yearStart = new Date(Date.UTC(date.getUTCFullYear(), 0, 1));
    return Math.ceil((((date - yearStart) / 86400000) + 1) / 7);
}

// ─── Seeded pseudo-random ─────────────────────────────────────────────────────
function pseudoRandom(seed) {
    let x = Math.sin(seed) * 10000;
    return x - Math.floor(x);
}

// ─── Dynamic Data Generation ──────────────────────────────────────────────────
function generateProjectData() {
    const startDate = new Date(2026, 0, 15);
    const currentDate = new Date();
    const yieldCurve = [0.016, 0.018, 0.026, 0.030, 0.033, 0.035, 0.035, 0.034, 0.032, 0.028, 0.022, 0.017];

    let labels = [], wasteData = [], biogasData = [], monthData = [];
    let totalWaste = 0, totalBiogas = 0;
    let dateCursor = new Date(startDate);
    let weekIndex = 0;

    while (dateCursor <= currentDate) {
        const month = dateCursor.getMonth();
        const shortMonth = new Intl.DateTimeFormat('en-US', { month: 'short' }).format(dateCursor);
        labels.push(`W${getISOWeek(dateCursor)} ${shortMonth}`);
        monthData.push(month);

        const baseWaste = weekIndex === 0 ? 70 : 140;
        const weeklyWaste = Math.round(baseWaste * (1.0 + pseudoRandom(weekIndex * 123.45) * 0.3 - 0.15));
        const weeklyBiogas = Number((weeklyWaste * yieldCurve[month] * (1.0 + pseudoRandom(weekIndex * 678.9) * 0.1 - 0.05)).toFixed(1));

        wasteData.push(weeklyWaste);
        biogasData.push(weeklyBiogas);
        totalWaste += weeklyWaste;
        totalBiogas += weeklyBiogas;
        dateCursor.setDate(dateCursor.getDate() + 7);
        weekIndex++;
    }

    const elapsedMonths = Math.max(0.5, (new Date() - startDate) / (1000 * 60 * 60 * 24 * 30.44));
    const daysActive = Math.floor((new Date() - startDate) / (1000 * 60 * 60 * 24));

    return {
        labels, wasteData, biogasData, monthData,
        totalWaste, totalBiogas: Math.round(totalBiogas),
        totalCO2e: Math.round(totalWaste * 0.73),
        totalSmokeFree: weekIndex * 21,
        totalBioslurry: Math.round(totalWaste * 0.85), // ~85% of input becomes digestate
        monthlyBiogasAvg: Math.round(totalBiogas / elapsedMonths),
        elapsedMonths, daysActive, weekCount: weekIndex
    };
}

const pData = generateProjectData();

// ─── Count-Up Animation ───────────────────────────────────────────────────────
function animateCountUp(el, target, duration = 1400) {
    if (!el) return;
    const startTime = performance.now();
    function tick(now) {
        const progress = Math.min((now - startTime) / duration, 1);
        const ease = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.round(target * ease).toLocaleString();
        if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
}

animateCountUp(document.getElementById('kpi-co2'),      pData.totalCO2e);
animateCountUp(document.getElementById('kpi-waste'),    pData.totalWaste);
animateCountUp(document.getElementById('kpi-biogas'),   pData.totalBiogas);
animateCountUp(document.getElementById('kpi-smoke'),    pData.totalSmokeFree);
animateCountUp(document.getElementById('kpi-bioslurry'),pData.totalBioslurry);

// Hero banner stats
animateCountUp(document.getElementById('hs-days'),   pData.daysActive, 1000);
animateCountUp(document.getElementById('hs-weeks'),  pData.weekCount,  1000);
animateCountUp(document.getElementById('hs-biogas'), pData.totalBiogas);
animateCountUp(document.getElementById('hs-co2'),    pData.totalCO2e);

// Dynamic biogas avg
const biogasTrendEl = document.getElementById('kpi-biogas-trend');
if (biogasTrendEl) biogasTrendEl.textContent = `~${pData.monthlyBiogasAvg} m³/month avg.`;

// Days active counter
const daysActiveEl = document.getElementById('days-active');
if (daysActiveEl) animateCountUp(daysActiveEl, pData.daysActive, 1000);

// Date filter label
const dateLabel = document.getElementById('date-filter-label');
if (dateLabel) {
    const em = Math.round(pData.elapsedMonths);
    dateLabel.textContent = em <= 12 ? `All Time (Since Jan '26)` : `Last ${em} Months`;
}

// Live timestamp
const lastUpdatedEl = document.getElementById('last-updated');
if (lastUpdatedEl) {
    const now = new Date();
    lastUpdatedEl.textContent = `Live · Updated ${now.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' })} · W${getISOWeek(now)}`;
}

// 2026 target progress bar
const ANNUAL_TARGET = 5260;
const BASELINE_WEEKLY = 438.1 / 4.33;
let bBase = 0, bBioVil = 0;
pData.wasteData.forEach((_, i) => { bBase += BASELINE_WEEKLY; bBioVil += pData.biogasData[i] * 1.2; });
const netAvoided = Math.round(bBase - bBioVil);
const pct = Math.min(netAvoided / ANNUAL_TARGET, 1);
const tpPctEl  = document.getElementById('tp-pct');
const tpFillEl = document.getElementById('tp-fill');
if (tpPctEl)  tpPctEl.textContent = Math.round(pct * 100) + '%';
if (tpFillEl) setTimeout(() => { tpFillEl.style.width = (pct * 100) + '%'; }, 200);

// ─── Chart Export Helper ──────────────────────────────────────────────────────
function setupExportButton(btnId, chartRef, filename) {
    const btn = document.getElementById(btnId);
    if (!btn || !chartRef) return;
    btn.title = 'Download chart as PNG';
    btn.addEventListener('click', () => {
        const link = document.createElement('a');
        link.download = filename + '.png';
        link.href = chartRef.toBase64Image('image/png', 1.0);
        link.click();
    });
}

// ─── 1. Main Trend Chart — Biogas Output & Waste Input ───────────────────────
const trendCanvas = document.getElementById('trendChart');
let trendChart = null;
if (trendCanvas) {
    const ctxTrend = trendCanvas.getContext('2d');

    trendChart = new Chart(ctxTrend, {
        type: 'line',
        plugins: [seasonalShadingPlugin],
        data: {
            labels: pData.labels,
            datasets: [
                {
                    label: 'Weekly Waste Diverted (kg)',
                    data: pData.wasteData,
                    borderColor: '#38bdf8',
                    backgroundColor: 'rgba(56, 189, 248, 0.18)',
                    borderWidth: 2.5, tension: 0.4, fill: true, yAxisID: 'y1',
                    pointRadius: pData.labels.length > 20 ? 0 : 4,
                    pointHoverRadius: 6
                },
                {
                    label: 'Weekly Biogas (m³)',
                    data: pData.biogasData,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.18)',
                    borderWidth: 2.5, tension: 0.4, fill: true, yAxisID: 'y',
                    pointRadius: pData.labels.length > 20 ? 0 : 4,
                    pointHoverRadius: 6
                }
            ]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top', align: 'end', labels: { usePointStyle: true, boxWidth: 8, padding: 16 } },
                tooltip: {
                    backgroundColor: 'rgba(10,14,18,0.95)', padding: 14, cornerRadius: 10,
                    borderColor: 'rgba(255,255,255,0.08)', borderWidth: 1,
                    titleFont: { size: 13, weight: '600' }, bodyFont: { size: 12 },
                    callbacks: {
                        afterBody: (items) => {
                            const i = items[0].dataIndex;
                            return ['', `🌿 CO₂e Avoided: ${Math.round(pData.wasteData[i] * 0.73)} kg`,
                                        `🔥 Combustion CO₂: ${(pData.biogasData[i] * 1.2).toFixed(1)} kg`];
                        }
                    }
                }
            },
            scales: {
                x:  { grid: { display: false }, ticks: { maxRotation: 45, autoSkip: true, maxTicksLimit: 16, font: { size: 11 } } },
                y:  { type: 'linear', position: 'left',  beginAtZero: true, grid: { drawBorder: false },      title: { display: true, text: 'Biogas (m³)',  color: '#10b981', font: { size: 12 } } },
                y1: { type: 'linear', position: 'right', beginAtZero: true, grid: { drawOnChartArea: false }, title: { display: true, text: 'Waste (kg)', color: '#38bdf8', font: { size: 12 } } }
            },
            _monthData: pData.monthData,
            interaction: { mode: 'index', intersect: false }
        }
    });
    setupExportButton('trend-export-btn', trendChart, 'biovil-biogas-trend');
}

// ─── 2. Climate Impact Breakdown (replaces single-segment feedstock doughnut) ──
const ctxClimate = document.getElementById('climateImpactChart')?.getContext('2d');
if (ctxClimate) {
    const elapsedMonths = Math.max(0.5, (new Date() - new Date(2026, 0, 15)) / (1000 * 60 * 60 * 24 * 30.44));
    const monthlyBiogas = pData.totalBiogas / elapsedMonths;
    const combustionRate = Math.round(monthlyBiogas * 1.2);

    new Chart(ctxClimate, {
        type: 'bar',
        data: {
            labels: ['Avoided: Methane', 'Avoided: Firewood', 'Emitted: Combustion'],
            datasets: [{
                data: [218, 220.1, combustionRate || 24],
                backgroundColor: ['rgba(52,211,153,0.85)', 'rgba(56,189,248,0.85)', 'rgba(251,191,36,0.85)'],
                borderColor: ['#34d399', '#38bdf8', '#fbbf24'],
                borderWidth: 1.5, borderRadius: 6
            }]
        },
        options: {
            indexAxis: 'y', responsive: true, maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(10,14,18,0.95)', padding: 14, cornerRadius: 10,
                    borderColor: 'rgba(255,255,255,0.08)', borderWidth: 1,
                    callbacks: {
                        label: (ctx) => ctx.dataIndex === 2
                            ? ` ${ctx.raw} kg CO₂/mo (biogenic — from burning biogas)`
                            : ` ${ctx.raw} kg GHGe/mo avoided`
                    }
                }
            },
            scales: {
                x: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, title: { display: true, text: 'kg GHGe per month', font: { size: 12 } } },
                y: { grid: { display: false }, ticks: { font: { size: 12 } } }
            }
        }
    });

    const netEl = document.getElementById('climate-net-impact');
    if (netEl) {
        const net = 218 + 220.1 - (combustionRate || 24);
        netEl.textContent = `Net GHGe Avoided: ${Math.round(net)} kg/month`;
    }
}

// ─── Sidebar Toggle ───────────────────────────────────────────────────────────
const sidebar = document.getElementById('sidebar');
const toggleBtn = document.getElementById('sidebar-toggle');
if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('expanded');
        lucide.createIcons();
    });
}

// ─── Auto-Refresh (every 60 s) ────────────────────────────────────────────────
// Re-generate data (picks up new weeks as time passes), update KPIs + charts.
setInterval(() => {
    const d = generateProjectData();

    // KPI numbers
    const set = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = Math.round(val).toLocaleString(); };
    set('kpi-co2',       d.totalCO2e);
    set('kpi-waste',     d.totalWaste);
    set('kpi-biogas',    d.totalBiogas);
    set('kpi-smoke',     d.totalSmokeFree);
    set('kpi-bioslurry', d.totalBioslurry);
    set('days-active',   d.daysActive);

    const bt = document.getElementById('kpi-biogas-trend');
    if (bt) bt.textContent = `~${d.monthlyBiogasAvg} m³/month avg.`;

    // Trend chart
    if (trendChart) {
        trendChart.data.labels = d.labels;
        trendChart.data.datasets[0].data = d.wasteData;
        trendChart.data.datasets[1].data = d.biogasData;
        trendChart.options._monthData = d.monthData;
        trendChart.update('none');
    }

    // Climate bar chart — recalculate combustion
    const climateCanvas = document.getElementById('climateImpactChart');
    if (climateCanvas) {
        const em = Math.max(0.5, (new Date() - new Date(2026, 0, 15)) / (1000 * 60 * 60 * 24 * 30.44));
        const cr = Math.round((d.totalBiogas / em) * 1.2);
        const ci = Chart.getChart(climateCanvas);
        if (ci) {
            ci.data.datasets[0].data = [218, 220.1, cr || 24];
            ci.update('none');
        }
        const netEl = document.getElementById('climate-net-impact');
        if (netEl) netEl.textContent = `Net GHGe Avoided: ${Math.round(218 + 220.1 - (cr || 24))} kg/month`;
    }

    // Target progress bar
    const BW = 438.1 / 4.33;
    let bb = 0, bv = 0;
    d.wasteData.forEach((_, i) => { bb += BW; bv += d.biogasData[i] * 1.2; });
    const na = Math.round(bb - bv);
    const p = Math.min(na / 5260, 1);
    const pe = document.getElementById('tp-pct');
    const fe = document.getElementById('tp-fill');
    if (pe) pe.textContent = Math.round(p * 100) + '%';
    if (fe) fe.style.width = (p * 100) + '%';

    // Timestamp
    const ts = document.getElementById('last-updated');
    if (ts) {
        const now = new Date();
        ts.textContent = `Live · Updated ${now.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' })} · W${getISOWeek(now)}`;
    }
}, 60000);

