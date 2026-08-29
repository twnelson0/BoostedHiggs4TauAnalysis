import awkward as ak
import uproot
import hist
from hist import intervals
import matplotlib.pyplot as plt
import numpy as np
import mplhep as hep
from coffea import processor, nanoevents
from coffea.nanoevents import BaseSchema
from coffea import util
from math import pi
import numba 
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import os
import time
import datetime
from distributed import Client
from dask_jobqueue import HTCondorCluster
import csv
import glob
import json
from Processors import PreLegacyAnalysisProcessor as AnalysisProcessor
import Corrections
#import Data
import cowtools.jobqueue
import cloudpickle
import argparse

#import warnings
#warnings.filterwarnings("error")


#X509 function (for HTC)
def move_X509():
	try:
		_x509_localpath = (
			[
				line
				for line in os.popen("voms-proxy-info").read().split("\n")
				if line.startswith("path")
			][0]
			.split(":")[-1]
			.strip()
		)
	except Exception as err:
		raise RuntimeError(
			"x509 proxy could not be parsed, try creating it with 'voms-proxy-init'"
		) from err
	_x509_path = f'/scratch/{os.environ["USER"]}/{_x509_localpath.split("/")[-1]}'
	os.system(f"cp {_x509_localpath} {_x509_path}")
	return os.path.basename(_x509_localpath)

#Command line arguements
#parse = argparse.ArgumentParser()
#parse.add_argument("-HTC","--RunOnHTC", nargs="?", const = 1, help = "Run on HTC")

