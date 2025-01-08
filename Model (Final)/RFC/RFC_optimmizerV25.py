import os
import pandas as pd
import pyomo.environ as pyo
from collections import ChainMap
from RFC_ConcreteV24 import create_RFC_modelV24
from contextlib import redirect_stdout


#Sets
T = range(0, 8760) #Time period {0,...,8759}
WS = [1, 2, 3, 4] #Sizes of wind turbine {1=100kW, 2=500kW, 3=800kW, 4=1500kW}
RS = [1, 2, 3] #Sizes of RFC {1=1000kW, 2=20000kW, 3=100000kW}
HFS = [1] #Sizes of H2 furnace {1=17.58kW}
C = ['Francois', 'Beaver Creek', 'Wrigley', 'Tsiigehtchic', 'Resolute Bay', 'Aupaluk', 'Old Crow', 
'Peawanuck', 'Tadoule Lake', 'Kwadacha', 'Makkovik', 'Port Hope Simpson', 'Umiujaq', 'Ramea', 
'Whati', 'Brochet', 'Fort Good Hope', 'Kingfisher Lake', 'Old Masset', 'Port Clements', 
'Keewaywin', 'Fort McPherson', 'Kangiqsujuaq', 'Watson Lake', 'Fort Chipewyan', 
'Arctic Bay', 'Weagamow Lake', 'Natuashish', 'Kangiqsualujjuaq', 'Naujaat', 'Fort Simpson', 
'Shamattawa', 'Pond Inlet', 'Inukjuak', 'Kuujjuaq', 'Rankin Inlet', 'Iqaluit' ]

# Read the data from Excel using Pandas
df2 = pd.read_excel('RFC_DataV24.xls', 'Unit Size', header=0, index_col=0)
df3 = pd.read_excel('RFC_DataV24.xls', 'Max Cap', header=0, index_col=0)
df5 = pd.read_excel('RFC_DataV24.xls', 'Costs', header=0, index_col=0)
df6 = pd.read_excel('RFC_DataV24.xls', 'Constants', header=0, index_col=0)

results_folder = 'Results'

