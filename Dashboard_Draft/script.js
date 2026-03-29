// Initialize Icons
lucide.createIcons();

// Chart Defaults for consistent premium look
Chart.defaults.color = '#94a3b8';
Chart.defaults.font.family = "'Outfit', sans-serif";
Chart.defaults.scale.grid.color = 'rgba(255, 255, 255, 0.05)';

const gradientPrimary = (ctx) => {
    const canvas = ctx.chart.canvas;
    const chartCtx = canvas.getContext('2d');
    const gradient = chartCtx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(16, 185, 129, 0.5)');
    gradient.addColorStop(1, 'rgba(16, 185, 129, 0.0)');
    return gradient;
};

const gradientSecondary = (ctx) => {
    const canvas = ctx.chart.canvas;
    const chartCtx = canvas.getContext('2d');
    const gradient = chartCtx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(56, 189, 248, 0.5)');
    gradient.addColorStop(1, 'rgba(56, 189, 248, 0.0)');
    return gradient;
};

// --- DYNAMIC DATA GENERATION: ASSAM CLIMATE & TIME PROGRESSION ---
function pseudoRandom(seed) {
    let x = Math.sin(seed) * 10000;
    return x - Math.floor(x);
}

function generateProjectData() {
    const startDate = new Date(2026, 0, 15); // Jan 15, 2026
    const currentDate = new Date(); // Current real-time date
    
    // Assam monthly biogas yield multiplier (m³ per kg of waste)
    // Jan/Feb cold (0.016), peaks in Summer July/Aug (0.035)
    const yieldCurve = [0.016, 0.018, 0.026, 0.030, 0.033, 0.035, 0.035, 0.034, 0.032, 0.028, 0.022, 0.017];
    
    let labels = [];
    let wasteData = [];
    let biogasData = [];
    
    let totalWaste = 0;
    let totalBiogas = 0;
    
    // Generate week-by-week
    let dateCursor = new Date(startDate);
    let weekIndex = 0;
    while (dateCursor <= currentDate) {
        let month = dateCursor.getMonth();
        let weekLabel = 'W' + Math.ceil(dateCursor.getDate() / 7) + ' ' + (new Intl.DateTimeFormat('en-US', {month: 'short'}).format(dateCursor));
        labels.push(weekLabel);
        
        // Random fluctuation +/- 15% to weekly waste (140kg base)
        let baseWaste = (weekIndex === 0) ? 70 : 140; // first week partial
        let fluctuation = 1.0 + (pseudoRandom(weekIndex * 123.45) * 0.3 - 0.15); 
        let weeklyWaste = Math.round(baseWaste * fluctuation);
        
        // Biogas yield depends on month temperature + tiny random noise
        let baseYield = yieldCurve[month];
        let yieldFluctuation = 1.0 + (pseudoRandom(weekIndex * 678.9) * 0.1 - 0.05); 
        let weeklyBiogas = Number((weeklyWaste * baseYield * yieldFluctuation).toFixed(1));
        
        wasteData.push(weeklyWaste);
        biogasData.push(weeklyBiogas);
        totalWaste += weeklyWaste;
        totalBiogas += weeklyBiogas;
        
        // Advance 7 days
        dateCursor.setDate(dateCursor.getDate() + 7);
        weekIndex++;
    }
    
    // 600kg waste = 218kg CO2. Wood displaces 220.1kg CO2. Overall multiplier ~0.73 per kg waste processed.
    let totalCO2e = Math.round(totalWaste * 0.73);
    let totalSmokeFree = weekIndex * 21; // ~21 hours saved per week
    
    return { labels, wasteData, biogasData, totalWaste, totalBiogas: Math.round(totalBiogas), totalCO2e, totalSmokeFree };
}

const pData = generateProjectData();

// Update DOM KPIs automatically
document.getElementById('kpi-co2').textContent = pData.totalCO2e.toLocaleString();
document.getElementById('kpi-waste').textContent = pData.totalWaste.toLocaleString();
document.getElementById('kpi-biogas').textContent = pData.totalBiogas.toLocaleString();
document.getElementById('kpi-smoke').textContent = pData.totalSmokeFree.toLocaleString();

