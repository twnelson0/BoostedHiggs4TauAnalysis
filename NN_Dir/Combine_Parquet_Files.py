import pyarrow.parquet as pq
import os
import glob

#Global Variables
parquet_dir = "/hdfs/store/user/twnelson/HH4Tau_EtAl/Parquet_Files/2018/New_Dir/"
Process_Array = ["TTToSemiLeptonic",
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
			"Signal_2TeV"]

if __name__ == "__main__":
	#Produce dictionary of files
	parquet_dict = dict.fromkeys(Process_Array)

	for process in Process_Array:
		if (len(glob.glob(parquet_dir + process + "*.parquet")) > 0):
			parquet_dict[process] = glob.glob(parquet_dir + process + "*.parquet")
		else:
			del parquet_dict[process]
	
	#Merge sampe process files together
	for process in parquet_dict.keys():
		schema = pq.ParquetFile(parquet_dict[process][0]).schema_arrow
		with pq.ParquetWriter(parquet_dir + process + ".parquet", schema = schema) as writer:
			for file in parquet_dict[process]:
				writer.write_table(pq.read_table(file,schema = schema))
	
		
     
