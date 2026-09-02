# BoostedHiggs4TauAnalysis
Updated analysis repo for the Boosted Higgs to 4 Tau analysis

## Installation/Setup

## Running Instructions

### Trigger Turn On Curves
**Note This code has not yet migrated to Coffea 07**
The code contained in the directory `TriggerEff/` is used to produce trigger efficiency turn on curves.
The processor can either be run offline or online.
To run the processor on HTC set the variable `run_on_condor` to `True` in the file `TriggerEff/Run_Trigger_Eff.py`.
To run the processor offline set the variable `run_on_condor` to `False`. 
~~To run the processor offline a python virtual environment must be setup on the AF due to versioning and package issues.
The instructions to set up the virtual environment provided in the **Installation/Setup** section will be sufficient to run the trigger efficiency processor offline.
To run the trigger efficiency processor (online or offline) simply run `python3 Run_Trigger_Eff.py` in the directory `TriggerEff`.
The virtual environment set up in the **Installation/Setup** section will also be sufficient to run the plotting script.~~
To produce the trigger turn on curves navigate to the directory `TriggerEff/Output_2018` and run the command `python3 Produce_TriggerTurnOnPlots.py -f "Your_Output_File.coffea"`.
The argument `"Your_Output_File.coffea"` will be a coffea file produced by the processor in the directory `Output_2018`.

### Control Plots
**These instructions are accurate but incomplete**
To produce the control plots navigate to the directory `ControlPlots` and run the runner script via `python3 Run_AnalysisSCript_4tau.py`.
This will create a coffea output file in the output directory(ies).
To produce the control plots from the coffea output navigate to the output directory and run the plotting script `PlotProducer.py`. 
The script `PlotProducer.py` requires 3 arguments to be specified: `-f` denotes the input coffea file, `-n` denotes the number of boosted taus of interest in the analysis (at the moment this should always be 4), and finally `-r` denotes the control region of interest (see control region table for list of valid inputs).
One final note; these instructions will submit jobs to HTC.
If a user wishes to run offline/interactively they should look at the "Running Offline" section for additional instructions.

*Additions ot make to these instructions*
- Section on `PlotProdcuer.py` seems adiquate
- Prior section requires more detail namely, the arguements the processor takes, the structure of the runner script

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

#### Trigger Modification
The control plot producing script allows the user to run on either one or a combination of the triggers (`Mu50` and `PFHT500_PFMHT100_PFMET100`) and their associated offline selections used in this analysis.
This behavior is controlled by an argument passed to the processor called `Trigger_Code`.
The argument `Trigger_Code` takes an integer value between 0 and 3.
When a value is unspecified the default value of `Trigger_Code` is 3.
The values of the variable `Trigger_Code` and their associated behaviors are listed in the following table.

|`Trigger_Code`  | Behavior   |
|---|---|
| 0  |  No triggers are applied |
| 1 | Only `Mu50` and associated offline selections are applied  |
| 2 | Only `PFHT500_PFMHT100_PFMET100` and associated offline selections are applied |
| 3 | Both triggers and associated offline selections are applied   |

#### Prelegacy Samples
There is a separate processor and runner pair that will produce output from the 2018 prelegacy samples the purposes of additional studies on these samples. 
To obtain the prelegacy samples simply run the runner script `Run_AnalysisScript_PreLegacy.py` via the command `python3 Run_AnalysisScript_PreLegacy.py` in the directory `ControlPlots/`.

### Cutflow Table
The output files produced by the control plot processor can be used to produce cutflow tables (tables in csv format).
To produce the cutflow table(s) navigate to the directory `ControlPlots/Output_2018MCData/` (this is the directory where the output file is saved to).
From this directory run the following command: `python3 Cutflow_Producer -f "Input_File.coffea" -n 4 -o "Out_CSV_Name"`.
The arguments required by this function are `-f` which denotes the name of the coffea file from which you wish to produce the cutflow table, `-n` which denotes the number of boosted taus in the final state (which should just be 4), and finally `-o` which denotes the name of the cutflow table cvs file. 

### Neural Network

#### Training

#### Running
