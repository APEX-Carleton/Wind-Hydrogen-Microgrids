# RFC_ConcreteV24.py

import pyomo.environ as pyo

def create_RFC_modelV24(T, WS, RS, HFS, SLT, W, L, LT, WUe, RUe, HFUt, WKe, RKe, HFKt, WCAP, RCAP, HFCAP, WOP, ROP, HFOP, SCAP, SOP, r, WL, SL, RL, HFL, EtaR, Etas, EtaHF, Rmin, H_E, E_H, H_T, M, Hi, roe, A, Cp, S, Co, Ci, SKe, H2CAP, H2L):
    model = pyo.ConcreteModel(name="(RFC_OptimizerV24)")

    # Variables
    
   # Costs
    model.tc = pyo.Var(within=pyo.NonNegativeReals) # Total cost of microgrid
    model.cc = pyo.Var(within=pyo.NonNegativeReals) # Discounted annual capital cost for all techs
    model.wcc = pyo.Var(WS, within=pyo.NonNegativeReals) # Discounted annual wind capital investment
    model.scc = pyo.Var(within=pyo.NonNegativeReals) # Discounted annual Solar capital investment
    model.rcc = pyo.Var(RS, within=pyo.NonNegativeReals) # Discounted annual RFC investment cost
    model.hfcc = pyo.Var(within=pyo.NonNegativeReals) # Discounted annual H2 furnace investment cost
    model.h2_storage_cc = pyo.Var(within=pyo.NonNegativeReals) # Discounted annual H2 storage capital cost
    model.oc = pyo.Var(within=pyo.NonNegativeReals) # Discounted annual operating cost for all techs
    model.woc = pyo.Var(WS, within=pyo.NonNegativeReals) # Discounted annual wind operating investment
    model.soc = pyo.Var(within=pyo.NonNegativeReals) # Discounted annual Solar operating investment
    model.roc = pyo.Var(RS, within=pyo.NonNegativeReals) # Discounted annual RFC operating cost
    model.hfoc = pyo.Var(within=pyo.NonNegativeReals) # Discounted annual H2 furnace operating cost
    
    # Wind
    model.we = pyo.Var(T, WS, within=pyo.NonNegativeReals) # Generation from wind for time t for electrical
    model.nwe = pyo.Var(WS, within=pyo.NonNegativeIntegers) # Capacity investment for wind
    model.cwe = pyo.Var(WS, within=pyo.NonNegativeReals) # total capacity for wind
    
    # Solar
    model.swe = pyo.Var(T, within=pyo.NonNegativeReals) # Generation from solar for time t for electrical
    model.nse = pyo.Var(within=pyo.NonNegativeIntegers) # Number of solar units installed (each unit 10 m²)
    model.ase = pyo.Var(within=pyo.NonNegativeReals) # Total area of solar panels installed (m²)
    model.sce = pyo.Var(within=pyo.NonNegativeReals) # Rated capacity of solar panels (kW)
    
    # RFC
    model.nre = pyo.Var(RS, within=pyo.NonNegativeIntegers) # Capacity investment for RFC
    model.cre = pyo.Var(RS, within=pyo.NonNegativeReals) # total capacity for RFC
    model.SoR = pyo.Var(T, within=pyo.NonNegativeReals) # State of Charge of RFC (amount of H2 stored)

    # H2 Furnace
    model.hft = pyo.Var(T, within=pyo.NonNegativeReals) # Generation from H2 furnace for time t for thermal
    model.nhft = pyo.Var(within=pyo.NonNegativeIntegers) # Capacity investment for H2 furnace
    model.chft = pyo.Var(within=pyo.NonNegativeReals) # Total capacity for H2 furnace
    
    # Hydrogen Storage
    model.n_h2_storage = pyo.Var(within=pyo.NonNegativeIntegers) # Number of 10 kg H2 storage units
    model.max_h2_storage = pyo.Var(within=pyo.NonNegativeReals) # Maximum hydrogen storage required
    
    # Power logic
    model.powlvl = pyo.Var(T) # Tracks whether there is a deficit or surplus of energy
    model.y = pyo.Var(T, within=pyo.Binary) # If powlvl[t] > 0, y=1, else y=0
    
    # Objective function
    def obj_rule(model):
        return model.cc + model.oc
    model.obj = pyo.Objective(rule=obj_rule)

    # Constraints
      
    # Define total cost
    def tc_cost(model):
        return model.tc == model.cc + model.oc
    model.tc_costcon = pyo.Constraint(rule=tc_cost)
    
    # Define annual capital cost
    def cc_cost(model):
        return model.cc == sum(model.wcc[ws] for ws in WS) + model.scc + sum(model.rcc[rs] for rs in RS) + model.hfcc + model.h2_storage_cc
    model.cc_costcon = pyo.Constraint(rule=cc_cost)
    
    def wcc_cost(model, ws):
        return model.wcc[ws] == (WCAP[ws]) * model.cwe[ws] * ((r['Const'] * (1 + r['Const'])**WL['Const']) / (((1 + r['Const'])**WL['Const']) - 1))
    model.wcc_costcon = pyo.Constraint(WS, rule=wcc_cost)
    
    def rcc_cost(model, rs):
        return model.rcc[rs] == (RCAP[rs]) * model.cre[rs] * ((r['Const'] * (1 + r['Const'])**RL['Const']) / (((1 + r['Const'])**RL['Const']) - 1))
    model.rc_costcon = pyo.Constraint(RS, rule=rcc_cost)
    
    def hfcc_cost(model, hfs):
        return model.hfcc == (HFCAP[hfs]) * model.chft * ((r['Const'] * (1 + r['Const'])**HFL['Const']) / (((1 + r['Const'])**HFL['Const']) - 1))
    model.hfcc_costcon = pyo.Constraint(HFS, rule=hfcc_cost)

    def scc_cost(model):
        return model.scc == (SCAP[1]) * model.sce * ((r['Const'] * (1 + r['Const'])**SL['Const']) / (((1 + r['Const'])**SL['Const']) - 1))
    model.scc_costcon = pyo.Constraint(rule=scc_cost)

    def h2_storage_cc_cost(model):
        return model.h2_storage_cc == model.n_h2_storage * (H2CAP[1]) * ((r['Const'] * (1 + r['Const'])**H2L['Const']) / (((1 + r['Const'])**H2L['Const']) - 1))
    model.h2_storage_cc_con = pyo.Constraint(rule=h2_storage_cc_cost)
    
    # Define annual operating costs
    def oc_cost(model):
        return model.oc == sum(model.woc[ws] for ws in WS) + model.soc + sum(model.roc[rs] for rs in RS) + model.hfoc
    model.oc_costcon = pyo.Constraint(rule=oc_cost)
    
    def woc_cost(model, ws):
        return model.woc[ws] == (WOP[ws]) * model.cwe[ws]
    model.woc_costcon = pyo.Constraint(WS, rule=woc_cost)
    
    def roc_cost(model, rs):
        return model.roc[rs] == (ROP[rs]) * model.cre[rs]
    model.roc_costcon = pyo.Constraint(RS, rule=roc_cost)
    
    def hfoc_cost(model, hfs):
        return model.hfoc == (HFOP[hfs]) * model.chft
    model.hfoc_costcon = pyo.Constraint(HFS, rule=hfoc_cost)
    
    # Solar operating cost
    def soc_cost(model):
        return model.soc == (SOP[1]) * model.sce
    model.soc_costcon = pyo.Constraint(rule=soc_cost)
       
    # Electrical constraints   
    
    # Wind turbine
    def capacity_we1(model, ws):
        return model.cwe[ws] == model.nwe[ws] * (WUe[ws])
    model.capacity_we1con = pyo.Constraint(WS, rule=capacity_we1)

    def performance_we1(model, t, ws):
        if ws == 1 and Ci[ws] <= W[t] <= Co[ws]: # cut-in cut-out wind speeds
            return model.we[t, ws] <= 0.5 * Cp[ws] * roe['Const'] * A[ws] * (W[t]) ** 3 * model.nwe[ws]  # Power Equation
        elif ws == 2 and Ci[ws] <= W[t] <= Co[ws]:
            return model.we[t, ws] <= 0.5 * Cp[ws] * roe['Const'] * A[ws] * (W[t]) ** 3 * model.nwe[ws]
        elif ws == 3 and Ci[ws] <= W[t] <= Co[ws]:
            return model.we[t, ws] <= 0.5 * Cp[ws] * roe['Const'] * A[ws] * (W[t]) ** 3 * model.nwe[ws]
        elif ws == 4 and Ci[ws] <= W[t] <= Co[ws]:
            return model.we[t, ws] <= 0.5 * Cp[ws] * roe['Const'] * A[ws] * (W[t]) ** 3 * model.nwe[ws]
        else:
            return model.we[t, ws] == 0
    model.performance_we1con = pyo.Constraint(T, WS, rule=performance_we1)
    
    def rated_capacity_limit(model, t, ws):
        return model.we[t, ws] <= WUe[ws] * model.nwe[ws]
    model.rated_capacity_limit_con = pyo.Constraint(T, WS, rule=rated_capacity_limit)

    def capacity_check_we1(model, ws):
        return model.cwe[ws] <= WKe[ws]
    model.capcity_check_we1con = pyo.Constraint(WS, rule=capacity_check_we1)

    def capacity_check_we2(model, t, ws):
        return model.cwe[ws] >= model.we[t, ws]
    model.capacity_check_we2con = pyo.Constraint(T, WS, rule=capacity_check_we2)

                            # Solar
    def capacity_solar(model):
        return model.ase == model.nse * 10  # Each unit corresponds to 10 m²
    model.capacity_solar_con = pyo.Constraint(rule=capacity_solar)

    # Solar rated capacity
    def capacity_rated_solar(model):
        return model.sce == model.ase * 1 * Etas['Const'] # 1 kW per m² at 1000 W/m² irradiance
    model.capacity_rated_solar_con = pyo.Constraint(rule=capacity_rated_solar)

    # Solar generation constraint
    def solar_generation(model, t):
        return model.swe[t] <= S[t] * Etas['Const'] * model.ase
    model.solar_generation_con = pyo.Constraint(T, rule=solar_generation)

    # Ensure solar capacity does not exceed maximum allowed capacity
    def capacity_check_solar_max(model):
        return model.sce <= SKe[1]
    model.capacity_check_solar_max_con = pyo.Constraint(rule=capacity_check_solar_max)

    # RFC
    def capacity_re1(model, rs):
        return model.cre[rs] == model.nre[rs] * (RUe[rs])
    model.capacity_re1con = pyo.Constraint(RS, rule=capacity_re1)

    def capacity_check_re1(model, t):
        return sum(model.cre[rs] for rs in RS) >= model.powlvl[t]
    model.capacity_check_re1con = pyo.Constraint(T, rule=capacity_check_re1)
    
    def capacity_check_re2(model, rs):
        return model.cre[rs] <= RKe[rs]
    model.capcity_check_re2con = pyo.Constraint(RS, rule=capacity_check_re2)

    # Track maximum hydrogen storage
    def track_max_h2_storage(model, t):
        return model.max_h2_storage >= model.SoR[t]
    model.track_max_h2_storage_con = pyo.Constraint(T, rule=track_max_h2_storage)
    
    # Linear reformulation without the ceil function
    def max_h2_storage_increments_lower(model):
        return model.n_h2_storage * 10 >= model.max_h2_storage
    model.max_h2_storage_increments_lower_con = pyo.Constraint(rule=max_h2_storage_increments_lower)

    def max_h2_storage_increments_upper(model):
        return model.n_h2_storage * 10 <= model.max_h2_storage + 10
    model.max_h2_storage_increments_upper_con = pyo.Constraint(rule=max_h2_storage_increments_upper)

    def RFC_state(model, t): 
        if t > 0:
            return model.SoR[t] == model.SoR[t-1] + ((model.powlvl[t] * EtaR['Const'] * (H_E['Const'])) * model.y[t]) + ((model.powlvl[t] * EtaR['Const'] * (E_H['Const'])) * (1 - model.y[t])) - (((LT[t]) * (H_T['Const'])) / EtaHF['Const'])
        else:
            return model.SoR[t] == (Hi) + ((model.powlvl[t] * EtaR['Const'] * (H_E['Const'])) * model.y[t]) + ((model.powlvl[t] * EtaR['Const'] * (E_H['Const'])) * (1 - model.y[t])) - (((LT[t]) * (H_T['Const'])) / EtaHF['Const'])
    model.RFC_statecon = pyo.Constraint(T, rule=RFC_state)
    
    def RFC_state2(model):
        return model.SoR[8759] == (Hi)
    model.RFC_statcon = pyo.Constraint(rule=RFC_state2)
    
    def RFC_energy1(model, t):
        return model.SoR[t] >= Rmin['Const']
    model.RFC_energy1con = pyo.Constraint(T, rule=RFC_energy1)
    
    # Thermal constraints   
    
    # H2 furnace
    def capacity_hft1(model, hfs):
        return model.chft == model.nhft * (HFUt[hfs])
    model.capacity_hft1con = pyo.Constraint(HFS, rule=capacity_hft1)
    
    def performance_hft1(model, t):
        return model.hft[t] == (LT[t])
    model.performance_hft1con = pyo.Constraint(T, rule=performance_hft1)
    
    def capacity_check_hft1(model, hfs):
        return model.chft <= HFKt[hfs]
    model.capacity_check_hft1con = pyo.Constraint(HFS, rule=capacity_check_hft1)
    
    def capacity_check_hft2(model, t):
        return model.chft >= model.hft[t]
    model.capacity_check_hft2con = pyo.Constraint(T, rule=capacity_check_hft2)
    
    # Microgrid power logic
    def pow_logic1(model, t):
        return model.powlvl[t] == sum(model.we[t, ws] for ws in WS) + model.swe[t] - (L[t])
    model.pow_logic1con = pyo.Constraint(T, rule=pow_logic1)
    
    def pow_logic2(model, t):
        return model.powlvl[t] <= M['Const'] * model.y[t]
    model.pow_logic2con = pyo.Constraint(T, rule=pow_logic2)
    
    def pow_logic3(model, t):
        return model.powlvl[t] >= M['Const'] * (model.y[t] - 1)
    model.pow_logic3con = pyo.Constraint(T, rule=pow_logic3)

    return model
