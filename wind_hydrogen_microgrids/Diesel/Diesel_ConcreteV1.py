# Diesel_ConcreteV1.py
import pyomo.environ as pyo

def create_Diesel_modelV1(T, GS, DFS, L, LT, GUe, DFUt, GKe, DFKt, GCAP, DFCAP, GOP, DFOP, DOP, r, GL, DFL, EtaG, EtaDF, D_E, D_T):
    model = pyo.ConcreteModel(name="(Diesel_OptimizerV1)")


    #Variables
    #Costs
    model.tc = pyo.Var(within=pyo.NonNegativeReals) #Total cost of microgrid
    model.cc = pyo.Var(within=pyo.NonNegativeReals) #Discounted annual capital cost for all technolgies 
    model.gcc = pyo.Var(GS, within=pyo.NonNegativeReals) #Discounted annual diesel generator capital investment
    model.dfcc = pyo.Var(within=pyo.NonNegativeReals) #Discounted annual diesel furnace  capital investment
    model.oc = pyo.Var(within=pyo.NonNegativeReals) #Discounted annual operating cost
    model.goc = pyo.Var(GS, within=pyo.NonNegativeReals) #Discounted annual diesel generator operating cost
    model.dfoc = pyo.Var(within=pyo.NonNegativeReals) #Discounted annual diesel furnace operating cost
    
    #Genset
    model.ge = pyo.Var(T, GS, within=pyo.NonNegativeReals) #Generation from genset for time t for electrical load
    model.nge = pyo.Var(GS, within=pyo.NonNegativeIntegers) #Number of diesel generator units
    model.cge = pyo.Var(GS, within=pyo.NonNegativeReals) #total capacity for diesel generator
    model.gf = pyo.Var(within=pyo.NonNegativeReals) #annual fuel consumption of genset in litres
    
    #Diesel furnace
    model.dft = pyo.Var(T, within=pyo.NonNegativeReals) #Generation from diesel furnace for time t for thermal load
    model.ndft = pyo.Var(within=pyo.NonNegativeIntegers) #Number of units for diesel furnace
    model.cdft = pyo.Var(within=pyo.NonNegativeReals) #total capacity for diesel furnace
    model.dff = pyo.Var(within=pyo.NonNegativeReals) #annual fuel consumption of diesel furnace in liters
    
    
    #Objective function
    def obj_rule(model):
        return model.cc + model.oc
    model.obj = pyo.Objective(rule=obj_rule)


    #Constraints
    #Define total cost
    def tc_cost(model):
        return model.tc == model.cc + model.oc
    model.tc_costcon = pyo.Constraint(rule=tc_cost)
    
    #Define annual captial cost
    def cc_cost(model):
        return model.cc == sum(model.gcc[gs] for gs in GS)  + model.dfcc
    model.cc_costcon = pyo.Constraint(rule=cc_cost)
    
    def gcc_cost(model, gs):
        return model.gcc[gs] == (GCAP[gs]) * model.cge[gs] * ((r['Const'] * (1 + r['Const'])**GL['Const']) / (((1 + r['Const'])**GL['Const']) - 1))
    model.gcc_costcon = pyo.Constraint(GS, rule=gcc_cost)
    
    def dfcc_cost(model, dfs):
        return model.dfcc == (DFCAP[dfs]) * model.cdft * ((r['Const'] * (1 + r['Const'])**DFL['Const']) / (((1 + r['Const'])**DFL['Const']) - 1))
    model.dfcc_costcon = pyo.Constraint(DFS, rule=dfcc_cost)
    
    #Define annual operating costs
    def oc_cost(model):
        return model.oc == sum(model.goc[gs] for gs in GS) + model.dfoc + ((model.gf + model.dff) * DOP[1])
    model.oc_costcon = pyo.Constraint(rule=oc_cost)
    
    def goc_cost(model, gs):
        return model.goc[gs] == (GOP[gs]) * model.cge[gs]
    model.goc_costcon = pyo.Constraint(GS, rule=goc_cost)
    
    def dfoc_cost(model, dfs):
        return model.dfoc == (DFOP[dfs]) * model.cdft
    model.dfoc_costcon = pyo.Constraint(DFS, rule=dfoc_cost)
       
    
    #Electrical constraints   
    #Genset
    def capacity_ge1(model, gs):
        return model.cge[gs] == model.nge[gs] * (GUe[gs])
    model.capacity_ge1con = pyo.Constraint(GS,rule=capacity_ge1)

    def performance_ge1(model, t):
        return sum(model.ge[t, gs] for gs in GS) >= L[t]
    model.performance_ge1con = pyo.Constraint(T, rule=performance_ge1)
    
    def capacity_check_ge1(model, gs):
        return model.cge[gs] <= GKe[gs]
    model.capcity_check_ge1con = pyo.Constraint(GS, rule=capacity_check_ge1)

    def capacity_check_ge2(model, t, gs):
        return model.cge[gs] >= model.ge[t, gs]
    model.capacity_check_ge2con = pyo.Constraint(T, GS, rule=capacity_check_ge2)
    
    def gfuel(model):
        return model.gf == (sum(model.ge[t, gs] for t in T for gs in GS) * D_E['Const'] / EtaG['Const'] )
    model.gfuelcon = pyo.Constraint(rule=gfuel)
    
    
    #Thermal constraints   
    #Diesel furnace
    def capacity_dft1(model, dfs):
        return model.cdft == model.ndft * (DFUt[dfs])
    model.capacity_dft1con = pyo.Constraint(DFS, rule=capacity_dft1)
    
    def performance_dft1(model, t):
        return model.dft[t] == (LT[t])
    model.performance_dft1con = pyo.Constraint(T, rule=performance_dft1)
    
    def capacity_check_dft1(model, dfs):
        return model.cdft <= DFKt[dfs]
    model.capacity_check_dft1con = pyo.Constraint(DFS, rule=capacity_check_dft1)
    
    def capacity_check_dft2(model, t):
        return model.cdft >= model.dft[t]
    model.capacity_check_dft2con = pyo.Constraint(T, rule=capacity_check_dft2)
    
    def dffuel(model):
        return model.dff == (sum(model.dft[t] for t in T) * D_T['Const'] / EtaDF['Const']) 
    model.dffuelcon = pyo.Constraint(rule=dffuel)
    
    return model