// Update date filter label dynamically based on elapsed time
const dateLabel = document.getElementById('date-filter-label');
if (dateLabel) {
    const elapsedMonths = Math.round((new Date() - new Date(2026, 0, 15)) / (1000 * 60 * 60 * 24 * 30));
    if (elapsedMonths <= 12) {
        dateLabel.textContent = `All Time (Since Jan '26)`;
    } else {
        dateLabel.textContent = `Last ${elapsedMonths} Months`;
    }
}

// 1. Main Trend Chart — Dynamic Weekly Production Rates
const ctxTrend = document.getElementById('trendChart').getContext('2d');
new Chart(ctxTrend, {
    type: 'line',
    data: {
        labels: pData.labels,
        datasets: [
            {
                label: 'Weekly Waste Diverted (kg)',
                data: pData.wasteData,
                borderColor: '#38bdf8',
                backgroundColor: gradientSecondary,
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                yAxisID: 'y1'
            },
            {
                label: 'Weekly Biogas (m³)',
                data: pData.biogasData,
                borderColor: '#10b981',
                backgroundColor: gradientPrimary,
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                yAxisID: 'y'
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
                align: 'end',
                labels: { usePointStyle: true, boxWidth: 8 }
            },
            tooltip: {
                backgroundColor: 'rgba(18, 25, 33, 0.9)',
                titleFont: { size: 14 },
                bodyFont: { size: 13 },
                padding: 12,
                cornerRadius: 8,
                displayColors: true
            }
        },
        scales: {
            x: {
                grid: { display: false }
            },
            y: {
                type: 'linear',
                display: true,
                position: 'left',
                grid: { drawBorder: false },
                title: { display: true, text: 'Biogas (m³)', color: '#10b981' }
            },
            y1: {
                type: 'linear',
                display: true,
                position: 'right',
                grid: { drawOnChartArea: false },
                title: { display: true, text: 'Waste (kg)', color: '#38bdf8' }
            }
        },
        interaction: {
            mode: 'index',
            intersect: false,
        }
    }
});

// 2. Feedstock Composition — Real data: 100% Animal Manure from Project 1
const ctxComposition = document.getElementById('compositionChart').getContext('2d');
const compositionData = [100];
const compositionLabels = ['Animal Manure (Cow Dung)'];
const compositionColors = ['#fbbf24'];

new Chart(ctxComposition, {
    type: 'doughnut',
    data: {
        labels: compositionLabels,
        datasets: [{
            data: compositionData,
            backgroundColor: compositionColors,
            borderWidth: 0,
            hoverOffset: 4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '75%',
        plugins: {
            legend: { display: false },
            tooltip: {
                backgroundColor: 'rgba(18, 25, 33, 0.9)',
                padding: 12,
                cornerRadius: 8,
                callbacks: {
                    label: function(context) {
                        return ' ' + context.label + ': ' + context.raw + '%';
                    }
                }
            }
        }
    }
});

// Build custom legend for Doughnut chart
const legendContainer = document.getElementById('compositionLegend');
compositionLabels.forEach((label, i) => {
    const item = document.createElement('div');
    item.className = 'legend-item';
    item.innerHTML = `
        <div class="legend-label">
            <span class="legend-color" style="background-color: ${compositionColors[i]}"></span>
            ${label}
        </div>
        <div class="legend-value">${compositionData[i]}%</div>
    `;
    legendContainer.appendChild(item);
});

// 3. Active Biodigester Systems — Real: 1 system (Rampur) operational
const ctxAdoption = document.getElementById('adoptionChart').getContext('2d');
new Chart(ctxAdoption, {
    type: 'bar',
    data: {
        labels: ['Jan 2026', 'Feb 2026', 'Mar 2026'],
        datasets: [{
            label: 'Active Systems',
            data: [1, 1, 1],
            backgroundColor: '#a78bfa',
            borderRadius: 6,
            barThickness: 40
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false }
        },
        scales: {
            y: {
                beginAtZero: true,
                max: 5,
                grid: { drawBorder: false },
                title: { display: true, text: 'Number of Systems' },
                ticks: { stepSize: 1 }
            },
            x: {
                grid: { display: false }
            }
        }
    }
});

// ─── Sidebar Collapse/Expand Toggle ───
const sidebar = document.getElementById('sidebar');
const toggleBtn = document.getElementById('sidebar-toggle');
if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('expanded');
        lucide.createIcons();
    });
}
