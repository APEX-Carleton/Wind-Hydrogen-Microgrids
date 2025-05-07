import pandas as pd
import pyomo.environ as pyo
from collections import ChainMap
from Diesel_ConcreteV1 import create_Diesel_modelV1
from contextlib import redirect_stdout
import openpyxl

# Sets
T = range(0, 8759)  # Time period {0,...,8759}
GS = [1, 2, 3, 4]  #Sizes of diesel genset {1=100kW, 2=500kW, 3=1000kW, 4=2000kW}
DFS = [1]  # Sizes of Diesel furnace {1=17.58kW}
C = ['Francois', 'Beaver Creek', 'Wrigley', 'Tsiigehtchic', 'Resolute Bay', 'Aupaluk', 'Old Crow', 
'Peawanuck', 'Tadoule Lake', 'Kwadacha', 'Makkovik', 'Port Hope Simpson', 'Umiujaq', 'Ramea', 
'Whati', 'Brochet', 'Fort Good Hope', 'Kingfisher Lake', 'Old Masset', 'Port Clements', 
'Keewaywin', 'Fort McPherson', 'Kangiqsujuaq', 'Watson Lake', 'Fort Chipewyan', 
'Arctic Bay', 'Weagamow Lake', 'Natuashish', 'Kangiqsualujjuaq', 'Naujaat', 'Fort Simpson', 
'Shamattawa', 'Pond Inlet', 'Inukjuak', 'Kuujjuaq', 'Rankin Inlet', 'Iqaluit']

# Read the data from Excel using Pandas
df2 = pd.read_excel('Diesel_DataV1.xls', 'Unit Size', header=0, index_col=0)
df3 = pd.read_excel('Diesel_DataV1.xls', 'Max Cap', header=0, index_col=0)
df5 = pd.read_excel('Diesel_DataV1.xls', 'Costs', header=0, index_col=0)
df6 = pd.read_excel('Diesel_DataV1.xls', 'Constants', header=0, index_col=0)

# Define data
GUe_temp = pd.DataFrame(df2['GUe']).to_dict()  # Unit size for each genset (kW)
GUe = dict(ChainMap(*GUe_temp.values()))
DFUt_temp = pd.DataFrame(df2['DFUt']).to_dict()  # Unit size for each diesel furnace (kW)
DFUt = dict(ChainMap(*DFUt_temp.values()))
GKe_temp = pd.DataFrame(df3['GKe']).to_dict()  # Max electrical capacity for each genset size (kW)
GKe = dict(ChainMap(*GKe_temp.values()))
DFKt_temp = pd.DataFrame(df3['DFKt']).to_dict()  # Max thermal capacity for each diesel furnace size (kW)
DFKt = dict(ChainMap(*DFKt_temp.values()))
GCAP_temp = pd.DataFrame(df5['GCAP']).to_dict()  # CAPEX for each genset size ($/kW)
GCAP = dict(ChainMap(*GCAP_temp.values()))
DFCAP_temp = pd.DataFrame(df5['DFCAP']).to_dict()  # CAPEX for each diesel furnace ($/kW)
DFCAP = dict(ChainMap(*DFCAP_temp.values()))
GOP_temp = pd.DataFrame(df5['GOP']).to_dict()  # OPEX for each genset size ($/kW)
GOP = dict(ChainMap(*GOP_temp.values()))
DFOP_temp = pd.DataFrame(df5['DFOP']).to_dict()  # OPEX for each diesel furnace size ($/kW)
DFOP = dict(ChainMap(*DFOP_temp.values()))
DOP_temp = pd.DataFrame(df5['DOP']).to_dict()  # OPEX for each diesel furnace size ($/kW)
DOP = dict(ChainMap(*DOP_temp.values()))
r_temp = pd.DataFrame(df6['r']).to_dict()  # Discount rate
r = dict(ChainMap(*r_temp.values()))
Tau_temp = pd.DataFrame(df6['Tau']).to_dict()  # Discount rate
Tau = dict(ChainMap(*Tau_temp.values()))
GL_temp = pd.DataFrame(df6['GL']).to_dict()  # Lifetime of genset
GL = dict(ChainMap(*GL_temp.values()))
DFL_temp = pd.DataFrame(df6['DFL']).to_dict()  # Lifetime of diesel furnace
DFL = dict(ChainMap(*DFL_temp.values()))
EtaG_temp = pd.DataFrame(df6['EtaG']).to_dict()  # Efficiency of genset
EtaG = dict(ChainMap(*EtaG_temp.values()))
EtaDF_temp = pd.DataFrame(df6['EtaDF']).to_dict()  # Efficiency of diesel furnace
EtaDF = dict(ChainMap(*EtaDF_temp.values()))
D_E_temp = pd.DataFrame(df6['D_E']).to_dict()  # Conversion of diesel to electrical energy(kWh/L)
D_E = dict(ChainMap(*D_E_temp.values()))
D_T_temp = pd.DataFrame(df6['D_T']).to_dict()  # Conversion of diesel to thermal energy (kWh/L)
D_T = dict(ChainMap(*D_T_temp.values()))

