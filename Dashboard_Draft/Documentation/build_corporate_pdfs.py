import markdown
import os

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = "/Users/pankajsharma/Library/CloudStorage/OneDrive-Personal/AI Agents/Bioenergy_KPI_Dashboard/Logo/logo 1colour  bg w.svg"
YIELD_IMG = os.path.join(DOCS_DIR, "yield_curve.png")
CO2_IMG = os.path.join(DOCS_DIR, "co2_impact.png")
CO2_CUM_IMG = os.path.join(DOCS_DIR, "co2_cumulative.png")
BUDGET_IMG = os.path.join(DOCS_DIR, "budget_chart.png")

# ─── BioViL Corporate Identity (CI) ───
# Primary:  Deep Teal #083f5e
# Accent:   BioViL Orange #f7941d / #fbb040
# Success:  Emerald #10b981
# Text:     Slate #1e293b / #334155 / #64748b
# Bg:       White #ffffff / Light Gray #f8fafc / Green-tint #f0fdf4

REPORT_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

@page {
    size: A4;
    margin: 15mm 15mm 18mm 15mm;
}

body {
    font-family: 'Outfit', -apple-system, 'Segoe UI', sans-serif;
    color: #1e293b;
    line-height: 1.7;
    font-size: 11pt;
    background: #fff;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
}

/* ── HEADER/FOOTER SPACING TRICK ── */
.header-space { height: 65px; }
.footer-space { height: 45px; }

/* ── GLOBAL FIXED HEADER — repeats on EVERY printed page ── */
.global-header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0 10px;
    border-bottom: 2px solid #083f5e;
    background: #fff;
    z-index: 1000;
}
.global-header img { height: 30px; }
.global-header .doc-label {
    font-size: 8.5pt;
    font-weight: 600;
    color: #083f5e;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

/* ── GLOBAL FIXED FOOTER — repeats on EVERY printed page ── */
.global-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0 0;
    border-top: 1px solid #e2e8f0;
    font-size: 7.5pt;
    color: #94a3b8;
    background: #fff;
    z-index: 1000;
}

/* ── COVER PAGE ── */
.cover {
    width: calc(100vw + 30mm); /* 15mm left + 15mm right margin */
    height: calc(100vh + 33mm); /* 15mm top + 18mm bottom margin */
    margin-top: -15mm;
    margin-left: -15mm;
    margin-right: -15mm;
    margin-bottom: -18mm;
    padding: 0 40px;
    background: linear-gradient(135deg, #083f5e 0%, #0a5a7a 40%, #10b981 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    color: white;
    page-break-after: always;
    position: relative;
    z-index: 2000;
    overflow: hidden;
}
.cover::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at 30% 50%, rgba(251,176,64,0.15) 0%, transparent 60%);
}
.cover-logo {
    width: 180px;
    margin-bottom: 50px;
    filter: brightness(0) invert(1);
    position: relative;
    z-index: 1;
}
.cover-tag {
    font-size: 10pt;
    font-weight: 500;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.7);
    margin-bottom: 20px;
    position: relative;
    z-index: 1;
}
.cover h1 {
    font-size: 36pt;
    font-weight: 800;
    letter-spacing: -1.5px;
    line-height: 1.15;
    margin-bottom: 20px;
    position: relative;
    z-index: 1;
    max-width: 700px;
}
.cover-sub {
    font-size: 14pt;
    font-weight: 300;
    color: rgba(255,255,255,0.85);
    max-width: 550px;
    margin-bottom: 60px;
    position: relative;
    z-index: 1;
}
.cover-meta {
    font-size: 10pt;
    color: rgba(255,255,255,0.5);
    letter-spacing: 1px;
    border-top: 1px solid rgba(255,255,255,0.2);
    padding-top: 20px;
    position: relative;
    z-index: 1;
}

/* ── SECTION BREAK ── */
.section-break {
    page-break-before: always;
}

