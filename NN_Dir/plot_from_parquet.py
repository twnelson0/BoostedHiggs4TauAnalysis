import pandas as pd
import numpy as np
from math import pi
import awkward as ak
import mplhep as hep
import matplotlib.pyplot as plt
import hist
import os

hep.style.use(hep.style.CMS)
TABLEAU_COLORS = ['blue','orange','green','red','purple','brown','pink','gray','olive','cyan']

#Produce stacked histogram
def StackPlot(signal_array,signal_list,background_array,background_list,data_hist,plot_name,axis_label,data_blind = False):
	if (data_blind):
		fig, ax_main, ax_comp = hep.comp.data_model(
			data_hist = data_hist,
			blind = (0,3000),
			stacked_components = background_array[:len(background_array)],
			stacked_labels = background_list[:len(background_list)],
			stacked_colors = TABLEAU_COLORS[:len(background_list)],
			xlabel = axis_label,
			model_uncertainty=True,
			comparison = "ratio",
			markersize = 20,
			flow = "sum",
		)
		xlabel = ax_main.set_xlabel(axis_label)
		
		#Stupid solution to make the points thicker (draw a copy of the data ontop of the previously produced ratio plot with thicker points)
		hep.histplot(data_hist, blind = (0,3000), ax=ax_main, histtype="errorbar",markersize=20, yerr=True, color = "k") 
		
		#Add signal
		color_list = ['cyan', 'red', 'purple']
		for i_mass in range(3):
			hep.histplot(signal_array[i_mass], ax=ax_main, color = color_list[i_mass], linewidth = 3.2, label = signal_list[i_mass], histtype = "step")
		#Add backgrounds again (if blinding only)
		for i in range(len(background_array)):
			hep.histplot(background_array[i], ax=ax_main, color = TABLEAU_COLORS[i], histtype= "fill")
		
		#Text, scaling and saving the plot
		ax_main.legend(fontsize = 14)
		hep.yscale_legend(ax_main,soft_fail=True)
	#	if (axis_label == r"Z-Boson Multiplicity" or axis_label == r"b-Jet Multiplicity"):
	#		print("Log Scale")
	#		ax_main.set_yscale('log')
		hep.cms.label(data=True, ax = ax_main, text = "2018 Data Preliminary")	
		plt.savefig(plot_name)
		plt.close()
	else:
		fig, ax_main, ax_comp = hep.comp.data_model(
			data_hist = data_hist,
			stacked_components = background_array[:len(background_array)],
			stacked_labels = background_list[:len(background_list)],
			stacked_colors = TABLEAU_COLORS[:len(background_list)],
			xlabel = axis_label,
			model_uncertainty=True,
			comparison = "ratio",
			markersize = 20,
			flow = "sum",
		)
		xlabel = ax_main.set_xlabel(axis_label)
		
		#Stupid solution to make the points thicker (draw a copy of the data ontop of the previously produced ratio plot with thicker points)
		hep.histplot(data_hist, ax=ax_main, histtype="errorbar",markersize=20, yerr=True, color = "k") 
		
		#Add signal
		color_list = ['cyan', 'red', 'purple']
		for i_mass in range(3):
			hep.histplot(signal_array[i_mass], ax=ax_main, color = color_list[i_mass], linewidth = 3.2, label = signal_list[i_mass], histtype = "step")
		
		#Text, scaling and saving the plot
		ax_main.legend(fontsize = 14)
		hep.yscale_legend(ax_main,soft_fail=True)
	#	if (axis_label == r"Z-Boson Multiplicity" or axis_label == r"b-Jet Multiplicity"):
	#		print("Log Scale")
	#		ax_main.set_yscale('log')
		hep.cms.label(data=True, ax = ax_main, text = "2018 Data Preliminary")	
		plt.savefig(plot_name)
		plt.close()

