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


#Use arguement parser to handle command line arguemetns
parse = argparse.ArgumentParser()
parse.add_argument("-f", "--File", help = "Input coffea file")
args = parse.parse_args()

if __name__ == "__main__":
	coffea_file = args.File
	print("Running on input file %s")
	
	#Import coffea files with histograms
	coffea_input = util.load(coffea_file)

	#Control Structures
	hist_array = ["Muon_pt_PreTrigger","Muon_pt_Trigger","HT_PreTrigger","HT_Trigger","MHT_PreTrigger","MHT_Trigger","MET_PreTrigger","MET_Trigger"]

	hist_dict = {"Muon_pt": ["Muon_pt_PreTrigger","Muon_pt_Trigger"],
				"HT": ["HT_PreTrigger","HT_Trigger"],
				"MHT": ["MHT_PreTrigger","MHT_Trigger"],
				"MET": ["MET_PreTrigger","MET_Trigger"]
			}


	hist_name_dict = {"Muon_pt": "Muon_pT_TurnOnPlot",
				"HT": "HT_TurnOnPlot",
				"MHT": "MHT_TurnOnPlot",
				"MET": "MET_TurnOnPlot"
			}
	
	#Produce Efficency plots
	for Hist in hist_dict.keys():
		fig, ax = plt.subplots()
		print(coffea_input.keys())
		#print(type(coffea_input))
		#print(type(coffea_input["Muon_pt_Trigger"]))
		hep.histplot(coffea_input['Signal_2TeV'][hist_dict[Hist][1]]/coffea_input['Signal_2TeV'][hist_dict[Hist][0]], histtype="step", color = "k")
		plt.savefig(hist_name_dict[Hist])		
		plt.close()



