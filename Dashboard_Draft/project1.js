// Initialize Icons
lucide.createIcons();

// ─── ISO Week Number ──────────────────────────────────────────────────────────
function getISOWeek(d) {
    const date = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    date.setUTCDate(date.getUTCDate() + 4 - (date.getUTCDay() || 7));
    const yearStart = new Date(Date.UTC(date.getUTCFullYear(), 0, 1));
    return Math.ceil((((date - yearStart) / 86400000) + 1) / 7);
}

// ─── Seeded pseudo-random (must match script.js) ──────────────────────────────
function pseudoRandom(seed) {
    let x = Math.sin(seed) * 10000;
    return x - Math.floor(x);
}

// ─── Generate project data (mirrors script.js exactly) ───────────────────────
function generateProjectData() {
    const startDate = new Date(2026, 0, 15);
    const currentDate = new Date();
    const yieldCurve = [0.016, 0.018, 0.026, 0.030, 0.033, 0.035, 0.035, 0.034, 0.032, 0.028, 0.022, 0.017];

    let labels = [], wasteData = [], biogasData = [];
    let totalWaste = 0, totalBiogas = 0;
    let dateCursor = new Date(startDate);
    let weekIndex = 0;

    while (dateCursor <= currentDate) {
        const month = dateCursor.getMonth();
        const shortMonth = new Intl.DateTimeFormat('en-US', { month: 'short' }).format(dateCursor);
        labels.push(`W${getISOWeek(dateCursor)} ${shortMonth}`);

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
        labels, wasteData, biogasData,
        totalWaste, totalBiogas: Math.round(totalBiogas),
        totalCO2e: Math.round(totalWaste * 0.73),
        totalSmokeFree: weekIndex * 21,
        totalBioslurry: Math.round(totalWaste * 0.85),
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
        const ease = 1 - Math.pow(1 - Math.min((now - startTime) / duration, 1), 3);
        el.textContent = Math.round(target * ease).toLocaleString();
        if (ease < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
}

// ─── Chart Defaults ───────────────────────────────────────────────────────────
Chart.defaults.color = '#94a3b8';
Chart.defaults.font.family = "'Outfit', sans-serif";
Chart.defaults.scale.grid.color = 'rgba(255, 255, 255, 0.05)';

let charts = {};

// ─── Radial Gauge (SVG half-circle) ─────────────────────────────────────────
// Renders an animated half-circle gauge showing % of annual GHGe target avoided.
function renderGauge(trackId, fillId, pctId, avoidedId, remainingId) {
    const ANNUAL_TARGET = 5260;
    const cx = 130, cy = 148, r = 105;

    // Compute net avoided from live data
    const BASELINE_WEEKLY = 438.1 / 4.33;
    let bBase = 0, bBioVil = 0;
    pData.wasteData.forEach((_, i) => {
        bBase   += BASELINE_WEEKLY;
        bBioVil += pData.biogasData[i] * 1.2;
    });
    const netAvoided = Math.round(bBase - bBioVil);
    const pct = Math.min(netAvoided / ANNUAL_TARGET, 1);
    const remaining = Math.max(0, ANNUAL_TARGET - netAvoided);

    function polarToXY(angle) {
        return [cx + r * Math.cos(angle), cy + r * Math.sin(angle)];
    }
    function arcD(from, to) {
        const [x1, y1] = polarToXY(from);
        const [x2, y2] = polarToXY(to);
        const large = (to - from) > Math.PI ? 1 : 0;
        return `M ${x1} ${y1} A ${r} ${r} 0 ${large} 1 ${x2} ${y2}`;
    }

    const trackEl = document.getElementById(trackId);
    const fillEl  = document.getElementById(fillId);
    const pctEl   = document.getElementById(pctId);

    if (!trackEl || !fillEl || !pctEl) return;

    const fullArc  = arcD(-Math.PI, 0);
    trackEl.setAttribute('d', fullArc);
    fillEl.setAttribute('d', fullArc); // same path; we clip via dasharray

    // Total arc length for a semicircle
    const arcLen = Math.PI * r;
    fillEl.setAttribute('stroke-dasharray', `0 ${arcLen}`);
    fillEl.setAttribute('stroke-dashoffset', '0');

    // Animate
    setTimeout(() => {
        fillEl.style.transition = 'stroke-dasharray 1.6s cubic-bezier(0.4,0,0.2,1)';
        fillEl.setAttribute('stroke-dasharray', `${pct * arcLen} ${arcLen}`);
        // Animate % text
        const start = performance.now();
        function tick(now) {
            const ease = 1 - Math.pow(1 - Math.min((now - start) / 1600, 1), 3);
            pctEl.textContent = Math.round(ease * pct * 100) + '%';
            if (ease < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
    }, 120);

    if (avoidedId) {
        const el = document.getElementById(avoidedId);
        if (el) el.textContent = netAvoided.toLocaleString() + ' kg CO₂e';
    }
    if (remainingId) {
        const el = document.getElementById(remainingId);
        if (el) el.textContent = remaining.toLocaleString() + ' kg CO₂e';
    }
}

// ─── Avoided Emissions Doughnut ────────────────────────────────────────────────
function createSourceDoughnut(canvasId, storeKey, legendId) {
    const ctx = document.getElementById(canvasId)?.getContext('2d');
    if (!ctx) return;
    if (charts[storeKey]) charts[storeKey].destroy();

    // Cumulative values scaled to time elapsed
    const months = Math.max(0.5, (new Date() - new Date(2026, 0, 15)) / (1000 * 60 * 60 * 24 * 30.44));
    const methane  = Math.round(218 * months);
    const firewood = Math.round(220.1 * months);
    const data   = [methane, firewood];
    const labels = ['Avoided Methane (Waste)', 'Avoided CO₂ (Firewood)'];
    const colors = ['#fbbf24', '#38bdf8'];

    charts[storeKey] = new Chart(ctx, {
        type: 'doughnut',
        data: { labels, datasets: [{ data, backgroundColor: colors, borderWidth: 0, hoverOffset: 6 }] },
        options: {
            responsive: true, maintainAspectRatio: false, cutout: '74%',
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(10,14,18,0.95)', padding: 12, cornerRadius: 10,
                    borderColor: 'rgba(255,255,255,0.08)', borderWidth: 1,
                    callbacks: { label: ctx => ` ${ctx.label}: ${ctx.raw.toLocaleString()} kg CO₂e` }
                }
            }
        }
    });

    if (legendId) {
        const container = document.getElementById(legendId);
        if (container && container.innerHTML === '') {
            labels.forEach((label, i) => {
                const item = document.createElement('div');
                item.className = 'legend-item';
                item.innerHTML = `<div class="legend-label"><span class="legend-color" style="background:${colors[i]}"></span>${label}</div><div class="legend-value">${data[i].toLocaleString()} kg</div>`;
                container.appendChild(item);
            });
        }
    }
}

// ─── Budget Chart ─────────────────────────────────────────────────────────────
function initBudgetChart() {
    const ctx = document.getElementById('budgetChart')?.getContext('2d');
    if (!ctx) return;
    if (charts.budget) charts.budget.destroy();

    charts.budget = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Construction Materials', 'Infrastructure & IT', 'Professional Services', 'Transport & Ops', 'Software & Licenses'],
            datasets: [{
                data: [1559, 952, 303.35, 115, 70.65],
                backgroundColor: ['#10b981', '#3b82f6', '#fbbf24', '#f87171', '#a78bfa'],
                borderWidth: 0, hoverOffset: 6
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false, cutout: '70%',
            plugins: {
                legend: { position: 'right', labels: { usePointStyle: true, boxWidth: 8, color: '#94a3b8', font: { size: 11 }, padding: 12 } },
                tooltip: {
                    backgroundColor: 'rgba(10,14,18,0.95)', padding: 12, cornerRadius: 10,
                    borderColor: 'rgba(255,255,255,0.08)', borderWidth: 1,
                    callbacks: { label: ctx => ` ${ctx.label}: €${ctx.raw.toFixed(2)}` }
                }
            }
        }
    });
}

// ─── Init charts per tab ──────────────────────────────────────────────────────
function initChartsForTab(tabId) {
    if (tabId === 'tracker-tab') {
        renderGauge('tGaugeTrack', 'tGaugeFill', 'tGaugePct', 'tGaugeAvoided', 'tGaugeRemaining');
        createSourceDoughnut('trackerSourceChart', 'trackerDoughnut', 'trackerSourceLegend');
    } else if (tabId === 'environmental-tab') {
        renderGauge('eGaugeTrack', 'eGaugeFill', 'eGaugePct', 'eGaugeAvoided', 'eGaugeRemaining');
        createSourceDoughnut('sourceChart', 'envDoughnut', 'sourceLegend');
    } else if (tabId === 'social-tab') {
        initBudgetChart();
    }
}

// ─── Tab Navigation ───────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    // Wire live KPIs to pData (all tabs)
    animateCountUp(document.getElementById('kpi-co2'), pData.totalCO2e);
    animateCountUp(document.getElementById('kpi-bioslurry-proj'), pData.totalBioslurry);

    // Environmental tab KPIs (cumulative, not static monthly rates)
    animateCountUp(document.getElementById('env-total-offset'), pData.totalCO2e);
    const envBiogasTrend = document.getElementById('env-biogas-trend');
    if (envBiogasTrend) envBiogasTrend.textContent = `${pData.monthlyBiogasAvg} m³/month avg.`;

    const navItems = document.querySelectorAll('.nav-item[data-tab]');
    const tabContents = document.querySelectorAll('.tab-content');

    // Init default tab
    initChartsForTab('tracker-tab');

    // URL hash routing
    const hash = window.location.hash.replace('#', '');
    if (hash) {
        const target = document.querySelector(`.nav-item[data-tab="${hash}"]`);
        if (target) {
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            tabContents.forEach(t => t.classList.remove('active'));
            target.classList.add('active');
            const targetTab = document.getElementById(hash);
            if (targetTab) {
                targetTab.classList.add('active');
                setTimeout(() => initChartsForTab(hash), 50);
            }
        }
    }

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            tabContents.forEach(t => t.classList.remove('active'));
            item.classList.add('active');
            const targetId = item.getAttribute('data-tab');
            const targetTab = document.getElementById(targetId);
            if (targetTab) {
                targetTab.classList.add('active');
                setTimeout(() => initChartsForTab(targetId), 50);
            }
        });
    });

    // Sidebar toggle
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('sidebar-toggle');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('expanded');
            lucide.createIcons();
        });
    }

    // ─── Mobile Bottom Nav Tab Switching ──────────────────────────────────────────
    const mobTabs = document.querySelectorAll('.mob-tab[data-mob-tab]');
    mobTabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = tab.getAttribute('data-mob-tab');
            // Switch tab content
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            tabContents.forEach(t => t.classList.remove('active'));
            const targetTab = document.getElementById(targetId);
            if (targetTab) {
                targetTab.classList.add('active');
                setTimeout(() => initChartsForTab(targetId), 50);
            }
            // Update sidebar nav active state
            const matchingSidebarItem = document.querySelector(`.nav-item[data-tab="${targetId}"]`);
            if (matchingSidebarItem) matchingSidebarItem.classList.add('active');
            // Update bottom nav active state
            document.querySelectorAll('.mob-tab').forEach(m => m.classList.remove('active'));
            tab.classList.add('active');
            // Scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });
            // Re-initialize icons
            lucide.createIcons();
        });
    });

    // Set bottom nav active state from URL hash
    const mobileHash = window.location.hash.replace('#', '');
    if (mobileHash) {
        document.querySelectorAll('.mob-tab').forEach(m => m.classList.remove('active'));
        const matchingMobTab = document.querySelector(`.mob-tab[data-mob-tab="${mobileHash}"]`);
        if (matchingMobTab) matchingMobTab.classList.add('active');
    }

    // ─── Auto-Refresh (every 60 s) ────────────────────────────────────────────
    setInterval(() => {
        // Regenerate data (adds new weeks as real time passes)
        const d = generateProjectData();
        Object.assign(pData, d);

        // Update KPI text
        const set = (id, v) => { const el = document.getElementById(id); if (el) el.textContent = Math.round(v).toLocaleString(); };
        set('kpi-co2', d.totalCO2e);
        set('kpi-bioslurry-proj', d.totalBioslurry);
        set('env-total-offset', d.totalCO2e);

        const bt = document.getElementById('env-biogas-trend');
        if (bt) bt.textContent = `${d.monthlyBiogasAvg} m³/month avg.`;

        // Re-render gauge + doughnut on active tab
        const activeTab = document.querySelector('.tab-content.active');
        if (activeTab) initChartsForTab(activeTab.id);
    }, 60000);
});
