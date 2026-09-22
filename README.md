# BoostedHiggs4TauAnalysis
Updated analysis repo for the Boosted Higgs to 4 Tau analysis

## Installation/Setup
This code is designed to run on the Wisconsin Analysis Facility.
Specifically this code can run on the Coffea2026 images.
Assuming you are running on the Wisconsin Analysis Facility on one of the Coffea2026 images it should work "out of the box" with no issues.

## Running Instructions

### Trigger Turn On Curves
**Note This code has not yet migrated to Coffea26**
The code contained in the directory `TriggerEff/` is used to produce trigger efficiency turn on curves.
The processor can either be run offline or online.
To run the processor on HTC set the variable `run_on_condor` to `True` in the file `TriggerEff/Run_Trigger_Eff.py`.
To run the processor offline set the variable `run_on_condor` to `False`. 
To produce the trigger turn on curves navigate to the directory `TriggerEff/Output_2018` and run the command `python3 Produce_TriggerTurnOnPlots.py -f "Your_Output_File.coffea"`.
The argument `"Your_Output_File.coffea"` will be a coffea file produced by the processor in the directory `Output_2018`.

### Pre-Skim Scripts
This repository contains a processor + runner script that calculate the number of events within a given set of skimmed nanoAOD input files and determine the sum of genweights prior to skimming.
The script returns these outputs as `.json` files.
The content of these `.json` files will eventually be passed onto the main analysis processor for the purposes of doing the cross section luminosity weighting and to the cutflow producer script.
The repository contains copies of these files for the 2018 MC (they are `ControlPlots/numEvents_2018_With2TeVSignal_JSON.json` and `ControlPlots/genWeightSum_2018_WithQCD_JSON.json`).

#### Running Instructions
The code that produces the pre-skim count and gen weight json files is run from the `ControlPlots` directory simply via python: `python3 PreSkimWeight_Runner.py`.
The runner itself takes no command line arguments (currently).
To change the files that are run on you must modify the `file_dict` object within the runner script `ControlPlots/PreSkimWeight_Runner.py`.
To modify the names of the json files produced as outputs modify the variables `count_json_name` and `genWeight_json_name` in the runner script.

### Control Plots
The control plots used for this analysis are produced from `.coffea` files produced by the analysis processor. 
Additional files such as cutflow tables can also be produced from these `.coffea` files.
The processor also produces the `.parquet` files needed for training the neural network.

#### Coffea Processor Instructions
The first step to producing the control plots is to generate the  output `.coffea` files from the analysis processor. 
To do this navigate to the `ControlPlots` directory and run the runner script associated with the analysis processor: `python3 Run_AnalysisScript_4tau.py`.
Once run a Coffea output file will be produced in the `Output_2018MCData` directory.
Currently the runner script takes on no command line arguments and is hard coded to run on 2018 MC + data.
To change the files being run on the `file_dict` object within the runner script must be changed by the user prior to running.
The runner calls the analysis processor (`ControlPlots/Processors/FourTauAnalysisProcessor.py`) and passes several arguments to the processor. 
Those arguments are `sumWEvents_Dict`, `year`,`nBoostedTaus`, `Trigger_Code`,`Tau_WP`, and `use_DBT`. 

The argument `sumWEvents_Dict` is a dictionary that maps each process to the corresponding sum of gen weights or number of events prior to skimming for the purpose of calculating the luminosity cross section weights. 
In the runner the dictionary is read in from a `json` file on line 396, currently the runner is hard coded to read in the json file corresponding to genweights from 2018.
if the user wants to change the dictionary being read in they would change the file specified on line 396.

The argument `year` is a string corresponding to the year associated with the data and MC, currently this value defaults to `2018`.
This argument is used to control the corrections applied and it must be in agreement with the year associated with the data + MC being run on.

The argument `nBoostedTaus` tells the processor how many boosted taus to select, this number should always be 4, and if unspecified it will default to 4.

The argument `Trigger_Code` controls what trigger(s) are applied by the processor.
The specifics of this argument are discussed in the section [Trigger Modification](#Trigger Modification).

Finally I will discuss the arguments `use_DBT` and `Tau_WP` together. 
The argument `use_DBT` is a Boolean that controls whether to select boosted taus using the MVA or deep boosted tau (DBT) isolation variable, if left unspecified this argument defaults to `True`. 
If `use_DBT` is set to `False` than the MVA isolation variable is used to select the boosted taus, the value of the MVA selection used is hard coded to 0.0.
If `use_DBT` is set to `True` then the DBT isolation variable is used to select the boosted taus.
The value of the DBT that the boosted taus must pass is controlled by the floating point argument `Tau_WP`, if a value for `Tau_WP` is not passed to the processor then `Tau_WP` defaults to 0.95.

One final note; by default the runner will submit analysis jobs to HTC.
If a user wishes to run offline/interactively they should look at the [Running Offline](#Running Offline) section for additional instructions.

##### Trigger Modification
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

##### Running Offline
To run the analysis processor offline/not on HTC condor the variable `run_on_condor` in `ControlPlots/Run_AnalysisScript_4tau.py` must be set to `False`.

#### Prelegacy Samples
There is a separate processor and runner pair that will produce output from the 2018 prelegacy samples using the prelegacy analysis for the purposes of additional studies on these samples. 
To obtain a `.coffea` output file from the prelegacy samples navigate to the directory `ControlPlots` and run the command `python3 Run_AnalysisScript_PreLegacy.py`.
The `.coffea` files produced will have the same histograms and are mostly compatible with the plotting infrastructure.
The runner and processor for the prelegacy samples are similar to the runner and processor used on the UL samples, however there are some differences worth noting.
The first difference is the input files are assumed to be specific skimmed prelegacy miniAODs.
Second difference is how the number of events prior to skimming are obtained, here these are pulled directly from the skimmed miniAOD files themselves at run time and passed into the processor.
Third are the arguments the processor takes, for the prelegacy processor these arguments are `sumWEvents_Dict`, `nBoostedTaus`, `Trigger_Code`, and `year`.
These arguments are identical to their UL counter parts (see the section [Coffea Processor Instructions](#Coffea Processor Instructions)).

#### Plot Producer
To produce the control plots from the Coffea output navigate to the output directory and run the plotting script `PlotProducer.py`. 
The script `PlotProducer.py` requires 3 arguments to be specified: `-f` denotes the input Coffea file, `-n` denotes the number of boosted taus of interest in the analysis (at the moment this should always be 4), and finally `-r` denotes the control region of interest (see control region table for list of valid inputs).


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


#### Cutflow Table
The output files produced by the control plot processor can be used to produce cutflow tables (tables in csv format).
To produce the cutflow table(s) navigate to the directory `ControlPlots/Output_2018MCData/` (this is the directory where the output file is saved to).
From this directory run the following command: `python3 Cutflow_Producer -f "Input_File.coffea" -n 4 -o "Out_CSV_Name"`.
The arguments required by this function are `-f` which denotes the name of the coffea file from which you wish to produce the cutflow table, `-n` which denotes the number of boosted taus in the final state (which should just be 4), and finally `-o` which denotes the name of the cutflow table cvs file. 

### Neural Network

#### Training

#### Running
