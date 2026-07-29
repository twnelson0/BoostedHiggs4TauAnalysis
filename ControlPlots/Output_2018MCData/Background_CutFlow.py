import uproot
import hist
from hist import intervals
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import mplhep as hep
from coffea import processor, nanoevents
from coffea.nanoevents.methods import candidate, vector
from coffea import util
from math import pi
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import vector
import os
import time
import datetime
import csv
import sys
import argparse
import itertools
import json

#Plot style variables defined
hep.style.use(hep.style.CMS)
#cmap = mpl.colormaps['PiYG'] 
#cmap = mpl.colormaps['plasma'] 
cmap = mpl.colormaps['hsv'] 

#Collection of color maps
cmap0 = mpl.colormaps['Reds']
cmap1 = mpl.colormaps['Greens']
cmap2 = mpl.colormaps['Blues']
cmap3 = mpl.colormaps['Oranges']
cmap4 = mpl.colormaps['Greys']
cmap5 = mpl.colormaps['Purples']
cmap_array = [cmap0,cmap1,cmap2,cmap3,cmap4,cmap5]

TABLEAU_COLORS = ['blue','orange','green','red','purple','brown','pink','gray','olive','cyan']

#Control Region dictionary
region_dict = {"All": "NoControlRegion",
			"ZCR": "ZControlRegion",
			"NotZCR": "NoZRegion",
			"TCR": "TopControlRegion",
			"NotTCR": "NotTopControlRegion",
			"TightTCR": "TightTopControlRegion",
			"LooseTCR": "LooseTopControlRegion",
			"FakeCR": "FakeControlRegion",
		}

#Use arguement parser to handle command line arguemetns
parse = argparse.ArgumentParser()
parse.add_argument("-f", "--File", help = "Input coffea file")
parse.add_argument("-n", "--NumberTau", help = "Number of boosted taus in selection")
args = parse.parse_args()