/* ── TYPOGRAPHY ── */
h1.section-title {
    font-size: 22pt;
    font-weight: 700;
    color: #083f5e;
    margin-bottom: 8px;
    margin-top: 5px;
    letter-spacing: -0.5px;
}
.section-num {
    font-size: 11pt;
    font-weight: 600;
    color: #f7941d;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 5px;
    display: block;
}
h2 {
    font-size: 15pt;
    font-weight: 600;
    color: #083f5e;
    margin-top: 25px;
    margin-bottom: 10px;
}
h3 {
    font-size: 12pt;
    font-weight: 600;
    color: #334155;
    margin-top: 18px;
    margin-bottom: 8px;
}
p {
    margin-bottom: 12px;
    color: #334155;
    text-align: justify;
}
ul, ol {
    margin-bottom: 14px;
    padding-left: 28px;
}
li {
    margin-bottom: 6px;
    color: #334155;
}
strong { color: #0f172a; }

/* ── KEY METRIC STRIP ── */
.kpi-strip {
    display: flex;
    gap: 12px;
    margin: 20px 0;
    page-break-inside: avoid;
}
.kpi-card {
    flex: 1;
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 10px;
    padding: 14px 12px;
    text-align: center;
}
.kpi-card .kpi-val {
    font-size: 20pt;
    font-weight: 700;
    color: #083f5e;
    line-height: 1.2;
}
.kpi-card .kpi-unit {
    font-size: 10pt;
    color: #64748b;
    font-weight: 400;
}
.kpi-card .kpi-label {
    font-size: 8pt;
    color: #64748b;
    margin-top: 3px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── FIGURE CONTAINER ── */
.figure {
    margin: 20px 0;
    page-break-inside: avoid;
}
.figure img {
    display: block;
    max-width: 100%;
    margin: 0 auto;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
}
.figure-caption {
    text-align: center;
    font-size: 9pt;
    color: #64748b;
    font-style: italic;
    margin-top: 8px;
}

/* ── DATA BOX / CALLOUT ── */
.callout {
    background: #f0fdf4;
    border-left: 4px solid #10b981;
    padding: 16px 18px;
    margin: 18px 0;
    border-radius: 0 8px 8px 0;
    page-break-inside: avoid;
}
.callout-orange {
    background: #fffbeb;
    border-left-color: #f7941d;
}
.callout strong { display: block; margin-bottom: 4px; color: #083f5e; }
.callout code {
    font-family: 'SF Mono', 'Courier New', monospace;
    font-size: 10pt;
    color: #059669;
    display: block;
    margin: 3px 0;
}

/* ── TABLE ── */
.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
    font-size: 10pt;
    page-break-inside: avoid;
}
.data-table th {
    background: #083f5e;
    color: white;
    padding: 8px 12px;
    text-align: left;
    font-weight: 600;
    font-size: 9pt;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.data-table td {
    padding: 8px 12px;
    border-bottom: 1px solid #e2e8f0;
    color: #334155;
}
.data-table tr:nth-child(even) td { background: #f8fafc; }

/* ── SIDE-BY-SIDE ── */
.two-col {
    display: flex;
    gap: 20px;
    align-items: flex-start;
    margin: 16px 0;
    page-break-inside: avoid;
}
.two-col > div { flex: 1; }
.two-col img { max-width: 100%; border-radius: 8px; border: 1px solid #e2e8f0; }

/* ── REFERENCES ── */
.ref-list {
    font-size: 9.5pt;
    color: #64748b;
    padding-left: 20px;
    list-style-type: decimal;
}
.ref-list li { margin-bottom: 6px; color: #64748b; }
.ref-list em { color: #334155; font-weight: 500; }
"""


def build_detailed_report():
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>BioViL — KPI Dashboard Technical Report</title>
    <style>{REPORT_CSS}</style>
</head>
<body>

<!-- ── GLOBAL FIXED HEADER (repeats on every printed page) ── -->
<div class="global-header">
    <img src="file://{LOGO_PATH}" alt="BioViL">
    <div class="doc-label">Technical Report — BioViL Energy</div>
</div>

<!-- ── GLOBAL FIXED FOOTER (repeats on every printed page) ── -->
<div class="global-footer">
    <span>BioViL Energy — Confidential</span>
    <span>March 2026 — Version 1.0</span>
</div>

<!-- ═══════════════════ COVER PAGE ═══════════════════ -->
<div class="cover">
    <img class="cover-logo" src="file://{LOGO_PATH}" alt="BioViL">
    <div class="cover-tag">Technical Report</div>
    <h1>KPI Dashboard Architecture & Operations Guide</h1>
    <div class="cover-sub">Comprehensive documentation of the BioViL Energy KPI Tracking System, biological fluctuation modeling, and environmental impact calculations.</div>
    <div class="cover-meta">March 2026 &nbsp;•&nbsp; Confidential &nbsp;•&nbsp; Version 1.0</div>
</div>

<!-- ═══════════════════ MAIN CONTENT WRAPPER ═══════════════════ -->
<table style="width: 100%; border-collapse: separate; border-spacing: 0;">
    <thead><tr><td><div class="header-space"></div></td></tr></thead>
    <tbody><tr><td>

<!-- ═══════════════════ SECTION 1: EXECUTIVE SUMMARY ═══════════════════ -->
<span class="section-num">Section 01</span>
<h1 class="section-title">Executive Summary</h1>
<p>The <strong>BioViL Energy KPI Dashboard</strong> is a bespoke, real-time monitoring and analytics platform designed to track the performance, environmental impact, and social outcomes of rural bioenergy deployments across India.</p>
<p>This report documents Operational Prototype #1, deployed in <strong>Rampur, Assam</strong>, featuring a 4 m³ underground fixed-dome biodigester operational since <strong>January 15, 2026</strong>. The system processes approximately 600 kg of animal manure monthly, displacing 120 kg of firewood and delivering measurable CO₂ reductions.</p>

<div class="kpi-strip">
    <div class="kpi-card">
        <div class="kpi-val">438.1 <span class="kpi-unit">kg</span></div>
        <div class="kpi-label">CO₂e Avoided / Month</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-val">600 <span class="kpi-unit">kg</span></div>
        <div class="kpi-label">Waste Diverted / Month</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-val">~20 <span class="kpi-unit">m³</span></div>
        <div class="kpi-label">Biogas Produced / Month</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-val">90 <span class="kpi-unit">hrs</span></div>
        <div class="kpi-label">Smoke-Free Hours / Month</div>
    </div>
</div>

<h2>System Specifications</h2>
<table class="data-table">
    <tr><th>Parameter</th><th>Specification</th></tr>
    <tr><td>Digester Type</td><td>Underground Fixed-Dome (Deenbandhu Model)</td></tr>
    <tr><td>System Capacity</td><td>4 m³</td></tr>
    <tr><td>Feedstock</td><td>100% Animal Manure (Cow Dung)</td></tr>
    <tr><td>Monthly Feedstock Volume</td><td>~600 kg fresh weight</td></tr>
    <tr><td>Firewood Displaced</td><td>~120 kg/month</td></tr>
    <tr><td>Operational Since</td><td>January 15, 2026</td></tr>
    <tr><td>Location</td><td>Rampur, Assam, India</td></tr>
</table>

<!-- ═══════════════════ SECTION 2: ENVIRONMENTAL IMPACT ═══════════════════ -->
<div class="section-break"></div>
<span class="section-num">Section 02</span>
<h1 class="section-title">Environmental Impact Model</h1>
<p>The dashboard calculates cumulative CO₂ equivalent (CO₂e) emissions avoided through two primary mitigation pathways:</p>

<h2>2.1 Methane Capture (Waste Diversion)</h2>
<p>Left untreated in warm, ponded slurry (typical of Assam's tropical climate), 600 kg of fresh cow dung generates approximately <strong>218 kg CO₂e/month</strong> in uncaptured methane emissions. This calculation follows the IPCC Tier-1 methodology with a Methane Conversion Factor (MCF) of 65% for liquid/slurry systems in warm climates, applying the AR6 Global Warming Potential (GWP) of 27.9 for biogenic methane.</p>

<h2>2.2 Firewood Displacement</h2>
<p>The biogas produced directly displaces the burning of approximately 120 kg of firewood per month for cooking. Using the EPA emission factor of approximately 1.81 kg CO₂ per kg of wood combusted, this avoids <strong>220.1 kg CO₂e/month</strong> in direct emissions and eliminates indoor air pollution.</p>

<div class="figure">
    <img src="file://{CO2_IMG}" alt="CO2 Impact Breakdown" style="max-width: 380px;">
    <div class="figure-caption">Figure 1 — Monthly CO₂ Emissions Avoided: Breakdown by Mitigation Pathway</div>
</div>

<div class="callout">
    <strong>Dashboard Calculation Engine</strong>
    <code>Total Monthly Offset = 218 + 220.1 = 438.1 kg CO₂e</code>
    <code>Internal Multiplier = 438.1 ÷ 600 = 0.73 kg CO₂e per kg waste</code>
    <p style="margin-top: 6px; font-size: 10pt;">This multiplier is applied dynamically to the cumulative waste processed by the system to compute the live KPI shown on the dashboard at any given point in time.</p>
</div>

<h2>2.3 Projected Annual CO₂e Trajectory</h2>
<p>Based on the monthly offset of 438.1 kg CO₂e and accounting for the seasonal temperature-driven yield variations (Section 3), the system projects approximately <strong>5.26 tonnes of CO₂e avoided</strong> in the first full year of operation. The cumulative trajectory accelerates during summer months when higher temperatures drive greater biogas yields.</p>

<div class="figure">
    <img src="file://{CO2_CUM_IMG}" alt="Cumulative CO2 Trajectory" style="max-width: 380px;">
    <div class="figure-caption">Figure 2 — Projected Cumulative CO₂e Emissions Avoided Over 2026 (Annual Target: 5.26 Tonnes)</div>
</div>

<!-- ═══════════════════ SECTION 3: BIOLOGICAL MODEL ═══════════════════ -->
<div class="section-break"></div>
<span class="section-num">Section 03</span>
<h1 class="section-title">Biological Fluctuation Model</h1>
<p>To provide stakeholders with scientifically accurate visualizations, the dashboard's charting engine models realistic, non-linear bioprocess variations based on the local climate of Assam. Unlike static linear projections, the system accounts for the fundamental relationship between ambient temperature and anaerobic digester performance.</p>

<h2>3.1 Mesophilic Temperature Sensitivity</h2>
<p>Unheated fixed-dome biodigesters are directly influenced by ground and ambient temperatures. In the <em>mesophilic</em> range (25–40°C), methanogenic bacteria operate at peak efficiency. When temperatures drop below 20°C (common in Assam's winters), bacterial activity slows significantly — a state known as <em>psychrophilic stalling</em>.</p>
<p>The dashboard integrates a <strong>12-month Yield Multiplier Curve</strong> specifically calibrated for Assam's climate zone:</p>

<div class="figure">
    <img src="file://{YIELD_IMG}" alt="Biogas Yield Curve" style="max-width: 420px;">
    <div class="figure-caption">Figure 3 — Annual Biogas Yield Variation Based on Assam's Seasonal Temperature Cycle</div>
</div>

<table class="data-table">
    <tr><th>Month</th><th>Yield (m³/kg)</th><th>Biological State</th></tr>
    <tr><td>January</td><td>0.016</td><td>Psychrophilic / Low Activity</td></tr>
    <tr><td>February</td><td>0.018</td><td>Psychrophilic / Low Activity</td></tr>
    <tr><td>March</td><td>0.026</td><td>Warming Transition</td></tr>
    <tr><td>April – May</td><td>0.030 – 0.033</td><td>Mesophilic / Optimal</td></tr>
    <tr><td>June – August</td><td>0.035</td><td>Mesophilic / Peak Performance</td></tr>
    <tr><td>September</td><td>0.032</td><td>Mesophilic / Optimal</td></tr>
    <tr><td>October – November</td><td>0.028 – 0.022</td><td>Cooling Transition</td></tr>
    <tr><td>December</td><td>0.017</td><td>Psychrophilic / Low Activity</td></tr>
</table>

<h2>3.2 Deterministic Organic Noise</h2>
<p>To simulate real-world waste collection variability, the algorithm applies a <strong>±15% weekly variance</strong> to the baseline waste input (140 kg/week) using a deterministic pseudo-random seed function. This ensures the charts display realistic peaks and valleys while remaining reproducible across page loads.</p>

<!-- ═══════════════════ SECTION 4: FINANCIAL & SOCIAL ═══════════════════ -->
<div class="section-break"></div>
<span class="section-num">Section 04</span>
<h1 class="section-title">Financial Deployment & Social Impact</h1>

<h2>4.1 Budget Utilization</h2>
<p>The project was funded through a €3,000 Catalyst Grant supplemented by €600 in private equity co-financing. The dashboard provides transparent, line-item accounting of how every euro was deployed locally.</p>

<div class="figure">
    <img src="file://{BUDGET_IMG}" alt="Budget Allocation" style="max-width: 380px;">
    <div class="figure-caption">Figure 4 — Catalyst Grant Utilization by Category (€3,000 Total)</div>
</div>

<table class="data-table">
    <tr><th>Category</th><th>Amount (€)</th><th>Share</th></tr>
    <tr><td>Construction Materials</td><td>1,559</td><td>52%</td></tr>
    <tr><td>IT & Website Infrastructure</td><td>952</td><td>32%</td></tr>
    <tr><td>Local Labor</td><td>303</td><td>10%</td></tr>
    <tr><td>Transport & Operations</td><td>115</td><td>4%</td></tr>
    <tr><td>Miscellaneous</td><td>71</td><td>2%</td></tr>
</table>

<h2>4.2 Social Impact Outcomes</h2>
<table class="data-table">
    <tr><th>Metric</th><th>Target</th><th>Achieved</th><th>Status</th></tr>
    <tr><td>Smoke-Free Indoor Hours</td><td>3 hrs/day</td><td>3 hrs/day</td><td style="color: #10b981; font-weight: 600;">✓ On Track</td></tr>
    <tr><td>Jobs Created (Local)</td><td>5</td><td>5</td><td style="color: #10b981; font-weight: 600;">✓ Achieved</td></tr>
    <tr><td>Community Operators Trained</td><td>3</td><td>4</td><td style="color: #10b981; font-weight: 600;">✓ Exceeded</td></tr>
    <tr><td>Company Registration</td><td>1</td><td>1</td><td style="color: #10b981; font-weight: 600;">✓ Achieved</td></tr>
    <tr><td>Pioneer Phase (Scaling)</td><td>5 systems</td><td>1 system</td><td style="color: #f7941d; font-weight: 600;">⬤ 20%</td></tr>
</table>

<div class="callout callout-orange">
    <strong>Health Impact Note</strong>
    <p style="font-size: 10pt; margin: 0;">The displacement of 120 kg/month of indoor firewood burning eliminates the household's primary source of fine particulate matter (PM2.5) exposure. WHO estimates that household air pollution from solid fuels causes over 3.2 million premature deaths annually. Each additional biodigester deployed contributes directly to reducing this burden.</p>
</div>

<!-- ═══════════════════ SECTION 5: ARCHITECTURE & REFERENCES ═══════════════════ -->
<div class="section-break"></div>
<span class="section-num">Section 05</span>
<h1 class="section-title">Dashboard Architecture</h1>
<p>The BioViL KPI Dashboard is a static-site application built with HTML5, CSS3, and vanilla JavaScript. It requires no server-side infrastructure and can be deployed on any web hosting platform.</p>

<h2>5.1 Dynamic Time Progression</h2>
<p>The system is anchored to the operational start date (January 15, 2026). On each page load, the JavaScript engine calculates the exact number of weeks elapsed and automatically generates new weekly data points, updating all charts and cumulative KPIs without any manual data entry.</p>

<h2>5.2 Technology Stack</h2>
<table class="data-table">
    <tr><th>Component</th><th>Technology</th><th>Purpose</th></tr>
    <tr><td>Charting</td><td>Chart.js v4</td><td>Interactive line, doughnut, and bar charts</td></tr>
    <tr><td>Icons</td><td>Lucide Icons</td><td>Lightweight, open-source SVG icon system</td></tr>
    <tr><td>Styling</td><td>Custom CSS (Glassmorphism)</td><td>Premium dark-mode aesthetic</td></tr>
    <tr><td>Typography</td><td>Google Fonts (Outfit)</td><td>Modern variable-weight typeface</td></tr>
    <tr><td>Routing</td><td>URL Hash-based</td><td>Cross-page tab navigation</td></tr>
</table>

<h2>5.3 Responsive Behavior</h2>
<p>The sidebar navigation auto-collapses into an icon-only mode on viewports ≤1200px wide, maximizing the data visualization area on tablets and smaller screens.</p>

<div class="section-break"></div>
<span class="section-num">Section 06</span>
<h1 class="section-title">References & Source Documents</h1>
<ol class="ref-list">
    <li><em>GHG_Emissions_Wood_&_Animal_waste.pdf</em> — Project 1 internal document. Provides monthly methane (MCF=65%) and firewood (1.81 kg CO₂/kg) emission calculations following IPCC Tier-1 methodology and AR6 GWP values.</li>
    <li><em>03. Budget Overview - 7647.xlsx</em> — Catalyst programme financial ledger. Provides line-item grant expenditure across all project categories.</li>
    <li><em>02. Impact Goal Overview - 7647.xlsx</em> — Social impact tracking document. Defines targets for employment, training, and scaling milestones.</li>
    <li>IPCC (2019). <em>2019 Refinement to the 2006 IPCC Guidelines for National Greenhouse Gas Inventories</em>. Volume 5, Chapter 4: Biological Treatment of Solid Waste.</li>
    <li>U.S. EPA (2023). <em>Emission Factors for Greenhouse Gas Inventories</em>. Table 1: Stationary Combustion, Wood and Wood Residuals.</li>
    <li>Bond, T. & Templeton, M.R. (2011). "History and future of domestic biogas plants in the developing world." <em>Energy for Sustainable Development</em>, 15(4), pp.347–354.</li>
</ol>

    </td></tr></tbody>
    <tfoot><tr><td><div class="footer-space"></div></td></tr></tfoot>
</table>

</body>
</html>"""

    with open(os.path.join(DOCS_DIR, 'BioViL_Detailed_Report.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print("✓ Detailed Report HTML generated")


def build_one_pager():
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>BioViL — Executive One-Pager</title>
    <style>{REPORT_CSS}
    /* Override body padding for one-pager */
    body {{ padding-top: 0; padding-bottom: 0; }}
    .global-header, .global-footer {{ display: none; }}
    
    .op-wrapper {{
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }}
    .op-hero {{
        background: linear-gradient(135deg, #083f5e 0%, #0a5a7a 60%, #10b981 100%);
        color: white;
        padding: 22px 35px 18px;
        display: flex;
        align-items: center;
        gap: 20px;
    }}
    .op-hero img {{ height: 45px; filter: brightness(0) invert(1); }}
    .op-hero h1 {{ font-size: 18pt; font-weight: 700; letter-spacing: -0.5px; margin: 0; }}
    .op-hero .op-tag {{
        font-size: 8.5pt;
        font-weight: 400;
        color: rgba(255,255,255,0.7);
        margin-top: 3px;
    }}
    .op-body {{
        padding: 12px 35px 0;
        flex: 1;
        display: flex;
        flex-direction: column;
    }}
    .op-strip {{
        display: flex;
        margin: 12px 0;
        gap: 8px;
    }}
    .op-strip .kpi-card {{ padding: 10px 8px; }}
    .op-strip .kpi-val {{ font-size: 16pt; }}
    .op-strip .kpi-label {{ font-size: 7pt; }}
    .pillar {{
        margin: 6px 0;
        padding: 10px 14px;
        border-radius: 8px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
    }}
    .pillar h3 {{
        margin: 0 0 4px;
        color: #083f5e;
        font-size: 10.5pt;
    }}
    .pillar p {{ margin: 0; font-size: 9pt; line-height: 1.5; }}
    .op-two {{ display: flex; gap: 8px; }}
    .op-two .pillar {{ flex: 1; }}
    .op-three {{ display: flex; gap: 8px; margin: 8px 0; }}
    .op-three > div {{ flex: 1; }}
    .op-three img {{
        max-width: 100%;
        border-radius: 6px;
        border: 1px solid #e2e8f0;
    }}
    .op-three .img-caption {{
        text-align: center;
        font-size: 7pt;
        color: #94a3b8;
        margin-top: 4px;
    }}
    .op-footer {{
        border-top: 2px solid #083f5e;
        padding: 8px 35px;
        font-size: 7.5pt;
        color: #94a3b8;
        display: flex;
        justify-content: space-between;
        margin-top: auto;
    }}
    </style>
</head>
<body>

<div class="op-wrapper">

<div class="op-hero">
    <img src="file://{LOGO_PATH}" alt="BioViL">
    <div>
        <h1>Executive Field Summary: Prototype #1</h1>
        <div class="op-tag">Rampur, Assam — 4 m³ Fixed-Dome Biodigester — Operational since Jan 15, 2026</div>
    </div>
</div>

<div class="op-body">
    <div class="op-strip">
        <div class="kpi-card">
            <div class="kpi-val">438 <span class="kpi-unit">kg</span></div>
            <div class="kpi-label">CO₂e Avoided / Mo</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-val">600 <span class="kpi-unit">kg</span></div>
            <div class="kpi-label">Waste Diverted / Mo</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-val">120 <span class="kpi-unit">kg</span></div>
            <div class="kpi-label">Firewood Replaced / Mo</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-val">5.26 <span class="kpi-unit">t</span></div>
            <div class="kpi-label">CO₂e Target / Year</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-val">3 <span class="kpi-unit">hrs</span></div>
            <div class="kpi-label">Smoke-Free / Day</div>
        </div>
    </div>

    <div class="op-two">
        <div class="pillar">
            <h3>🌍 Environmental Stewardship</h3>
            <p>Capturing methane from 600 kg of waste avoids <strong>218 kg CO₂e/month</strong>. Displacing 120 kg of firewood avoids <strong>220.1 kg CO₂e/month</strong>. Combined: <strong>438.1 kg CO₂e/month</strong> (IPCC Tier-1, AR6 GWP).</p>
        </div>
        <div class="pillar">
            <h3>🤝 Social Capacity</h3>
            <p><strong>5 jobs</strong> created locally. <strong>4 operators</strong> trained (exceeding target). <strong>3 hrs/day</strong> smoke-free indoor air, reducing PM2.5 exposure. <strong>1 company</strong> registered.</p>
        </div>
        <div class="pillar">
            <h3>💰 Financial Transparency</h3>
            <p><strong>€3,000</strong> Catalyst Grant + <strong>€600</strong> Private Equity. 100% allocated locally: construction (€1,559), IT (€952), labor (€303), transport (€115).</p>
        </div>
    </div>

    <!-- Three charts in a row -->
    <div class="op-three">
        <div>
            <img src="file://{CO2_IMG}" alt="CO2 Breakdown">
            <div class="img-caption">Monthly CO₂e Breakdown</div>
        </div>
        <div>
            <img src="file://{YIELD_IMG}" alt="Yield Curve">
            <div class="img-caption">Biogas Yield vs Temperature</div>
        </div>
        <div>
            <img src="file://{BUDGET_IMG}" alt="Budget">
            <div class="img-caption">Grant Utilization (€3,000)</div>
        </div>
    </div>

    <div class="pillar" style="margin-top: 4px;">
        <h3>📊 Advanced Biological Modeling</h3>
        <p>The dashboard dynamically adjusts biogas projections using Assam's mesophilic temperature curve. Winter yield drops to 0.016 m³/kg; summer peaks at 0.035 m³/kg — reflecting real bioprocess behavior with ±15% organic variance applied weekly.</p>
    </div>
</div>

<div class="op-footer">
    <span>BioViL Energy — Confidential — March 2026</span>
    <span>Version 1.0</span>
</div>

</div> <!-- end op-wrapper -->

</body>
</html>"""

    with open(os.path.join(DOCS_DIR, 'BioViL_One_Pager.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print("✓ One-Pager HTML generated")


if __name__ == "__main__":
    build_detailed_report()
    build_one_pager()
