import awkward as ak
import numpy as np

#Era Enumeration
class RunEra_Enum(Enum):
	MC_2018=0
	UL_2018_A=1
	UL_2018_B=2
	UL_2018_C=3
	UL_2018_D=4

#Phi corrections
def PhiCorrections(x,y):
	if (x == 0 and y > 0):
		corrected_phi = np.pi
	elif (x == 0 and y < 0):
		corrected_phi = -np.pi
	elif (x > 0):
		corrected_phi = np.arctan(y/x)
	elif (x < 0 and y > 0):
		corrected_phi = np.arctan(y/x) + np.pi
	elif (x < 0 and y < 0):
		corrected_phi = np.arctan(y/x) + np.pi
	else:
		corrected_phi = 0

	return corrected_phi

#Vectorize the phi corrections
vec_PhiCorrections = np.vectorize(PhiCorrections)

#MET phi crrections
def METPhi_Corrections(uncorrMET_pt, uncorrMET_phi, run_num, isData, nPV, year=2018):
	MET_Phi_Corr = {"MET_pt_corr": uncorrMET_pt, "MET_phi_corr": uncorrMET_phi}
	runera = -1

	#Correct nPV 
	nPV = ak.where(nPV > 100, ak.ones_like(nPV)*100, nPV)

	#Set run era
	if (year == 2018):
		if (not(isData)):
			runera = RunEra_Enum["MC_2018"]
		else:
			if (ak.all(run_num) >= 315252 and ak.all(run_num) <= 316995):
				runera = RunEra_Enum["UL_2018_A"]
			if (ak.all(run_num) >= 316998 and ak.all(run_num) <= 319312):
				runera = RunEra_Enum["UL_2018_B"]
			if (ak.all(run_num) >= 319313 and ak.all(run_num) <= 320393):
				runera = RunEra_Enum["UL_2018_C"]
			if (ak.all(run_num) >= 320394 and ak.all(run_num) <= 325273):
				runera = RunEra_Enum["UL_2018_D"]

	#METX and METY corrections
	METX_Corr = ak.zeros_like(MET_Phi_Corr["MET_pt_corr"])
	METY_Corr = ak.zeros_like(MET_Phi_Corr["MET_pt_corr"])
	if (runera == RunEra_Enum["UL_2018_A"]):
		METX_Corr = -(0.362865*nPV -1.94505)
		METY_Corr = -(0.0709085*nPV -0.307365)
	if (runera == RunEra_Enum["UL_2018_B"]):
		METX_Corr = -(0.492083*nPV -2.93552)
		METY_Corr = -(0.17874*nPV -0.786844)
	if (runera == RunEra_Enum["UL_2018_C"]):
		METX_Corr = -(0.521349*nPV -1.44544)
		METY_Corr = -(0.118956*nPV -1.96434)
	if (runera == RunEra_Enum["UL_2018_D"]):
		METX_Corr = -(0.531151*nPV -1.37568)
		METY_Corr = -(0.0884639*nPV -1.57089)
	if (runera == RunEra_Enum["MC_2018"]):
		METX_Corr = -(0.296713*nPV -0.141506)
		METY_Corr = -(0.115685*nPV +0.0128193)

	#Obtain corectected MET
	CorrectedMET_x = uncorrMET_pt*np.cos(uncorrMET_phi) + METX_Corr
	CorrectedMET_y = uncorrMET_pt*np.cos(uncorrMET_phi) + METX_Corr

	CorrectedMET = np.sqrt(CorrectedMET_x**2 + CorrectedMET_y**2)

	CorrectedPhi = vec_PhiCorrections(CorrectedMET_x,CorrectedMET_y)

	MET_Phi_Corr["MET_pt_corr"] = CorrectedMET
	MET_Phi_Corr["MET_phi_corr"] =	CorrectedPhi

	return MET_Phi_Corr

