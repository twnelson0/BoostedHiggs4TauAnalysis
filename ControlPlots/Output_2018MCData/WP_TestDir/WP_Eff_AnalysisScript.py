import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob
import csv

def get_selec_eff(input_file, process):
	csv_frame = pd.read_csv(input_file)
	skim_count = csv_frame[csv_frame["Sample"] == process]["SkimOnly"]
	selec_count = csv_frame[csv_frame["Sample"] == process]["Higgs_dR"]

	return selec_count/skim_count



if __name__ == "__main__":
	tauWP = np.linspace(start=0.85,stop=0.95,num=11)		
	
	#Round the entries for ease of working with them
	for i in range(len(tauWP)):
		tauWP[i] = round(tauWP[i],2)
	
	#Set up working point file dictionary
	file_wp_dict = dict.fromkeys(tauWP)

	for wp in tauWP:
		wp_str = str(wp)[2:]
		if (len(wp_str) == 1):
			wp_str = wp_str + "0"
		wp_str = "p" + wp_str
		file_wp_dict[wp] = glob.glob("Cutflow_Table_WP_" + wp_str + "_DBT.csv")[0]
	
	#Obtain the skimming effiences
	ZZ4l_SelecEff = np.array([])
	Signal_SelecEff = np.array([])
	for wp in tauWP:
		print(file_wp_dict[wp])
		ZZ4l_SelecEff = np.append(ZZ4l_SelecEff,get_selec_eff(file_wp_dict[wp], "ZZ4l"))
		Signal_SelecEff = np.append(Signal_SelecEff,get_selec_eff(file_wp_dict[wp], "Signal_2TeV"))

	#Plot the efficiencies
	fig, ax_ZZ4l = plt.subplots()
	ax_ZZ4l.plot(tauWP,ZZ4l_SelecEff,'ko', markersize = 7)
	ax_ZZ4l.set(xlabel="Deep Boosted Tau Working Point", ylabel = r"$\epsilon_{\text{Selection}}$", title = r"$ZZ \rightarrow 4l$ Selection Efficiency")
	plt.savefig("ZZ4l_SelecEff_DBT.png")
	
	fig, ax_Signal = plt.subplots()
	ax_Signal.plot(tauWP,Signal_SelecEff,'ko', markersize = 7)
	ax_Signal.set(xlabel="Deep Boosted Tau Working Point", ylabel = r"$\epsilon_{\text{Selection}}$", title = r"$X \rightarrow HH \rightarrow 4\tau$ Selection Efficiency")
	plt.savefig("Signal_SelecEff_DBT.png")
	