if __name__ == "__main__":
	#Condor related stuff
	run_on_condor = True
	os.environ["CONDOR_CONFIG"] = "/etc/condor/condor_config"
	
	if (run_on_condor):
		print("Run on Condor")
		#Xrootd setup
		_x509_path = move_X509()
		print(f"x509 path: {_x509_path}")
		htc_log_err_dir = "/scratch/twnelson/ControlPlot_HTC/Run_" + str(time.localtime()[0]) + "_" + str(time.localtime()[1]) + "_" + str(time.localtime()[2]) + "_" + str(time.localtime()[3]) + f".{time.localtime()[4]:02d}"
		os.makedirs(htc_log_err_dir)

		cluster = HTCondorCluster(
				cores=1,
				memory="6 GB",
				disk="4 GB",
				death_timeout = '60',
				#python = "/usr/local/bin/python3",
				job_extra_directives={
					"+JobFlavour": '"tomorrow"',
					"log": "dask_job_output.$(PROCESS).$(CLUSTER).log",
					"output": "dask_job_output.$(PROCESS).$(CLUSTER).out",
					"error": "dask_job_output.$(PROCESS).$(CLUSTER).err",
					"should_transfer_files": "yes",
					"when_to_transfer_ouput": "ON_EXIT_OR_EVICT",
					"transfer_executable": "false",
					"Requirements": "HasSingularityJobStart",
					"container_image": "/cvmfs/unpacked.cern.ch/registry.hub.docker.com/coffeateam/coffea-dask-almalinux9:2026.4.0-py3.12",
					"InitialDir": f'/scratch/{os.environ["USER"]}',
					'transfer_input_files': f'{os.environ["PWD"]}, {_x509_path}',

				},
				job_script_prologue = [
					"export XRD_RUNFORKHANDLER=1",
					f"export X509_USER_PROXY={_x509_path}",
				]
		)
		cluster.adapt(minimum=1, maximum=500)

	#	cluster = cowtools.jobqueue.GetCondorClient(
	#					memory = "4 GB",
	#					disk = "2 GB",
	#					max_workers=500,
	#					container_image = "/cvmfs/unpacked.cern.ch/registry.hub.docker.com/coffeateam/coffea-dask-cc7:latest-py3.10"
	#				)

		runner = processor.Runner(
			executor = processor.DaskExecutor(client=Client(cluster),status=False),
			#executor = processor.DaskExecutor(client=cluster,status=False),
			schema=BaseSchema,
			skipbadfiles=True,
			xrootdtimeout=1000,
			#chunksize=500000,
			#maxchunks = 1
		)

		#Pass modules to HTC
		cloudpickle.register_pickle_by_value(AnalysisProcessor)
		cloudpickle.register_pickle_by_value(Corrections)
		#cloudpickle.register_pickle_by_value(Data)
		#cloudpickle.register_pickle_by_value(Corrections.kFactor)
		#cloudpickle.register_pickle_by_value(Corrections.PU_Reweighting)
	
	else: #Iterative runner
		print("Run Iteratively")
		runner = processor.Runner(executor = processor.IterativeExecutor(), schema=BaseSchema)

	#Diretory for files
	Skimmed_4tau_base_MC = "root://cmsxrootd.hep.wisc.edu//store/user/twnelson/HH4Tau_EtAl/Skimmed_Files/2018/MC/"
	Skimmed_4tau_base_Data = "root://cmsxrootd.hep.wisc.edu//store/user/twnelson/HH4Tau_EtAl/Skimmed_Files/2018/Data/"
	Skimmed_4tau_loc_Data = "/hdfs/store/user/twnelson/HH4Tau_EtAl/Skimmed_Files/2018/Data/"
	Skimmed_4tau_loc_MC = "/hdfs/store/user/twnelson/HH4Tau_EtAl/Skimmed_Files/2018/MC/"

	signal_base = "root://cmseos.fnal.gov//store/user/abdollah/SkimBoostedHH4t/2018/4t/v2_Hadd/GluGluToRadionToHHTo4T_M-"
	background_base = "root://cmseos.fnal.gov//store/user/abdollah/SkimBoostedHH4t/2018/4t/v2_Hadd/"	
	data_loc = "root://cmseos.fnal.gov//store/user/abdollah/SkimBoostedHH4t/2018/4t/v2_Hadd/"

	file_dict_full = {
		"TTToSemiLeptonic": [background_base + "TTToSemiLeptonic.root"], "TTTo2L2Nu": [background_base + "TTTo2L2Nu.root"], "TTToHadronic": [background_base + "TTToHadronic.root"],
		"ZZ4l": [background_base + "ZZ4l.root"],
		"VV2l2nu" : [background_base + "VV2l2nu.root"],
		"WZ1l3nu" : [background_base + "WZ1l3nu.root"],
		"WZ3l1nu" : [background_base + "WZ3l1nu.root"],
		"ZZ2l2q" : [background_base + "ZZ2l2q.root"],
		"WZ2l2q" : [background_base + "WZ2l2q.root"],
		"WZ1l1nu2q" : [background_base + "WZ1l1nu2q.root"],
		"DYJetsToLL_Pt-50To100": [background_base + "DYJetsToLL_Pt-50To100.root"] ,
		"DYJetsToLL_Pt-100To250": [ background_base + "DYJetsToLL_Pt-100To250.root"],
		"DYJetsToLL_Pt-250To400": [ background_base + "DYJetsToLL_Pt-250To400.root"],
		"DYJetsToLL_Pt-400To650": [ background_base + "DYJetsToLL_Pt-400To650.root"],
		"DYJetsToLL_Pt-650ToInf": [background_base + "DYJetsToLL_Pt-650ToInf.root"],
		"Tbar-tchan" : [background_base + "Tbar-tchan.root"],
		"T-tchan" : [background_base + "T-tchan.root"],
		"Tbar-tW" : [background_base + "Tbar-tW.root"],
		"T-tW" : [background_base + "T-tW.root"],
		"WJetsToLNu_HT-100To200" : [background_base + "WJetsToLNu_HT-100To200.root"],
		"WJetsToLNu_HT-200To400" : [background_base + "WJetsToLNu_HT-200To400.root"],
		"WJetsToLNu_HT-400To600" : [background_base + "WJetsToLNu_HT-400To600.root"],
		"WJetsToLNu_HT-600To800" : [background_base + "WJetsToLNu_HT-600To800.root"],
		"WJetsToLNu_HT-800To1200" : [background_base + "WJetsToLNu_HT-800To1200.root"],
		"WJetsToLNu_HT-1200To2500" : [background_base + "WJetsToLNu_HT-1200To2500.root"],
		"WJetsToLNu_HT-2500ToInf" : [background_base + "WJetsToLNu_HT-2500ToInf.root"],
		"Signal": [signal_base + "2000.root"],
		"Data_SingleMuon": [data_loc + "SingleMu_Run2018A.root", data_loc + "SingleMu_Run2018B.root", data_loc + "SingleMu_Run2018C.root", data_loc + "SingleMu_Run2018D.root"],
		"Data_JetHT": [data_loc + "JetHT_Run2018A-17Sep2018-v1.root", data_loc + "JetHT_Run2018B-17Sep2018-v1.root", data_loc + "JetHT_Run2018C-17Sep2018-v1.root",data_loc + "JetHT_Run2018D-PromptReco-v2.root"]
	}

	N_PreSkim_Dict = dict.fromkeys(file_dict_full.keys())
	del N_PreSkim_Dict["Data_SingleMuon"]
	del N_PreSkim_Dict["Data_JetHT"]
    

	#SingleMu_2018A_Debug = np.random.choice(SingleMu_2018A_Debug, 10)

	#print(SingleMu_2018A_Debug)
	#Arrays of Signal
	#Signal_Base = "/hdfs/store/user/abdollah/RadionHH4tau_UL_Nov2025/"
	#HH_4Tau_2018_Signal = glob.glob()
	
	#Set file dictionary and list of backgrounds prior to running processor
	#file_dict = file_dict_data_test
	file_dict = file_dict_full
	#file_dict = file_dict_prob
	
	#file_dict = file_dict_signal_only
	#file_dict = file_dict_data_only
	#file_dict = file_dict_MC_only
	#file_dict = file_dict_test
	#file_dict = file_dict_data_mc_mix
	#file_dict = file_dict_ZZ4L_Only
	#file_dict = file_dict_Test_Reweighting


	#Pull in the weight and event count prior to skimming information
	#with open("genWeightSum_JSON.json") as json_file:
	#with open("genWeightSum_2018_WithQCD_JSON.json") as json_file:
	#	sumWEvents_Dict = json.load(json_file)

