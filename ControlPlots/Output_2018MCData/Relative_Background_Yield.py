import coffea
import awkward as ak
import numpy as np
import matplotlib.pyplot as plt
from coffea import util
import hist
import csv
import sys
import argparse

#Use arguement parser to handle command line arguemetns
parse = argparse.ArgumentParser()
parse.add_argument("-f", "--File", help = "Input coffea file")
args = parse.parse_args()

#Process array
proc_arr = [r"$t\bar{t}$",r"Drell-Yan+Jets","Di-Bosons","Single Top","W+Jets",r"$ZZ \rightarrow 4l$"]

#Drell Yan Arra
DY_Arr = ["DYJetsToLL_M-4to50_HT-70to100","DYJetsToLL_M-4to50_HT-100to200","DYJetsToLL_M-4to50_HT-200to400","DYJetsToLL_M-4to50_HT-400to600",
		"DYJetsToLL_M-4to50_HT-600toInf","DYJetsToLL_M-50_HT-70to100","DYJetsToLL_M-50_HT-100to200","DYJetsToLL_M-50_HT-200to400",
		"DYJetsToLL_M-50_HT-400to600","DYJetsToLL_M-50_HT-600to800","DYJetsToLL_M-50_HT-800to1200","DYJetsToLL_M-50_HT-1200to2500","DYJetsToLL_M-50_HT-2500toInf"]
	
#Background names to samples dictionary
background_dict = {r"$t\bar{t}$" : ["TTToSemiLeptonic","TTTo2L2Nu","TTToHadronic"], r"$t\bar{t}$ Hadronic" : ["TTToHadronic"], 
		r"$t\bar{t}$ Semileptonic" : ["TTToSemiLeptonic"], r"$t\bar{t}$ 2L2Nu" : ["TTTo2L2Nu"],
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
}

def sample_yield(sample, total_yield, coffea_input):
	return coffea_input[sample]["Event_Count"]/total_yield

def process_yield(process, total_yield, coffea_input):
	rel_yield = 0
	for sample in background_dict[process]:
		rel_yield += coffea_input[sample]["Event_Count"]/total_yield
	return rel_yield 

def total_yield(coffea_input):
	total_yield = 0
	for process in proc_arr:
		for sample in background_dict[process]:
			total_yield += coffea_input[sample]["Event_Count"]

	return total_yield


if __name__ == "__main__":
	#Import coffea files with histograms
	coffea_file = args.File
	coffea_input = util.load(coffea_file)

	#Obtain the total yield
	total_yield = total_yield(coffea_input)

	#For each process get the relative yield
	print("Working in file " + str(coffea_file))
	for process in proc_arr:
		print("Relative yield of " + str(process) + ": %.4f"%process_yield(process,total_yield,coffea_input))
	
#	for sample in DY_Arr:
#		print("Relative yield of " + str(sample) + ": %.4f"%sample_yield(sample,total_yield,coffea_input))

	#Verify that this code is working by verifying the sum of all processes is 1
#	check_sum = 0
#	for process in proc_arr:
#		check_sum += process_yield(process,total_yield,coffea_input)
#	
#	if (check_sum == 1):
#		print("Code works")
#	else:
#		print("Code is not working")
#		print("Check sum = %.4f"%check_sum)



