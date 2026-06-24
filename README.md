# BoostedHiggs4TauAnalysis
Updated analysis repo for the Boosted Higgs to 4 Tau analysis

## Installation/Setup

### Python Virtual Environnement for Plotting
Due to how the AF works, in order to run the plotting script a python virtual environment must be set up so that a more recent version of the package mplhep can be used. 

To set up the virtual environment for plotting navigate to the directory `ControlPlots/`
In the analysis facility create a shallow virtual environment by running the command:
`new-af-venv PlottingEnv`
Start up the environment via `source PlottingEnv/bin/activate` and run the following command:
```
pip install --force-reinstall -v "mplhep==1.1.0"
```
Then install version 1.24.0 of numpy in the environment using the following command:
```
pip install --force-reinstall -v "numpy==1.24.0"
```

All plotting scripts can only be run from the virtual environment due to the current mismatch in mplhep versions.

## Running Instructions

### Control Plots
To produce the control plots navigate to the directory `ControlPlots` and run the runner script via `python3 Run_AnalysisSCript_4tau.py`.
This will create a coffea output file in the output directory(ies).
To produce the control plots from the coffea output navigate to the output directory and run the plotting script `PlotProducer.py`. 
The script `PlotProducer.py` requires 3 arguments to be specified; `-f` denotes the input coffea, `-n` denotes the number of boosted taus of interest in the analysis (this should always be 4), and finally `-r` denotes the control region of interest (see control region table for arguments).

**Control Region Arguments**
| `-r`  | Region  |
|---|---|
| `All`  | No Control Region  |
|  `ZCR` | Z Control Region  |
|  `TCR` |  Top Control Region |
|  `FakeCR` | Fake Control Region |
| `TightTCR` | Tight Top Control Region |
| `LooseTCR` | Loose Top Control Region |
| `NotTCR` | Not Top Control Region |
| `NotZCR` | Not Z Control Region | 


