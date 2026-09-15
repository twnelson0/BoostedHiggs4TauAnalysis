import awkward as ak
import numpy as np
import uproot
import hist as hist
import matplotlib.pyplot as plt

if __name__ == "__main__":
	#Files to be accessed
	file_base = "root://cmseos.fnal.gov//store/user/abdollah/SkimBoostedHH4t/2018/4t/v2_Hadd/"
	file_list = ["GluGluToRadionToHHTo4T_M-2000.root","ZZ4l.root"]
	sample_dict = {"GluGluToRadionToHHTo4T_M-2000.root" : "Signal_2TeV_2018","ZZ4l.root": "ZZ4l"}

	#Produce MVA distributions in each file
	for file in file_list:
		fig,ax = plt.subplots()
		h_MVAVar = hist.Hist.new.Regular(100,-1,1, label=r"boostedTauByIsolationMVArun2v1DBoldDMwLTrawNew", overflow = False).Double()
		
		with uproot.open(file_base + file + ":4tau_tree") as PL_file:
			print(PL_file["boostedTauByIsolationMVArun2v1DBoldDMwLTrawNew"].array())
			h_MVAVar.fill(ak.ravel(PL_file["boostedTauByIsolationMVArun2v1DBoldDMwLTrawNew"].array()))

		#Save the output
		h_MVAVar[0::4j].plot1d(ax=ax)
		#hist.rebin(20,ax)
		ax.set_title(sample_dict[file])
		plt.savefig("PL_MVA_" + sample_dict[file] + "_Distribution.png")	