#	with open("numEvents_JSON.json") as json_file:
#		numEvents_Dict = json.load(json_file)
	
	trigger_bit_dict = {0:"NoTrigger",1:"SingleMuonTrigger",2:"HTMETMHTTrigger",3:"BothTriggers"}

	for process in N_PreSkim_Dict.keys():
		temp_file = uproot.open(file_dict[process][0])
		N_PreSkim_Dict[process] = temp_file['hcount'].member('fEntries')/2

	
	for n_taus in range(4,5):
		for trigger_bit in range(3,4):
			print("About to run processor")
			start_time = time.time()
			if (run_on_condor):
				print(f"https://cms02.hep.wisc.edu:8009/user/{os.environ['USER']}/{cluster.dashboard_link}")
			fourtau_out = runner(file_dict, treename="4tau_tree", processor_instance=AnalysisProcessor.Analysis4TauProcessor(sumWEvents_Dict = N_PreSkim_Dict, nBoostedTaus = n_taus, Trigger_Code = trigger_bit)) #Modified for NanoAOD (changd treename)
			end_time = time.time()
			time_running = end_time-start_time
			print("It takes about %.1f s to run the coffea processor with %d boosted tau selections"%(time_running,n_taus))
			
			#Save coffea file
			#outfile = os.path.join(os.getcwd() + "/Output_2018MCData/", f"output_{n_taus}_boosted_tau_selec_4TauSamples_VlooseWP_NoISO.coffea")
			#outfile = os.path.join(os.getcwd() + "/Output_2018MCData/", f"output_{n_taus}_boosted_tau_selec_4TauSamples_tightWP_p95_SignalNoSkim_FixedSignalWeight.coffea")
			#outfile = os.path.join(os.getcwd() + "/Output_2018MCData/", f"output_{n_taus}_boosted_tau_selec_4TauSamples_tightWP_p95_Signal_" + trigger_bit_dict[trigger_bit]	+ "_Test.coffea")
			outfile = os.path.join(os.getcwd() + "/Output_2018MCData/", f"output_{n_taus}_boosted_tau_selec_4TauSamples_PreLegacy_" + trigger_bit_dict[trigger_bit]	+ "_Coffea2026.coffea")
			#outfile = os.path.join(os.getcwd() + "/Output_2018MCData/", f"DummyTest_" + trigger_bit_dict[trigger_bit]	+ ".coffea")
			util.save(fourtau_out, outfile)
			print(f"Saved output to {outfile}")	