if __name__ == "__main__":
	print("Running on file " + args.File)

	cutflow_csv_bool = True

	coffea_file = args.File

	#Dictionaries and arrays with information on plot constrution, naming and samples
	four_tau_hist_list = [
			"boostedtau_pt_Trigg","boostedtau_eta_Trigg","boostedtau_phi_Trigg",
			"electron_pt_Trigg","electron_eta_Trigg","electron_phi_Trigg",
			"muon_pt_Trigg","muon_eta_Trigg","muon_phi_Trigg", #"Leadingmuon_pt_Trigg",#"Leadingmuon_eta_Trigg",
			"Jet_pt_Trigg","Jet_eta_Trigg","Jet_phi_Trigg",
			"AK8Jet_pt_Trigg","AK8Jet_eta_Trigg","AK8Jet_phi_Trigg","nAK8Jet_Trigg",
			"MET","HT","MHT", #, "Mini_Cutflow", "Mini_NMinus1"
			"ZMult", "bJetMult",
			"LeadingPair_dR", "NextLeadingPair_dR", "FourTauMass"
			]

	#Additional boosted tau distributions to pull based on boosted tau requirements
	add_var = []
	n_tau = int(args.NumberTau)
	if (n_tau == 1):
		print("One Boosted tau required")
		add_var = ["Leadingboostedtau_pt_Trigg"]
	if (n_tau == 2):
		print("Two Boosted taus required")
		add_var = ["Leadingboostedtau_pt_Trigg", "Subleadingboostedtau_pt_Trigg"]
	if (n_tau == 3):
		print("Three Boosted taus required")
		add_var = ["Leadingboostedtau_pt_Trigg", "Subleadingboostedtau_pt_Trigg","Thirdleadingboostedtau_pt_Trigg"]
	if (n_tau == 4):
		print("Four Boosted taus required")
		add_var = ["Leadingboostedtau_pt_Trigg", "Subleadingboostedtau_pt_Trigg","Thirdleadingboostedtau_pt_Trigg","Fourthleadingboostedtau_pt_Trigg"]

	four_tau_hist_list = add_var + four_tau_hist_list
	
	background_list_full = [r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$","Signal"]
	background_list_fullQCD = [r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$","QCD"]
	background_list_test = [r"$ZZ \rightarrow 4l$"]
	background_list_none = []
	background_list = background_list_full
	background_plot_names = {r"$t\bar{t}$" : "_ttbar_", r"$t\bar{t}$ Hadronic" : "_ttbarHadronic_", r"$t\bar{t}$ Semileptonic" : "_ttbarSemilepton_",
			r"$t\bar{t}$ 2L2Nu" : "_ttbar2L2Nu_", r"Drell-Yan+Jets": "_DYJets_", "Di-Bosons" : "_DiBosons_", "Single Top": "_SingleTop_", "QCD" : "_QCD_", 
			"W+Jets" : "_WJets_", r"$ZZ \rightarrow 4l$" : "_ZZ4l_", r"$ZZ \rightarrow 4l$ Test": "_ZZ4lTest_", r"$ZZ \rightarrow 4l$ Control": "_ZZ4lControl_",
			"W+Jets HT 70-100 GeV" : "_WJetsHT70-100_","W+Jets HT 100-200 GeV" : "_WJetsHT100-200_","W+Jets HT 200-400 GeV" : "_WJetsHT200-400_",
			"W+Jets HT 400-600 GeV" : "_WJetsHT400-600_","W+Jets HT 600-800 GeV" : "_WJetsHT600-800_","W+Jets HT 800-1200 GeV" : "_WJetsHT800-1200_",
			"W+Jets HT 1200-2500 GeV" : "_WJetsHT1200-2500_","W+Jets HT 2500-Inf GeV" : "_WJetsHT2500-Inf_"} #For file names
	
	#Background names to samples dictionary
	background_dict = {r"$t\bar{t}$" : ["TTToSemiLeptonic","TTTo2L2Nu","TTToHadronic"], 
			r"$t\bar{t}$ Hadronic" : ["TTToHadronic"], r"$t\bar{t}$ Semileptonic" : ["TTToSemiLeptonic"], r"$t\bar{t}$ 2L2Nu" : ["TTTo2L2Nu"],
			r"Drell-Yan+Jets": ["DYJetsToLL_M-4to50_HT-70to100","DYJetsToLL_M-4to50_HT-100to200","DYJetsToLL_M-4to50_HT-200to400","DYJetsToLL_M-4to50_HT-400to600",
			"DYJetsToLL_M-4to50_HT-600toInf","DYJetsToLL_M-50_HT-70to100","DYJetsToLL_M-50_HT-100to200","DYJetsToLL_M-50_HT-200to400",
			"DYJetsToLL_M-50_HT-400to600","DYJetsToLL_M-50_HT-600to800","DYJetsToLL_M-50_HT-800to1200","DYJetsToLL_M-50_HT-1200to2500","DYJetsToLL_M-50_HT-2500toInf"], 
			"Di-Bosons": ["WZ2l2q","WZ1l1nu2q","ZZ2l2q", "WZ1l3nu", "VV2l2nu", "WWTo1L1Nu2Q", "WWTo4Q", "ZZTo4Q", "ZZTo2L2Nu", "ZZTo2Nu2Q"], 
			"Single Top": ["Tbar-tchan","T-tchan","Tbar-tW","T-tW","ST_s-channel_4f_leptonDecays", "ST_s-channel_4f_hadronicDecays"], 
			"W+Jets": ["WJetsToLNu_HT-70To100","WJetsToLNu_HT-100To200","WJetsToLNu_HT-200To400","WJetsToLNu_HT-400To600","WJetsToLNu_HT-600To800","WJetsToLNu_HT-800To1200","WJetsToLNu_HT-1200To2500","WJetsToLNu_HT-2500ToInf"],
			"W+Jets HT 100-200 GeV": ["WJetsToLNu_HT-100To200"],"W+Jets HT 200-400 GeV": ["WJetsToLNu_HT-200To400"],"W+Jets HT 400-600 GeV": ["WJetsToLNu_HT-400To600"],
			"W+Jets HT 600-800 GeV": ["WJetsToLNu_HT-600To800"],"W+Jets HT 800-1200 GeV": ["WJetsToLNu_HT-800To1200"],
			"W+Jets HT 1200-2500 GeV": ["WJetsToLNu_HT-1200To2500"], "W+Jets HT 2500-Inf GeV": ["WJetsToLNu_HT-2500ToInf"],
			r"$ZZ \rightarrow 4l$" : ["ZZ4l"],
			"QCD": ["QCD_HT50to100","QCD_HT100to200","QCD_HT200to300","QCD_HT300to500","QCD_HT500to700","QCD_HT700to1000","QCD_HT1000to1500","QCD_HT1500to2000","QCD_HT2000toInf"],
			"Signal": ["Signal_2TeV"],
	}

	all_sample_array = []
	for background in background_list:
		print(background_dict[background])
		all_sample_array.append(background_dict[background])
	
	#Import coffea files with histograms
	coffea_input = util.load(coffea_file)

	#Produce csv table
	if (cutflow_csv_bool):
		table_keys = ["Sample","SkimOnly","Trigger", "LeadingBoostedTau","SubleadingBoostedTau","3rdLeadingBoostedTau","4thLeadingBoostedTau","VisMassSelec","Higgs_dR"]
		table_array = []
	#	var_dict = {
	#			"SkimOnly": "n_Skim" ,"Trigger" : "n_Trigger", "LeadingBoostedTau": "n_LeadBoostedTau","SubleadingBoostedTau": "n_SubLeadBoostedTau",
	#			"3rdLeadingBoostedTau": "n_3rdLeadBoostedTau","4thLeadingBoostedTau": "n_4thLeadBoostedTau","VisMassSelec": "n_VisMass","Higgs_dR" : "n_Higgs_dR"
	#		}
		var_dict = {
				"SkimOnly": "w_Skim" ,"Trigger" : "w_Trigger", "LeadingBoostedTau": "w_LeadBoostedTau","SubleadingBoostedTau": "w_SubLeadBoostedTau",
				"3rdLeadingBoostedTau": "w_3rdLeadBoostedTau","4thLeadingBoostedTau": "w_4thLeadBoostedTau","VisMassSelec": "w_VisMass","Higgs_dR" : "w_Higgs_dR"
			}
		#table_dict["Sample"] = ["Muon Data Set","HT Data Set", "Both Sets of Data"]
		samples = ["TTToSemiLeptonic","TTTo2L2Nu","TTToHadronic","DYJetsToLL_M-4to50_HT-70to100","DYJetsToLL_M-4to50_HT-100to200","DYJetsToLL_M-4to50_HT-200to400",
				"DYJetsToLL_M-4to50_HT-400to600","DYJetsToLL_M-4to50_HT-600toInf","DYJetsToLL_M-50_HT-70to100","DYJetsToLL_M-50_HT-100to200","DYJetsToLL_M-50_HT-200to400",
				"DYJetsToLL_M-50_HT-400to600","DYJetsToLL_M-50_HT-600to800","DYJetsToLL_M-50_HT-800to1200","DYJetsToLL_M-50_HT-1200to2500","DYJetsToLL_M-50_HT-2500toInf",
				"ZZ4l","WZ2l2q","WZ1l1nu2q","ZZ2l2q", "WZ1l3nu", "VV2l2nu", "WWTo1L1Nu2Q", "WWTo4Q", "ZZTo4Q", "ZZTo2L2Nu", "ZZTo2Nu2Q","Tbar-tchan","T-tchan","Tbar-tW","T-tW",
				"ST_s-channel_4f_leptonDecays", "ST_s-channel_4f_hadronicDecays","WJetsToLNu_HT-70To100","WJetsToLNu_HT-100To200","WJetsToLNu_HT-200To400","WJetsToLNu_HT-400To600",
				"WJetsToLNu_HT-600To800","WJetsToLNu_HT-800To1200","WJetsToLNu_HT-1200To2500","WJetsToLNu_HT-2500ToInf","Signal_2TeV","Data_Mu","Data_HT"]
       
		with open("../numEvents_JSON.json") as json_file:
			pre_skim_dict = json.load(json_file)
		#pre_skim_dict = json.loads("../numEvents_JSON.json")
		#print(pre_skim_dict)
		
		for sample in samples:
			table_dict = dict.fromkeys(["Sample","SkimOnly","Trigger", "LeadingBoostedTau","SubleadingBoostedTau","3rdLeadingBoostedTau","4thLeadingBoostedTau","VisMassSelec","Higgs_dR"])
			table_dict["Sample"] = sample
			#print(pre_skim_dict[sample])
			all_labels = list(var_dict.keys())
			#all_labels.append("PreSkim") 
			for key in all_labels:
				#if (key == "PreSkim"):
				#	table_dict[key] = pre_skim_dict[sample]
				#else:
				table_dict[key] = coffea_input[sample][var_dict[key]]
			table_array.append(table_dict)

		with open("NanoAOD_UL_DeepTau_DataMC_Cutflow_Weights_Tightp95Cut_WSignal_Fixed.csv", "w", newline="") as f:
			w = csv.DictWriter(f,table_keys)
			w.writeheader()
			w.writerows(table_array)




