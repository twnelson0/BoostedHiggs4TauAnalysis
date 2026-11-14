import pandas as pd
import numpy as np
import json
import os
import tensorflow as tf
import awkward as ak

def read_file(input_file):
	data = pd.read_parquet(input_file,engine="pyarrow")
	return data

def normalize_data(data, norm_data):
	for variable in norm_data["Unnamed: 0"]:
		mean = norm_data[norm_data["Unnamed: 0"] == variable]['mu'].values[0]
		std = norm_data[norm_data["Unnamed: 0"] == variable]['std'].values[0]
		data[variable]	= (data[variable] - mean)/ std
	return data

if __name__ == "__main__":
	#file_array = ["Data_JetHT_mass_2000GeV.parquet", "Data_SingleMuonmass_2000GeV.parquet"]
	#file_array = ["Data_JetHT","Data_SingleMuon","Signal"]
	
#	file_array = ["Data_JetHT","Data_SingleMuon","Signal_mass_1000GeV","Signal_mass_2000GeV","Signal_mass_3000GeV","TTToSemiLeptonic","TTTo2L2Nu","TTToHadronic",
#			"DYJetsToLL_Pt-50To100","DYJetsToLL_Pt-100To250","DYJetsToLL_Pt-250To400","DYJetsToLL_Pt-400To650","DYJetsToLL_Pt-650ToInf",
#			"WZ3l1nu","WZ2l2q","WZ1l1nu2q","ZZ2l2q", "WZ1l3nu", "VV2l2nu", "Tbar-tchan","T-tchan","Tbar-tW","T-tW", 
#			"WJetsToLNu_HT-100To200","WJetsToLNu_HT-200To400","WJetsToLNu_HT-400To600","WJetsToLNu_HT-600To800","WJetsToLNu_HT-800To1200","WJetsToLNu_HT-1200To2500","WJetsToLNu_HT-2500ToInf",
#			"ZZ4l"]

	file_array = ["TTToSemiLeptonic",
			"TTTo2L2Nu",
			"TTToHadronic",
			"ZZ4l",
			"ZZTo2L2Nu",
			"ZZTo2Nu2Q",
			"VV2l2nu",
			"ZZTo4Q" ,
			"WWTo1L1Nu2Q",
			"WWTo4Q",
			"WZ1l3nu",
			"ZZ2l2q",
			"WZ2l2q",
			"WZ1l1nu2q",
			"DYJetsToLL_M-4to50_HT-70to100",
			"DYJetsToLL_M-4to50_HT-100to200",
			"DYJetsToLL_M-4to50_HT-200to400",
			"DYJetsToLL_M-4to50_HT-400to600",
			"DYJetsToLL_M-4to50_HT-600toInf",
			"DYJetsToLL_M-50_HT-70to100",
			"DYJetsToLL_M-50_HT-100to200",
			"DYJetsToLL_M-50_HT-200to400",
			"DYJetsToLL_M-50_HT-400to600",
			"DYJetsToLL_M-50_HT-600to800",
			"DYJetsToLL_M-50_HT-800to1200",
			"DYJetsToLL_M-50_HT-1200to2500",
			"DYJetsToLL_M-50_HT-2500toInf",
			"T-tchan",
			"Tbar-tchan",
			"T-tW",
			"Tbar-tW",
			"ST_s-channel_4f_hadronicDecays",
			"ST_s-channel_4f_leptonDecays",
			"WJetsToLNu_HT-70To100",
			"WJetsToLNu_HT-100To200",
			"WJetsToLNu_HT-200To400",
			"WJetsToLNu_HT-400To600",
			"WJetsToLNu_HT-600To800",
			"WJetsToLNu_HT-800To1200",
			"WJetsToLNu_HT-1200To2500",
			"WJetsToLNu_HT-2500ToInf",
			"QCD_HT50to100",
			"QCD_HT100to200",
			"QCD_HT200to300",
			"QCD_HT300to500",
			"QCD_HT500to700",
			"QCD_HT700to1000",
			"QCD_HT1000to1500",
			"QCD_HT1500to2000",
			"QCD_HT2000toInf",
			"Data_Mu",
			"Data_HT",
			"Signal_4Tau_1TeV",
			#"Signal_4Tau_1p5TeV",
			"Signal_4Tau_2TeV",
			#"Signal_4Tau_2p5TeV",
			"Signal_4Tau_3TeV",
			"Signal_2V2Tau_1TeV",
			"Signal_2V2Tau_2TeV",
			"Signal_2V2Tau_3TeV",
			"Signal_4V_1TeV",
			"Signal_4V_2TeV",
			"Signal_4V_3TeV"]
	file_loc = "/hdfs/store/user/twnelson/HH4Tau_EtAl/Parquet_Files/2018/ParquetFiles_2026_11_11_1952/"

	for file_name in file_array:
		if not(os.path.isfile(file_loc + file_name + ".parquet")):
			print("Empty")
			print(file_name)
			continue
		#Get config file from JSON
		#with open("conf.json",'r') as config_file
		#	 config = json.load(config_file)

		#Extract config varaibles
		#model_path = config['model_path']
		#input_tree_name = config['input_tree_name']
		#input_branches = config['input_branches']
		#evaluation_branches = config['evaluation_branches']
		#output_column_name = config['output_column_name']
		#output_tree_name = config['output_tree_name']

		#Load Neural Net Model
		model = tf.keras.models.load_model("model.keras")
		model.summary()

		#Load the data
		data_full = read_file(file_loc + file_name +".parquet")
		
		#Drop variables not used in model 
		data = data_full.drop("weight",axis=1)
		data = data.drop("ZMult",axis=1)
		data = data.drop("RecoRadion_Mass",axis=1)
		data = data.drop("numBJet",axis=1)
		data = data.drop("H1OS",axis=1)
		data = data.drop("H2OS",axis=1)
		data = data.drop("LeadingTau_pT",axis=1)

		#Read in normalization information and normalize data
		norm_data = pd.read_csv("variable_norm.csv")
		data_norm = normalize_data(data,norm_data)
		data_norm_np = data_norm.to_numpy() #Convert to numpy

		#Run stuff through the model
		print(data_norm)
		print(data_norm_np)
		print(data_norm_np.shape[0])
		print(model.input_shape)
		print(file_name)
		if (data_norm_np.shape[0] != 0):
			print("Not empty")
			predictions = model.predict(data_norm_np)
		else:
			print("Empty")
			predictions = np.array([])
		
		data_full["predictions"] = predictions.flatten()

		#Store parquet files
		data_full.to_parquet(file_name + "with_predictions.parquet")

	



