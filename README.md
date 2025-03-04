This repository contains the models, datesets and extended data tables for the paper "Hydrogen microgrids can facilitate the clean energy transition in remote, northern communities"

### Repository structure and contents
/Diesel - Contains the diesel microgrid model, and the input datasets. 
  - "Diesel Datasets - Final.xlsx": Community specific hourly electric and thermal load data
  - "Diesel_DataV1.xls": Input paramaters for diesel model
  - "Diesel_OptimizerV2.py": Diesel microgrid optimization model
  - "Diesel_ConcreteV1.py": Function to build diesel microgrid model, and solve for relevant communities using "CPLEX" solver. Outputs each communties results as Excel and .txt document

/RFC - Contains the wind-hydrogen microgrid model and imput datasets. 
  - \NREL_data: Contains input data when considering NREL wind capital costs
  - \conservative_data: Contains input data considering conservative northern wind capital costs.
  - "RFC Datasets - Final.xlsx": Community specific hourly input data. (electric and themral load, aswell as wind and solar resource data)
  - "RFC_ConcreteV24py": Function to build wind hydrogen microgrid model, and solve for relevant communities using "Gurobi" solver. Outputs each communties results as Excel and .txt document.
  - "RFC_optimizerV25.py": Wind hydrogen microgrid model

\SI - Contains extended data tables 
  - "SI_wind_hydrogen_microgrids.xlsx": contains results for each community for the diesle mircrogrid model, and wind hydrogen microgrid model (NREL and conservative wind cpaital cost scenarios).