if __name__ == "__main__":
	#mass = "2000"
	#mass_array = ["1000","2000","3000"]
	mass_array = ["1","2","3"]
	#region_array = ["All","ZCR","TCR","FakeCR","LowPurity","HighPurity"] 
	region_array = ["HighPurity"] 
	
	#for mass in mass_array:
	for region_name in region_array:
		print(region_name)
		#Neural Network Varaibles
		var_array = ["radion_pt","vis_mass","vis_mass2","radion_eta","higgs1_dr","higgs2_dr","dphi_H1","dphi_H2",
				"dphi_H1_MET","dphi_H2_MET","dr_HH","dphi_HH","dr_H1_Rad","dr_H2_Rad","dphi_rad_MET","H1OS","H2OS","numBJet","predictions","ZMult","RecoRadion_Mass"] #,"weight","predictions"]
		
		#Variables for plotting
		dict_plot_names = {"radion_pt": "radion_pT_AllMass_EitherOr_Trigger","vis_mass": "LeadingHiggs_AllMass_EitherOr_Trigger",
				"vis_mass2": "SubLeadingHiggs_AllMass_EitherOr_Trigger", "radion_eta": "Radion_eta_AllMass_EitherOr_Trigger", 
				"higgs1_dr": "leading_diTau_DeltaR_AllMass_EitherOr_Trigger", "higgs2_dr": "subleading_diTau_DeltaR_AllMass_EitherOr_Trigger",
				"dphi_H1": "LeadingdiTau_DeltaPhi_AllMass_EitherOr_Trigger", "dphi_H2": "SubleadingdiTau_DeltaPhi_AllMass_EitherOr_Trigger",
				"dphi_H1_MET": "LeadingHiggs_MET_DeltaPhi_AllMass_EitherOr_Trigger", "dphi_H2_MET": "SubleadingHiggs_MET_DeltaPhi_AllMass_EitherOr_Trigger",
				"dr_HH": "Higgs_DeltaR_AllMass_EitherOr_Trigger", "dphi_HH": "HiggsDeltaPhi_AllMass_EitherOr_Trigger" ,"dr_H1_Rad": "LeadingHiggs_Radion_DeltaR_AllMass_EitherOr_Trigger",
				"dr_H2_Rad": "SubLeadingHiggs_Radion_DeltaR_AllMass_EitherOr_Trigger", "dphi_rad_MET": "Radion_MET_DeltaPhi_AllMass_EitherOr_Trigger",
				"H1OS":"LeadingHiggs_Charge_AllMass_EitherOr_Trigger","H2OS": "SubleadingHiggs_Charge_AllMass_EitherOr_Trigger", "numBJet": "BJetMult_AllAllMass_EitherOr_Trigger", 
				"predictions": "NeuralNetwork_Prediction_AllMass_EitherOr_Trigger", "ZMult": "ZMult_AllMass_EitherOr_Trigger", 
				"RecoRadion_Mass": "RecoRadion_AllMass_EitherOr_Trigger"}
		
		dict_axis_names = {"radion_pt": r"Radion $p_T$ (GeV)","vis_mass": r"Leading Di-Boosted $\tau$ mass (GeV)",
				"vis_mass2": r"Next Leading Di-Boosted $\tau$ mass (GeV)", "radion_eta": r"Radion $\eta$", 
				"higgs1_dr": r"Leading Di-Boosted $\tau$ $\Delta R$", "higgs2_dr": r"Next Leading Di-Boosted $\tau$ $\Delta R$",
				"dphi_H1": r"Leading Di-Boosted $\tau$ $\Delta \phi$", "dphi_H2": r"Next Leading Di-Boosted $\tau$ $\Delta \phi$",
				"dphi_H1_MET": r"Leading Higgs MET $\Delta \phi$", "dphi_H2_MET": r"Next Leading Higgs MET $\Delta \phi$",
				"dr_HH": r"Di-Higgs $\Delta R$", "dphi_HH": r"Di-Higgs $\Delta \phi$" ,"dr_H1_Rad": r"Leading Higgs Radion $\Delta R$",
				"dr_H2_Rad": r"Next Leading Higgs Radion $\Delta R$", "dphi_rad_MET": r"",
				"H1OS": r"Leading Di-Boosted $\tau$ Charge","H2OS": r"Next Leading Di-Boosted $\tau$ Charge", "numBJet": r"b-Jet Multiplicity", 
				"predictions": r"Neural Network Score", "ZMult": r"Z-Boson Multiplicity", 
				"RecoRadion_Mass": r"Radion Mass (GeV)"}
		
		data_files = ["Data_HT","Data_Mu"]
		signal_file = ["Signal"]
		background_list = [r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$","QCD"]
		signal_list = [r"MC Sample $m_\phi$ = 1 TeV",r"MC Sample $m_\phi$ = 2 TeV",r"MC Sample $m_\phi$ = 3 TeV"]
		background_plot_names = {r"$t\bar{t}$" : "_ttbar_", r"Drell-Yan+Jets": "_DYJets_", "Di-Bosons" : "_DiBosons_", "Single Top": "_SingleTop+", "QCD" : "_QCD_", "W+Jets" : "_WJets_", r"$ZZ \rightarrow 4l$" : "_ZZ4l_"}
		background_dict = {r"$t\bar{t}$" : ["TTToSemiLeptonic","TTTo2L2Nu","TTToHadronic"], 
					r"Drell-Yan+Jets": ["DYJetsToLL_M-4to50_HT-70to100","DYJetsToLL_M-4to50_HT-100to200","DYJetsToLL_M-4to50_HT-200to400","DYJetsToLL_M-4to50_HT-400to600","DYJetsToLL_M-4to50_HT-600toInf","DYJetsToLL_M-50_HT-70to100","DYJetsToLL_M-50_HT-100to200","DYJetsToLL_M-50_HT-200to400","DYJetsToLL_M-50_HT-400to600","DYJetsToLL_M-50_HT-600to800","DYJetsToLL_M-50_HT-800to1200","DYJetsToLL_M-50_HT-1200to2500","DYJetsToLL_M-50_HT-2500toInf"],
					"Di-Bosons": ["ZZTo2L2Nu","ZZTo2Nu2Q","VV2l2nu","ZZTo4Q" ,"WWTo1L1Nu2Q","WWTo4Q","WZ1l3nu","ZZ2l2q","WZ2l2q","WZ1l1nu2q"],
					"Single Top": ["T-tchan","Tbar-tchan","T-tW","Tbar-tW","ST_s-channel_4f_hadronicDecays","ST_s-channel_4f_leptonDecays"],
					"QCD": ["QCD_HT50to100","QCD_HT100to200","QCD_HT200to300","QCD_HT300to500","QCD_HT500to700","QCD_HT700to1000","QCD_HT1000to1500","QCD_HT1500to2000","QCD_HT2000toInf"],
					"W+Jets": ["WJetsToLNu_HT-70To100","WJetsToLNu_HT-100To200","WJetsToLNu_HT-200To400","WJetsToLNu_HT-400To600","WJetsToLNu_HT-600To800","WJetsToLNu_HT-800To1200","WJetsToLNu_HT-1200To2500","WJetsToLNu_HT-2500ToInf"],
					r"$ZZ \rightarrow 4l$" : ["ZZ4l"]
				}
		
		#Import data, background and signal
		background_input_dict = {}
		Null_Backgrounds = []
		for background_type in background_dict:
			non_files_array = []
			for background in background_dict[background_type]:
				if not(os.path.isfile(background + "with_predictions.parquet")):
					print(background)
					non_files_array.append(background)
					continue
				background_input_dict[background] = pd.read_parquet(background + "with_predictions.parquet",engine="pyarrow")
			
			#Remove empty backgrounds
			if (non_files_array == background_dict[background_type]):
				Null_Backgrounds.append(background_type)
			else:
				for background in non_files_array:
					background_dict[background_type].remove(background)

		for background_type in Null_Backgrounds:
			del background_dict[background_type]
			background_list.remove(background_type)


		signal_input_dict = {}
		for mass in mass_array:
			signal_input_dict[mass] = pd.read_parquet("Signal_" + mass + "TeVwith_predictions.parquet",engine="pyarrow")

		data_input_dict = {}
		for data_file in data_files:
			data_input_dict[data_file] = pd.read_parquet(data_file + "with_predictions.parquet",engine="pyarrow")

		#Histogram binning
		N1 = 10
		N_fourMass = 15
		N2 = 8


		#Histogram dictionaries
		hist_dict_background = {
				"radion_pt": hist.Hist.new.StrCat([r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$"],name="background").Reg(N1,0,500, label=r"Radion $p_T$ (GeV)").Weight(), 
				"vis_mass": hist.Hist.new.StrCat([r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$"],name="background").Reg(N2,0,120, label=r"Leading di-$\tau$ Mass (GeV)").Weight(),
				"vis_mass2": hist.Hist.new.StrCat([r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$"],name="background").Reg(N2,0,120, label=r"Subleading di-$\tau$ Mass (GeV)").Weight(),
				"radion_eta": hist.Hist.new.StrCat([r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$"],name="background").Reg(N1,-5,5, label = r"Radion $\eta$").Weight(),
				"higgs1_dr": hist.Hist.new.StrCat([r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$"],name="background").Reg(N1,0,5, label = r"Leading di-$\tau$ $\Delta$R").Weight(),
				"higgs2_dr": hist.Hist.new.StrCat([r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$"],name="background").Reg(N1,0,5, label = r"Subleading di-$\tau$ $\Delta$R").Weight(),
				"dphi_H1": hist.Hist.new.StrCat([r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$"],name="background").Reg(N1,-pi,pi, label = r"Subleading di-$\tau$ $\Delta \phi$").Weight(),
				"dphi_H2": hist.Hist.new.StrCat([r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$"],name="background").Reg(N1,-pi,pi, label = r"Leading di-$\tau$ $\Delta \phi$").Weight(),
				"dphi_H1_MET": hist.Hist.new.StrCat([r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$"],name="background").Reg(N1,-pi,pi, label = r"Leading Higgs MET $\Delta \phi$").Weight(),
				"dphi_H2_MET": hist.Hist.new.StrCat([r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$"],name="background").Reg(N1,-pi,pi, label = r"Subleading Higgs MET $\Delta \phi$").Weight() ,
				"dr_HH": hist.Hist.new.StrCat([r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$"],name="background").Reg(N1,0,5, label = r"Higgs $\Delta$R").Weight(),
				"dphi_HH": hist.Hist.new.StrCat([r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$"],name="background").Reg(N1,-pi,pi, label = r"Higgs $\Delta \phi$").Weight(),
				"dr_H1_Rad": hist.Hist.new.StrCat([r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$"],name="background").Reg(N1,0,5, label = r"Leading Higgs Radion $\Delta$R").Weight(),
				"dr_H2_Rad": hist.Hist.new.StrCat([r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$"],name="background").Reg(N1,0,5, label = r"Subleading Higgs Radion $\Delta$R").Weight(),
				"dphi_rad_MET": hist.Hist.new.StrCat([r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$"],name="background").Reg(N1,-pi,pi, label = r"Radion MET $\Delta \phi$").Weight(),
				"H1OS": hist.Hist.new.StrCat([r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$"],name = "background").Reg(11,-5,5,label = r"Leading Higgs Electric Charge").Weight(),
				"H2OS": hist.Hist.new.StrCat([r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$"],name = "background").Reg(11,-5,5,label = r"Subleading Higgs Electric Charge").Weight(),
				"numBJet": hist.Hist.new.StrCat([r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$"],name="background").Reg(6,0,6, label = r"B Jet Multiplicity").Weight(),
				"ZMult": hist.Hist.new.StrCat([r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$"],name="background").Reg(6,0,6, label = r"Z Boson Multiplicity").Weight(),
				"predictions": hist.Hist.new.StrCat([r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$"],name="background").Reg(N1,0,1.0, label = r"Neural Network Model Output").Weight(),
				"RecoRadion_Mass": hist.Hist.new.StrCat([r"$t\bar{t}$", r"Drell-Yan+Jets", "Di-Bosons", "Single Top", "W+Jets", r"$ZZ \rightarrow 4l$"],name="background").Reg(N_fourMass,0,3000, label = r"Reconstructed Radion Mass (GeV)").Weight(),
			}

		hist_dict_signal = {
				"radion_pt": hist.Hist.new.StrCat([r"$m_\phi$ = 1 TeV", r"$m_\phi$ = 2 TeV", r"$m_\phi$ = 3 TeV"],name="signal").Reg(N1,0,500, label=r"Radion $p_T$ (GeV)").Weight(), 
				"vis_mass": hist.Hist.new.StrCat([r"$m_\phi$ = 1 TeV", r"$m_\phi$ = 2 TeV", r"$m_\phi$ = 3 TeV"],name="signal").Reg(N2,0,120, label=r"Leading di-$\tau$ Mass (GeV)").Weight(),
				"vis_mass2": hist.Hist.new.StrCat([r"$m_\phi$ = 1 TeV", r"$m_\phi$ = 2 TeV", r"$m_\phi$ = 3 TeV"],name="signal").Reg(N2,0,120, label=r"Subleading di-$\tau$ Mass (GeV)").Weight(),
				"radion_eta": hist.Hist.new.StrCat([r"$m_\phi$ = 1 TeV", r"$m_\phi$ = 2 TeV", r"$m_\phi$ = 3 TeV"],name="signal").Reg(N1,-5,5, label = r"Radion $\eta$").Weight(),
				"higgs1_dr": hist.Hist.new.StrCat([r"$m_\phi$ = 1 TeV", r"$m_\phi$ = 2 TeV", r"$m_\phi$ = 3 TeV"],name="signal").Reg(N1,0,5, label = r"Leading di-$\tau$ $\Delta$R").Weight(),
				"higgs2_dr": hist.Hist.new.StrCat([r"$m_\phi$ = 1 TeV", r"$m_\phi$ = 2 TeV", r"$m_\phi$ = 3 TeV"],name="signal").Reg(N1,0,5, label = r"Subleading di-$\tau$ $\Delta$R").Weight(),
				"dphi_H1": hist.Hist.new.StrCat([r"$m_\phi$ = 1 TeV", r"$m_\phi$ = 2 TeV", r"$m_\phi$ = 3 TeV"],name="signal").Reg(N1,-pi,pi, label = r"Subleading di-$\tau$ $\Delta \phi$").Weight(),
				"dphi_H2": hist.Hist.new.StrCat([r"$m_\phi$ = 1 TeV", r"$m_\phi$ = 2 TeV", r"$m_\phi$ = 3 TeV"],name="signal").Reg(N1,-pi,pi, label = r"Leading di-$\tau$ $\Delta \phi$").Weight(),
				"dphi_H1_MET": hist.Hist.new.StrCat([r"$m_\phi$ = 1 TeV", r"$m_\phi$ = 2 TeV", r"$m_\phi$ = 3 TeV"],name="signal").Reg(N1,-pi,pi, label = r"Leading Higgs MET $\Delta \phi$").Weight(),
				"dphi_H2_MET": hist.Hist.new.StrCat([r"$m_\phi$ = 1 TeV", r"$m_\phi$ = 2 TeV", r"$m_\phi$ = 3 TeV"],name="signal").Reg(N1,-pi,pi, label = r"Subleading Higgs MET $\Delta \phi$").Weight() ,
				"dr_HH": hist.Hist.new.StrCat([r"$m_\phi$ = 1 TeV", r"$m_\phi$ = 2 TeV", r"$m_\phi$ = 3 TeV"],name="signal").Reg(N1,0,5, label = r"Higgs $\Delta$R").Weight(),
				"dphi_HH": hist.Hist.new.StrCat([r"$m_\phi$ = 1 TeV", r"$m_\phi$ = 2 TeV", r"$m_\phi$ = 3 TeV"],name="signal").Reg(N1,-pi,pi, label = r"Higgs $\Delta \phi$").Weight(),
				"dr_H1_Rad": hist.Hist.new.StrCat([r"$m_\phi$ = 1 TeV", r"$m_\phi$ = 2 TeV", r"$m_\phi$ = 3 TeV"],name="signal").Reg(N1,0,5, label = r"Leading Higgs Radion $\Delta$R").Weight(),
				"dr_H2_Rad": hist.Hist.new.StrCat([r"$m_\phi$ = 1 TeV", r"$m_\phi$ = 2 TeV", r"$m_\phi$ = 3 TeV"],name="signal").Reg(N1,0,5, label = r"Subleading Higgs Radion $\Delta$R").Weight(),
				"dphi_rad_MET": hist.Hist.new.StrCat([r"$m_\phi$ = 1 TeV", r"$m_\phi$ = 2 TeV", r"$m_\phi$ = 3 TeV"],name="signal").Reg(N1,-pi,pi, label = r"Radion MET $\Delta \phi$").Weight(),
				"H1OS": hist.Hist.new.StrCat([r"$m_\phi$ = 1 TeV", r"$m_\phi$ = 2 TeV", r"$m_\phi$ = 3 TeV"],name = "signal").Reg(11,-5,5,label = r"Leading Higgs Electric Charge").Weight(),
				"H2OS": hist.Hist.new.StrCat([r"$m_\phi$ = 1 TeV", r"$m_\phi$ = 2 TeV", r"$m_\phi$ = 3 TeV"],name = "signal").Reg(11,-5,5,label = r"Subleading Higgs Electric Charge").Weight(),
				"numBJet": hist.Hist.new.StrCat([r"$m_\phi$ = 1 TeV", r"$m_\phi$ = 2 TeV", r"$m_\phi$ = 3 TeV"],name="signal").Reg(6,0,6, label = r"B Jet Multiplicity").Weight(),
				"ZMult": hist.Hist.new.StrCat([r"$m_\phi$ = 1 TeV", r"$m_\phi$ = 2 TeV", r"$m_\phi$ = 3 TeV"],name="signal").Reg(6,0,6, label = r"Z Boson Multiplicity").Weight(),
				"predictions": hist.Hist.new.StrCat([r"$m_\phi$ = 1 TeV", r"$m_\phi$ = 2 TeV", r"$m_\phi$ = 3 TeV"],name="signal").Reg(N1,0,1.0, label = r"Neural Network Model Output").Weight(),
				"RecoRadion_Mass": hist.Hist.new.StrCat([r"$m_\phi$ = 1 TeV", r"$m_\phi$ = 2 TeV", r"$m_\phi$ = 3 TeV"],name="signal").Reg(N_fourMass,0,3000, label = r"Reconstructed Radion Mass (GeV)").Weight(),
			}

		if (region_name == "HighPurity" or region_name == "All"): #Blind the data
			reco_mass = 0.01
		else:
			reco_mass = 3000

		hist_dict_data = {
				"radion_pt": hist.Hist.new.StrCat(["Data"],name="data").Reg(N1,0,500, label=r"Radion $p_T$ (GeV)").Weight(), 
				"vis_mass": hist.Hist.new.StrCat(["Data"],name="data").Reg(N2,0,120, label=r"Leading di-$\tau$ Mass (GeV)").Weight(),
				"vis_mass2": hist.Hist.new.StrCat(["Data"],name="data").Reg(N2,0,120, label=r"Subleading di-$\tau$ Mass (GeV)").Weight(),
				"radion_eta": hist.Hist.new.StrCat(["Data"],name="data").Reg(N1,-5,5, label = r"Radion $\eta$").Weight(),
				"higgs1_dr": hist.Hist.new.StrCat(["Data"],name="data").Reg(N1,0,5, label = r"Leading di-$\tau$ $\Delta$R").Weight(),
				"higgs2_dr": hist.Hist.new.StrCat(["Data"],name="data").Reg(N1,0,5, label = r"Subleading di-$\tau$ $\Delta$R").Weight(),
				"dphi_H1": hist.Hist.new.StrCat(["Data"],name="data").Reg(N1,-pi,pi, label = r"Subleading di-$\tau$ $\Delta \phi$").Weight(),
				"dphi_H2": hist.Hist.new.StrCat(["Data"],name="data").Reg(N1,-pi,pi, label = r"Leading di-$\tau$ $\Delta \phi$").Weight(),
				"dphi_H1_MET": hist.Hist.new.StrCat(["Data"],name="data").Reg(N1,-pi,pi, label = r"Leading Higgs MET $\Delta \phi$").Weight(),
				"dphi_H2_MET": hist.Hist.new.StrCat(["Data"],name="data").Reg(N1,-pi,pi, label = r"Subleading Higgs MET $\Delta \phi$").Weight() ,
				"dr_HH": hist.Hist.new.StrCat(["Data"],name="data").Reg(N1,0,5, label = r"Higgs $\Delta$R").Weight(),
				"dphi_HH": hist.Hist.new.StrCat(["Data"],name="data").Reg(N1,-pi,pi, label = r"Higgs $\Delta \phi$").Weight(),
				"dr_H1_Rad": hist.Hist.new.StrCat(["Data"],name="data").Reg(N1,0,5, label = r"Leading Higgs Radion $\Delta$R").Weight(),
				"dr_H2_Rad": hist.Hist.new.StrCat(["Data"],name="data").Reg(N1,0,5, label = r"Subleading Higgs Radion $\Delta$R").Weight(),
				"dphi_rad_MET": hist.Hist.new.StrCat(["Data"],name="data").Reg(N1,-pi,pi, label = r"Radion MET $\Delta \phi$").Weight(),
				"H1OS": hist.Hist.new.StrCat(["Data"],name = "data").Reg(11,-5,5,label = r"Leading Higgs Electric Charge").Weight(),
				"H2OS": hist.Hist.new.StrCat(["Data"],name = "data").Reg(11,-5,5,label = r"Subleading Higgs Electric Charge").Weight(),
				"numBJet": hist.Hist.new.StrCat(["Data"],name="data").Reg(6,0,6, label = r"B Jet Multiplicity").Weight(),
				"ZMult": hist.Hist.new.StrCat(["Data"],name="data").Reg(6,0,6, label = r"Z Boson Multiplicity").Weight(),
				"predictions": hist.Hist.new.StrCat(["Data"],name="data").Reg(N1,0,1.0, label = r"Neural Network Model Output").Weight(), 
				"RecoRadion_Mass": hist.Hist.new.StrCat(["Data"],name="data").Reg(N_fourMass,0, 3000, label = r"Reconstructed Radion Mass (GeV)").Weight(),
			}
		
		if (region_name == "ZCR"):
			for mass in mass_array:
				signal_input_dict[mass] = signal_input_dict[mass][np.bitwise_and(signal_input_dict[mass].ZMult >= 1,signal_input_dict[mass].numBJet < 1)]
			for background_type in background_dict:
				for background in background_dict[background_type]: 
					background_input_dict[background] = background_input_dict[background][np.bitwise_or(background_input_dict[background].ZMult >= 1, background_input_dict[background].numBJet < 1)]
			for data in data_files:
				data_input_dict[data] = data_input_dict[data][np.bitwise_and(data_input_dict[data].ZMult >= 1,data_input_dict[data].numBJet < 1)]
		if (region_name == "TCR"):
			for mass in mass_array:
				signal_input_dict[mass] = signal_input_dict[mass][np.bitwise_and(signal_input_dict[mass].numBJet >= 1, signal_input_dict[mass].ZMult < 1)]
			for background_type in background_dict:
				for background in background_dict[background_type]: 
					background_input_dict[background] = background_input_dict[background][np.bitwise_and(background_input_dict[background].numBJet >= 1, background_input_dict[background].ZMult < 1)]
			for data in data_files:
				data_input_dict[data] = data_input_dict[data][np.bitwise_and(data_input_dict[data].numBJet >= 1, data_input_dict[data].ZMult < 1)]
		if (region_name == "FakeCR"):
			for mass in mass_array:
				signal_input_dict[mass] = signal_input_dict[mass][np.bitwise_and(signal_input_dict[mass].ZMult < 1,signal_input_dict[mass].numBJet < 1)]
				signal_input_dict[mass] = signal_input_dict[mass][np.bitwise_or(signal_input_dict[mass].H1OS != 0,signal_input_dict[mass].H2OS != 0)]
			for background_type in background_dict:
				for background in background_dict[background_type]: 
					background_input_dict[background] = background_input_dict[background][np.bitwise_and(background_input_dict[background].ZMult < 1,background_input_dict[background].numBJet < 1)]
					background_input_dict[background] = background_input_dict[background][np.bitwise_or(background_input_dict[background].H1OS != 0,background_input_dict[background].H2OS != 0)]
			for data in data_files:
				data_input_dict[data] = data_input_dict[data][np.bitwise_and(data_input_dict[data].ZMult < 1,data_input_dict[data].numBJet < 1)]
				data_input_dict[data] = data_input_dict[data][np.bitwise_or(data_input_dict[data].H1OS != 0,data_input_dict[data].H2OS != 0)]
		if (region_name == "LowPurity"):
			for mass in mass_array:
				signal_input_dict[mass] = signal_input_dict[mass][np.bitwise_and(signal_input_dict[mass].ZMult < 1,signal_input_dict[mass].numBJet < 1)]
				signal_input_dict[mass] = signal_input_dict[mass][np.bitwise_and(signal_input_dict[mass].H1OS == 0,signal_input_dict[mass].H2OS == 0)]
				signal_input_dict[mass] = signal_input_dict[mass][signal_input_dict[mass].predictions < 0.7]
			for background_type in background_dict:
				for background in background_dict[background_type]: 
					background_input_dict[background] = background_input_dict[background][np.bitwise_and(background_input_dict[background].ZMult < 1,background_input_dict[background].numBJet < 1)]
					background_input_dict[background] = background_input_dict[background][np.bitwise_and(background_input_dict[background].H1OS == 0,background_input_dict[background].H2OS == 0)]
					background_input_dict[background] = background_input_dict[background][background_input_dict[background].predictions < 0.7]
			for data in data_files:
				data_input_dict[data] = data_input_dict[data][np.bitwise_and(data_input_dict[data].ZMult < 1,data_input_dict[data].numBJet < 1)]
				data_input_dict[data] = data_input_dict[data][np.bitwise_and(data_input_dict[data].H1OS == 0,data_input_dict[data].H2OS == 0)]
				data_input_dict[data] = data_input_dict[data][data_input_dict[data].predictions < 0.7]
		if (region_name == "HighPurity"):
			for mass in mass_array:
				signal_input_dict[mass] = signal_input_dict[mass][np.bitwise_and(signal_input_dict[mass].ZMult < 1,signal_input_dict[mass].numBJet < 1)]
				signal_input_dict[mass] = signal_input_dict[mass][np.bitwise_and(signal_input_dict[mass].H1OS == 0,signal_input_dict[mass].H2OS == 0)]
				signal_input_dict[mass] = signal_input_dict[mass][signal_input_dict[mass].predictions >= 0.7]
			for background_type in background_dict:
				for background in background_dict[background_type]: 
					background_input_dict[background] = background_input_dict[background][np.bitwise_and(background_input_dict[background].ZMult < 1,background_input_dict[background].numBJet < 1)]
					background_input_dict[background] = background_input_dict[background][np.bitwise_and(background_input_dict[background].H1OS == 0,background_input_dict[background].H2OS == 0)]
					background_input_dict[background] = background_input_dict[background][background_input_dict[background].predictions >= 0.7]
			for data in data_files:
				data_input_dict[data] = data_input_dict[data][np.bitwise_and(data_input_dict[data].ZMult < 1,data_input_dict[data].numBJet < 1)]
				data_input_dict[data] = data_input_dict[data][np.bitwise_and(data_input_dict[data].H1OS == 0,data_input_dict[data].H2OS == 0)]
				data_input_dict[data] = data_input_dict[data][data_input_dict[data].predictions >= 0.7]

		#Generate all histograms
		for hist_name in var_array:
			#Fill background histograms
			for background_type in background_list:
				for background in background_dict[background_type]:
					hist_dict_background[hist_name].fill(background_type,background_input_dict[background][hist_name].to_numpy(),weight=background_input_dict[background]["weight"].to_numpy())
					#print("Hist name: " + hist_name)
					#print("Weight for " + background +":")
					#print(background_input_dict[background]["weight"].to_numpy())
					#if (background == "ZZ4l" and hist_name == "radion_pt"):
					#	print("Z4l radion pT being read in:")
					#	print(background_input_dict[background][hist_name])
			
			#Fill in signal
			for mass in mass_array:
				hist_dict_signal[hist_name].fill(r"$m_\phi$ = %s TeV"%mass[0],signal_input_dict[mass][hist_name].to_numpy(),weight=signal_input_dict[mass]["weight"].to_numpy())

			#Fill in the data
			for data_file in data_files:
				hist_dict_data[hist_name].fill("Data",data_input_dict[data_file][hist_name].to_numpy())

			#Put dictionaries into stacks and arrays for plotting
			background_array = []
			background_stack = hist_dict_background[hist_name].stack("background")
			signal_stack = hist_dict_signal[hist_name].stack("signal")
			data_stack = hist_dict_data[hist_name].stack("data")
			
			signal_array = []
			signal_array.append(hist_dict_signal[hist_name][{"signal": r"$m_\phi$ = 1 TeV"}])
			signal_array.append(hist_dict_signal[hist_name][{"signal": r"$m_\phi$ = 2 TeV"}])
			signal_array.append(hist_dict_signal[hist_name][{"signal": r"$m_\phi$ = 3 TeV"}])
			
			data_hist = hist_dict_data[hist_name][{"data": "Data"}]
			for background in background_list:
				background_array.append(hist_dict_background[hist_name][{"background": background}])

			#Generate plots
			print(hist_name)
			if (region_name == "HighPurity" and hist_name == "RecoRadion_Mass"):
				StackPlot(signal_array,signal_list,background_array,background_list,data_hist,dict_plot_names[hist_name] + "_" + region_name, dict_axis_names[hist_name], data_blind = True) 
			else:
				StackPlot(signal_array,signal_list,background_array,background_list,data_hist,dict_plot_names[hist_name] + "_" + region_name, dict_axis_names[hist_name]) 



		 