# Define data
A_temp = pd.DataFrame(df2['A']).to_dict()  # Swept area for each wind turbine size (m^2)
A = dict(ChainMap(*A_temp.values()))
Cp_temp = pd.DataFrame(df2['Cp']).to_dict()  # Coefficient of performance for each wind turbine size (0.33)
Cp = dict(ChainMap(*Cp_temp.values()))
Ci_temp = pd.DataFrame(df2['Ci']).to_dict()  # Cut in windspeed (m/s)
Ci = dict(ChainMap(*Ci_temp.values()))
Co_temp = pd.DataFrame(df2['Co']).to_dict()  # Cut out windspeed (m/s)
Co = dict(ChainMap(*Co_temp.values()))
WUe_temp = pd.DataFrame(df2['WUe']).to_dict() # Unit size for each wind turbine size (kW)
WUe = dict(ChainMap(*WUe_temp.values()))
RUe_temp = pd.DataFrame(df2['RUe']).to_dict() # Unit size for each RFC size (kW)
RUe = dict(ChainMap(*RUe_temp.values()))
HFUt_temp = pd.DataFrame(df2['HFUt']).to_dict() # Unit size for each H2 furnace (kW)
HFUt = dict(ChainMap(*HFUt_temp.values()))
WKe_temp = pd.DataFrame(df3['WKe']).to_dict() # Max electrical capacity wind energy (kW)
WKe = dict(ChainMap(*WKe_temp.values()))
RKe_temp = pd.DataFrame(df3['RKe']).to_dict() # Max electrical capacity RFC (kW)
RKe = dict(ChainMap(*RKe_temp.values()))
HFKt_temp = pd.DataFrame(df3['HFKt']).to_dict() # Max thermal capacity H2 furnace (kW)
HFKt = dict(ChainMap(*HFKt_temp.values()))
SKe_temp = pd.DataFrame(df3['SKe']).to_dict() # Max solar capacity (kW)
SKe = dict(ChainMap(*SKe_temp.values()))
WCAP_temp = pd.DataFrame(df5['WCAP']).to_dict() # CAPEX for each wind turbine size ($/kW)
WCAP = dict(ChainMap(*WCAP_temp.values()))
RCAP_temp = pd.DataFrame(df5['RCAP']).to_dict() # CAPEX for each RFC size ($/kW)
RCAP = dict(ChainMap(*RCAP_temp.values()))
HFCAP_temp = pd.DataFrame(df5['HFCAP']).to_dict() # CAPEX for H2 furnace ($/kW)
HFCAP = dict(ChainMap(*HFCAP_temp.values()))
SCAP_temp = pd.DataFrame(df5['SCAP']).to_dict() # CAPEX for Solar ($/kW)
SCAP = dict(ChainMap(*SCAP_temp.values()))
H2CAP_temp = pd.DataFrame(df5['H2CAP']).to_dict() # CAPEX for 10 kg H2 Storage 
H2CAP = dict(ChainMap(*H2CAP_temp.values()))
WOP_temp = pd.DataFrame(df5['WOP']).to_dict() # OPEX for each wind turbine size ($/kW)
WOP = dict(ChainMap(*WOP_temp.values()))
ROP_temp = pd.DataFrame(df5['ROP']).to_dict() # OPEX for each RFC size ($/kW)
ROP = dict(ChainMap(*ROP_temp.values()))
HFOP_temp = pd.DataFrame(df5['HFOP']).to_dict() # OPEX for H2 furnace size ($/kW)
HFOP = dict(ChainMap(*HFOP_temp.values()))
SOP_temp = pd.DataFrame(df5['SOP']).to_dict() # OPEX for Solar ($/kW)
SOP = dict(ChainMap(*SOP_temp.values()))
roe_temp = pd.DataFrame(df6['roe']).to_dict() # Air density (kg/m^3)
roe = dict(ChainMap(*roe_temp.values()))
r_temp = pd.DataFrame(df6['r']).to_dict() # Discount rate
r = dict(ChainMap(*r_temp.values()))
WL_temp = pd.DataFrame(df6['WL']).to_dict() # Lifetime of wind trubines
WL = dict(ChainMap(*WL_temp.values()))
RL_temp = pd.DataFrame(df6['RL']).to_dict() # Lifetime of RFC
RL = dict(ChainMap(*RL_temp.values()))
HFL_temp = pd.DataFrame(df6['HFL']).to_dict() # Lifetime of H2 Furnace
HFL = dict(ChainMap(*HFL_temp.values()))
SL_temp = pd.DataFrame(df6['SL']).to_dict() # Lifetime of Solar
SL = dict(ChainMap(*SL_temp.values()))
EtaR_temp = pd.DataFrame(df6['EtaR']).to_dict() # Efficiency of RFC
EtaR = dict(ChainMap(*EtaR_temp.values()))
Etas_temp = pd.DataFrame(df6['Etas']).to_dict() # Efficiency of RFC
Etas = dict(ChainMap(*Etas_temp.values()))
EtaHF_temp = pd.DataFrame(df6['EtaHF']).to_dict() # Efficiency of H2 furnace
EtaHF = dict(ChainMap(*EtaHF_temp.values()))
Rmin_temp = pd.DataFrame(df6['Rmin']).to_dict() # Minimum storage of H2 (SoR) (kg)
Rmin = dict(ChainMap(*Rmin_temp.values()))
H_E_temp = pd.DataFrame(df6['H_E']).to_dict() # Conversion of electrical energy to H2 (kg H2/kWh)
H_E = dict(ChainMap(*H_E_temp.values()))
E_H_temp = pd.DataFrame(df6['E_H']).to_dict() # Conversion of H2 to electrical energy (kg H2/kWh) 
E_H = dict(ChainMap(*E_H_temp.values()))
H_T_temp = pd.DataFrame(df6['H_T']).to_dict() # Conversion of H2 to thermal energy (kg H2/kWh)
H_T = dict(ChainMap(*H_T_temp.values()))
M_temp = pd.DataFrame(df6['M']).to_dict() # Water requirement for H2 processes (kg H20/kg H2)
M = dict(ChainMap(*M_temp.values()))
H2L_temp = pd.DataFrame(df6['H2L']).to_dict() # Water requirement for H2 processes (kg H20/kg H2)
H2L = dict(ChainMap(*H2L_temp.values()))


