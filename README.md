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

### Setup for Running Control Plot Processor Offline
Due to versioning issues on the Wisconsin AF the control plot processor can only be run offline (not on HTC) in a python virtual environment. 
This environment can be the same virtual environment that is set up for the plotting scripts or it can be in a new virtual environment.
In either case the following commands must be run in the virtual environment to handle the version discrepancies:
```
pip install --force-reinstall -v "setuptools==53.0.0"
```

## Running Instructions

### Trigger Turn On Curves
The code contained in the directory `TriggerEff/` is used to produce trigger efficiency turn on curves.
The processor can either be run offline or online.
To run the processor on HTC set the variable `run_on_condor` to `True` in the file `TriggerEff/Run_Trigger_Eff.py`.
To run the processor offline set the variable `run_on_condor` to `False`. 
To run the processor offline a python virtual environment must be setup on the AF due to versioning and package issues.
The instructions to set up the virtual environment provided in the **Installation/Setup** section will be sufficient to run the trigger efficiency processor offline.
To run the trigger efficiency processor (online or offline) simply run `python3 Run_Trigger_Eff.py` in the directory `TriggerEff`.
The virtual environment set up in the **Installation/Setup** section will also be sufficient to run the plotting script.
To produce the trigger turn on curves navigate to the directory `TriggerEff/Output_2018` and run the command `python3 Produce_TriggerTurnOnPlots.py -f "Your_Output_File.coffea"`.
The argument `"Your_Output_File.coffea"` will be a coffea file produced by the processor in the directory `Output_2018`.

### Control Plots
To produce the control plots navigate to the directory `ControlPlots` and run the runner script via `python3 Run_AnalysisSCript_4tau.py`.
This will create a coffea output file in the output directory(ies).
To produce the control plots from the coffea output navigate to the output directory and run the plotting script `PlotProducer.py`. 
The script `PlotProducer.py` requires 3 arguments to be specified: `-f` denotes the input coffea file, `-n` denotes the number of boosted taus of interest in the analysis (at the moment this should always be 4), and finally `-r` denotes the control region of interest (see control region table for list of valid inputs).
One final note; these instructions will submit jobs to HTC.
If a user wishes to run offline/interactively they should look at the "Running Offline" section for additional instructions.

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


#### Running Offline
To run the coffea processor offline/not on HTC condor the variable `run_on_condor` in `ControlPlots/Run_AnalysisScript_4tau.py` must be set to `False`.
To run the control plot processor offline one must be in a virtual environment on the Wisconsin AF due to versioning issues, to see what specific packages and versions need to be installed see the installation section of the README.
When in the appropriate virtual environment and with the change to `run_on_condor` made the processor is run via the python runner script `python3 Run_AnalysisSCript_4tau.py`.

#### Trigger Modification
The control plot producing script allows the user to run on either one or a combination of the triggers (`Mu50` and `PFHT500_PFMHT100_PFMET100`) and their associated offline selections used in this analysis.
This behavior is controlled by an argument passed to the processor called `Trigger_Code`.
The argument `Trigger_Code` takes an integer $n \in \mathbb{Z}_4$. 
When a value is unspecified the default value of `Trigger_Code` is 3.
The values of the variable `Trigger_Code` and their associated behaviors are listed in the following table.

|`Trigger_Code`  | Behavior   |
|---|---|
| 0  |  No triggers are applied |
| 1 | Only `Mu50` and associated offline selections are applied  |
| 2 | Only `PFHT500_PFMHT100_PFMET100` and associated offline selections are applied |
| 3 | Both triggers and associated offline selections are applied   |

### Neural Network

#### Training

#### Running