# Run model for all models in set C
for c in C:
    # Define location specific data file
    df1 = pd.read_excel('RFC Datasets - Final.xlsx', c, header=0)

    # Define location specific data
    L_temp = pd.DataFrame(df1['L']).to_dict()  # Electric load (kW)
    L = dict(ChainMap(*L_temp.values()))
    LT_temp = pd.DataFrame(df1['Lt']).to_dict()  # Thermal load (kW)
    LT = dict(ChainMap(*LT_temp.values()))
    
    # Create the Pyomo model
    model = create_Diesel_modelV1(T, GS, DFS, L, LT, GUe, DFUt, GKe, DFKt, GCAP, DFCAP, GOP, DFOP,DOP, r, GL, DFL, EtaG, EtaDF, D_E, D_T)

    # Create the solver interface and solve the model using CPLEX
    solver = pyo.SolverFactory('cplex_direct')
    solver.solve(model, tee=True)

     # Writes outputs to text file
    with open(c + '.txt', 'w') as f:
        with redirect_stdout(f):
            # Genset values
            model.nge.pprint()
            model.cge.pprint()
            model.ge.pprint()
            model.gf.pprint()

            # Diesel furnace values
            model.ndft.pprint()
            model.cdft.pprint()
            model.dft.pprint()
            model.dff.pprint()
        
            # Costs
            model.tc.pprint()
            model.cc.pprint()
            model.oc.pprint()
            model.gcc.pprint()
            model.dfcc.pprint()
            model.goc.pprint()
            model.dfoc.pprint()

    #writes output to excel file
    # Extract scalar data
    scalar_data = {
        'Total Cost ($)': pyo.value(model.tc),
        'Capital Cost (CAPEX)': pyo.value(model.cc),
        'Operating Cost (OPEX)': pyo.value(model.oc),
        'Annual Fuel Consumption Genset (L)': pyo.value(model.gf),
        'Annual Fuel Consumption Diesel Furnace (L)': pyo.value(model.dff),
    }

    # Creating tables for generators and diesel furnaces
    generator_data = [
        {'Size': '100 kW', 'Built': model.nge[1].value, 'Capacity (kW)': model.cge[1].value, 'Capital Cost ($)': pyo.value(model.gcc[1]), 'Operating Cost ($)': pyo.value(model.goc[1])},
        {'Size': '500 kW', 'Built': model.nge[2].value, 'Capacity (kW)': model.cge[2].value, 'Capital Cost ($)': pyo.value(model.gcc[2]), 'Operating Cost ($)': pyo.value(model.goc[2])},
        {'Size': '1000 kW', 'Built': model.nge[3].value, 'Capacity (kW)': model.cge[3].value, 'Capital Cost ($)': pyo.value(model.gcc[3]), 'Operating Cost ($)': pyo.value(model.goc[3])},
        {'Size': '2000 kW', 'Built': model.nge[4].value, 'Capacity (kW)': model.cge[4].value, 'Capital Cost ($)': pyo.value(model.gcc[4]), 'Operating Cost ($)': pyo.value(model.goc[4])},
    ]
    generator_df = pd.DataFrame(generator_data)
    generator_df.loc['Total'] = generator_df.sum(numeric_only=True)
    generator_df.at['Total', 'Size'] = 'Total'

    diesel_furnace_data = [
        {'Size': '17.58 kW', 'Built': pyo.value(model.ndft), 'Capacity (MW)': pyo.value(model.cdft), 'Capital Cost ($)': pyo.value(model.dfcc), 'Operating Cost ($)': pyo.value(model.dfoc)},
    ]
    diesel_furnace_df = pd.DataFrame(diesel_furnace_data)
    diesel_furnace_df.loc['Total'] = diesel_furnace_df.sum(numeric_only=True)
    diesel_furnace_df.at['Total', 'Size'] = 'Total'

    # Capturing time-dependent data
    time_series_data = {
        'Time': list(T),
        'Electric Load (kW)': [L[t] for t in T],
        'Thermal Load (kW)': [LT[t] for t in T],
        'Diesel Generation (kW)': [sum(pyo.value(model.ge[t, gs]) for gs in GS) for t in T],
        'Thermal Generation (kW)': [pyo.value(model.dft[t]) for t in T]
    }

    time_series_df = pd.DataFrame(time_series_data)

    # Write solution to Excel file
    with pd.ExcelWriter(f"{c}_solution.xlsx", engine="openpyxl") as writer:
        scalar_df = pd.DataFrame(list(scalar_data.items()), columns=['Parameter', 'Value'])
        scalar_df.to_excel(writer, sheet_name='Summary Scalars', index=False)
        generator_df.to_excel(writer, sheet_name='Generator Summary', index=False)
        diesel_furnace_df.to_excel(writer, sheet_name='Diesel Furnace Summary', index=False)
        time_series_df.to_excel(writer, sheet_name='Time Series', index=False)