# Run model for all models in set C
for c in C:
    df1 = pd.read_excel('RFC Datasets - Final.xlsx', c, header=0)

    # Define location specific data
    W_temp = pd.DataFrame(df1['wind_speed']).to_dict() # Windspeed (m/s)
    W = dict(ChainMap(*W_temp.values()))
    S_temp = pd.DataFrame(df1['DNI']).to_dict() # Direct Normal Iraddiance (kw/m²)
    S = dict(ChainMap(*S_temp.values()))
    L_temp = pd.DataFrame(df1['L']).to_dict() # Electric load (kW)
    L = dict(ChainMap(*L_temp.values()))
    LT_temp = pd.DataFrame(df1['Lt']).to_dict() # Thermal load (kW)
    LT = dict(ChainMap(*LT_temp.values()))
    Hi_temp = pd.DataFrame(df1['H2_tank_size']).to_dict()
    Hi = df1['H2_tank_size'].iloc[0]  # Initial value of H2 storage

    
    
    # Create the Pyomo model
    model = create_RFC_modelV24(T, WS, RS, HFS, W, L, LT, WUe, RUe, HFUt, WKe, RKe, HFKt, WCAP, RCAP, HFCAP, WOP, ROP, HFOP, SCAP, SOP, r, WL, SL, RL, HFL, EtaR, Etas, EtaHF, Rmin, H_E, E_H, H_T, M, Hi, roe, A, Cp, S, Co, Ci, SKe, H2CAP, H2L)

    # Create the solver interface and solve the model
    solver = pyo.SolverFactory('gurobi')
    solver.options['mipgap'] = 0.01 #optional solver option
    solver.solve(model, tee=True) 

    txt_output_path = os.path.join(results_folder, f'{c}.txt')
    excel_output_path = os.path.join(results_folder, f'{c}_outputs.xlsx')

    # Writes outputs to text file
    with open(txt_output_path, 'w') as f:
        with redirect_stdout(f):
            # Wind turbine values
            model.nwe.pprint()
            model.cwe.pprint()
            model.we.pprint()

            # RFC values
            model.nre.pprint()
            model.cre.pprint()
            model.SoR.pprint()

            # H2 furnace values
            model.nhft.pprint()
            model.chft.pprint()
            model.hft.pprint()
        
            # Costs
            model.tc.pprint()
            model.cc.pprint()
            model.oc.pprint()
            model.wcc.pprint()
            model.rcc.pprint()
            model.hfcc.pprint()
            model.woc.pprint()
            model.roc.pprint()
            model.hfoc.pprint()
            
            # Power logic
            model.powlvl.pprint()
            model.y.pprint()

   
    # Generate excel file with results
    scalar_data = {
        'Total Cost Annual Costs ($)': (model.tc.value),
        'Total Capital Cost (CAPEX)': (model.cc.value),
        'Total Operating Cost (OPEX)': (model.oc.value),
        'H2 Furnace Capital Cost (CAPEX)': (model.hfcc.value),
        'H2 Furnace Operating Cost (OPEX)': (model.hfoc.value),
        'H2 Furnaces Built': (model.nhft.value),
        'H2 Furnace Capacity (kW)': (model.chft.value),
        'Solar Capacity (kW)': (model.sce.value),
        'Solar Capital cost (CAPEX)': (model.scc.value),
        'solar Operational Cost (OPEX)': (model.soc.value),

    }

    turbine_data = [
        {'Size': '100 kW', 'Built': model.nwe[1].value, 'Capacity (kW)': (model.cwe[1].value)},
        {'Size': '500 kW', 'Built': model.nwe[2].value, 'Capacity (kW)': (model.cwe[2].value)},
        {'Size': '800 kW', 'Built': model.nwe[3].value, 'Capacity (kW)': (model.cwe[3].value)},
        {'Size': '1500 kW', 'Built': model.nwe[4].value, 'Capacity (kW)': (model.cwe[4].value)},
    ]
    turbine_df = pd.DataFrame(turbine_data)
    turbine_df.loc['Total'] = turbine_df.sum(numeric_only=True)
    turbine_df.at['Total', 'Size'] = 'Total'

    rfc_data = [
        {'Size': '1000 kW', 'Built': model.nre[1].value, 'Capacity (kW)': (model.cre[1].value)},
        {'Size': '20000 kW', 'Built': model.nre[2].value, 'Capacity (kW)': (model.cre[2].value)},
        {'Size': '100000 kW', 'Built': model.nre[3].value, 'Capacity (kW)': (model.cre[3].value)},
    ]
    rfc_df = pd.DataFrame(rfc_data)
    rfc_df.loc['Total'] = rfc_df.sum(numeric_only=True)
    rfc_df.at['Total', 'Size'] = 'Total'

    time_series_data = {
        'Timestep': list(T),
        'State of RFC (SoR), (tH2)': [(model.SoR[t].value) for t in T],
        'RFC Power Level (powlvl), (kWh)': [model.powlvl[t].value for t in T],
        'H2 Furnace Generation (hft)': [model.hft[t].value for t in T],
        'Wind Generation (we), (kWh)': [sum(model.we[t, ws].value for ws in WS) for t in T],
        'Solar Generation, (kWh)': [model.swe[t].value for t in T],
        'RFC Binary Indicator (y)': [model.y[t].value for t in T],
        'Electric Load (L), (kWh)': [L[t] for t in T],
        'Thermal Load (LT), (kWh)': [LT[t] for t in T]
    }

    time_series_df = pd.DataFrame(time_series_data)

    with pd.ExcelWriter(excel_output_path) as writer:
        scalar_df = pd.DataFrame(list(scalar_data.items()), columns=['Parameter', 'Value'])
        scalar_df.to_excel(writer, sheet_name='Summary Scalars', index=False)
        turbine_df.to_excel(writer, sheet_name='Turbine Summary', index=False)
        rfc_df.to_excel(writer, sheet_name='RFC Summary', index=False)
        time_series_df.to_excel(writer, sheet_name='Time Series', index=False)