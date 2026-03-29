import pandas as pd
import xlsxwriter

def create_excel():
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('BioViL_KPI_Calculation_Model.xlsx', engine='xlsxwriter')

    # --- Sheet 1: Assumptions & Formulas ---
    assumptions_data = {
        'Parameter': [
            'Waste Feedstock',
            'Firewood Displaced',
            'Methane Avoided (Waste)',
            'Emissions Avoided (Wood)',
            'Total CO2e Offset per month',
            'CO2e Yield Ratio',
            'Assam Temperature Base Effect',
            'Smoke-Free Time'
        ],
        'Value': [
            '600 kg/mo',
            '120 kg/mo',
            '218 kg CO2e/mo',
            '220.1 kg CO2e/mo',
            '438.1 kg CO2e/mo',
            '0.73 kg CO2e / kg waste',
            '0.016 (Winter) to 0.035 (Summer) m3 biogas/kg waste',
            '3 hrs/day (21 hrs/wk) per household'
        ],
        'Reference / Source / Logic': [
            'GHG_Emissions_Wood_&_Animal_waste.pdf & Client Specs',
            'GHG_Emissions_Wood_&_Animal_waste.pdf',
            'Calculated via IPCC MCF=65% (Liquid/Slurry, Warm Climate) & AR6 GWP',
            'EPA "Wood and Wood Residuals" factor (~1.81 kg CO2/kg wood)',
            'Sum of Waste + Wood offsets',
            'Dashboard internal multiplier (438.1 / 600 kg). Used to dynamically calculate live KPI.',
            'Mesophilic bacterial efficiency in Assam climate. Used to generate the biological curve in the dashboard charts.',
            'Client impact goals & industry standard'
        ]
    }
    df_assumptions = pd.DataFrame(assumptions_data)
    df_assumptions.to_excel(writer, sheet_name='Core Logic & References', index=False)

    # --- Sheet 2: Assam Temperature Yield Model ---
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    yield_curve = [0.016, 0.018, 0.026, 0.030, 0.033, 0.035, 0.035, 0.034, 0.032, 0.028, 0.022, 0.017]
    temp_model = {
        'Month': months,
        'Mesophilic Yield Multiplier (m3 biogas / kg waste)': yield_curve,
        'Biological State': ['Psychrophilic/Low', 'Psychrophilic/Low', 'Warming', 'Mesophilic/Optimal', 'Mesophilic/Optimal', 'Mesophilic/Peak', 'Mesophilic/Peak', 'Mesophilic/Peak', 'Mesophilic/Optimal', 'Cooling', 'Cooling', 'Psychrophilic/Low']
    }
    df_temps = pd.DataFrame(temp_model)
    df_temps.to_excel(writer, sheet_name='Biological Temperature Model', index=False)

    # Format sheets
    workbook = writer.book
    worksheet1 = writer.sheets['Core Logic & References']
    worksheet2 = writer.sheets['Biological Temperature Model']

    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1})
    cell_format = workbook.add_format({'text_wrap': True, 'valign': 'top', 'border': 1})

    for col_num, value in enumerate(df_assumptions.columns.values):
        worksheet1.write(0, col_num, value, header_format)
    worksheet1.set_column('A:A', 30, cell_format)
    worksheet1.set_column('B:B', 30, cell_format)
    worksheet1.set_column('C:C', 60, cell_format)

    for col_num, value in enumerate(df_temps.columns.values):
        worksheet2.write(0, col_num, value, header_format)
    worksheet2.set_column('A:A', 20, cell_format)
    worksheet2.set_column('B:B', 45, cell_format)
    worksheet2.set_column('C:C', 30, cell_format)

    writer.close()
    print("Excel model successfully synthesized.")

if __name__ == "__main__":
    create_excel()
