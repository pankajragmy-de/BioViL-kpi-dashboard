# BioViL Energy KPI Dashboard — Detailed Technical Report & Walkthrough

## 1. Executive Summary
The **BioViL Energy KPI Dashboard** is a bespoke, real-time monitoring interface designed to track the performance, environmental impact, and social outcomes of rural bioenergy projects. 

This specific deployment is configured for **Operational Prototype #1** located in **Rampur, Assam**, which features a 4 m³ underground fixed-dome biodigester. The system processes approximately 600 kg of animal manure (cow dung) monthly, displacing 120 kg of firewood and empowering the local community through targeted training and employment.

## 2. Dashboard Architecture & User Experience

### 2.1 Interface & Aesthetics
The dashboard is built as an interactive Single Page Application (SPA)-style interface using vanilla HTML, CSS, and JavaScript. It utilizes a **premium dark-mode glassmorphism design** system.
*   **Navigation:** A fully responsive sidebar that automatically collapses into an icon-only view on smaller screens (≤1200px) to maximize data visibility.
*   **Cross-Page Routing:** Seamless hash-based URL routing (e.g., `project1.html#environmental-tab`) allows users to jump directly to specific impact metrics from the global overview page.

### 2.2 Dynamic Time Progression
Unlike static dashboards, the BioViL tracking system utilizes an **Auto-Growing Timeline Algorithm**.
*   **Deployment Anchor:** The system is anchored to the operational start date of **January 15, 2026**.
*   **Live Updates:** Every time the dashboard is loaded, the JavaScript engine calculates the exact number of weeks elapsed since the start date. It automatically generates new data points on the trend charts and updates the cumulative totals (e.g., "All Time (Since Jan '26)").

## 3. Biological Fluctuation Model & Charting

The "Biogas Output & Waste Input" chart algorithm models realistic, non-linear bioprocess variations based on the local climate of Assam.

### 3.1 Mesophilic Temperature Sensitivity
Fixed-dome unheated biodigesters operate in the *mesophilic* temperature range, taking a heavy performance penalty when temperatures drop. To reflect this, the dashboard relies on an integrated **Yield Multiplier Curve** based on average ambient temperatures in Assam:
*   **Winter (Jan-Feb, ~15-20°C):** Yield drops to ~0.016 - 0.018 m³ biogas per kg of fresh waste.
*   **Summer (Jul-Aug, >30°C):** Yield accelerates to ~0.035 m³ biogas per kg.

### 3.2 Deterministic Organic Noise
To simulate real-world waste collection inaccuracies, a deterministic pseudo-random function adds a **±15% weekly variance** to the baseline waste input (140 kg/week), ensuring the charts display realistic peaks and valleys.

## 4. Key Performance Indicator (KPI) Calculations

The dashboard's internal logic calculates global KPIs cleanly from primary references.

### 4.1 Environmental Impact (CO₂e Avoided)
The cumulative CO₂e avoided encompasses two core mitigations:
1.  **Methane Capture (Waste Diversion):** Leaving 600 kg of fresh cow dung to rot in a warm, ponded slurry (Assam climate) generates roughly 218 kg CO₂e/month in uncaptured methane emissions.
2.  **Firewood Displacement:** Burning 120 kg of firewood emits approximately 220.1 kg CO₂e/month.

**Dashboard Equation:**
*   Total Monthly Offset = 438.1 kg CO₂e
*   Given 600 kg of waste processes 438.1 kg CO₂e, the system applies an exact multiplier: **`~0.73 kg CO₂e avoided per 1 kg of waste processed`**.
*   This multiplier is multiplied by the dynamically generated total waste array to output the live KPI.

### 4.2 Economic & Social Metrics
*   **Smoke-Free Hours:** Modeled at **3 hours saved per day** (21 hours/week) per active household displaced from indoor firewood cooking.
*   **Budget Utilization:** A standard €3,000 Catalyst Grant is successfully tracked across 5 categories, heavily weighted toward Construction Materials (€1,559) and Infrastructure (€952), with €600 raised in private equity co-financing.
*   **Community Capacity:** Tracks strictly verified targets: 5 Jobs Created, 4 Operators Trained, 1 Company Registered.

## 5. References & Documentation

1.  **Project 1 Raw Data:** *GHG_Emissions_Wood_&_Animal_waste.pdf* (Total monthly offsets, IPCC conversion logic).
2.  **Financials:** *03. Budget Overview - 7647.xlsx* and *02. Impact Goal Overview - 7647.xlsx* (Asset allocation and social goal completion).
3.  **Scientific Literature (Temperature Models):** Based on research regarding *Fixed-Dome Biodigester Performance in Northern India/Assam*, noting psychrophilic stalling (<20°C) and mesophilic peaking (35°C).

---
*Generated: March 2026*
*System: BioViL Analytics Engine*
