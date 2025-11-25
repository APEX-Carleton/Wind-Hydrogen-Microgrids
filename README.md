This repository contains the models, datasets, and result tables for the paper "Hydrogen microgrids can facilitate the clean energy transition in remote, northern communities"

### Repository structure and contents
/Diesel - Contains the diesel microgrid model and the input datasets. 
  - "Diesel Datasets - Final.xlsx": Community-specific hourly electric and thermal load data.
  - "Diesel_DataV1.xls": Input paramaters for diesel model.
  - "Diesel_OptimizerV2.py": Builds diesel microgrid model, and solves for relevant communities using "CPLEX" solver.
  - "Diesel_ConcreteV1.py": Diesel microgrid optimization model.
  - "Diesel_Results": Folder containing results for each community.

/RFC - Contains the hydrogen microgrid model and input datasets. 
  - "RFC Datasets - Final.xlsx": Community-specific hourly input data. (electric and thermal load, as well as wind and solar resource data).
  - "RFC_ConcreteV24py": Hydrogen microgrid model.
  - "RFC_optimizerV25.py": Builds wind hydrogen microgrid model, and solves for relevant communities using "Gurobi" solver.
  \NREL
    - "RFC_DataV24.xls": Contains input data when considering NREL wind capital costs.
    - \Results_NREL: Folder containing results for each community when considering NREL wind capital costs.
  \Conservative
    - "RFC_DataV24_WC: Contains input data considering conservative northern wind capital costs.
    - \Conservative_results: Folder containing results for each community when considering conservative wind capital costs.

  \Data shared with the research team under a non-disclosure agreement have been removed.
