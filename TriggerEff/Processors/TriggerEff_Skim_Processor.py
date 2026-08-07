import awkward as ak
import uproot
import hist
from hist import intervals
import matplotlib.pyplot as plt
import numpy as np
from coffea import processor, nanoevents
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema, BaseSchema
from coffea.nanoevents.methods import candidate, vector
from coffea import util
from coffea.lumi_tools import LumiMask
from math import pi
import numba 
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import vector
import os
import time
import datetime
from distributed import Client
from dask_jobqueue import HTCondorCluster
import csv
import glob
import json
from enum import Enum

class Trigger_Eff_Skim_Processor(processor.ProcessorABC):
	def __init__(self,ApplySkim = True, year = 2018, trigger_code = 0):
		self.applySkim = ApplySkim
		self.year = year
		self.nBoostedTau_Selec = 4
		self.trigger_code = trigger_code
	
	def process(self,events):
		vector.register_awkward()
		#Objects for analysis
		dataset = events.metadata['dataset']
		event_level = ak.zip(
			{
				"METHTMHT_Trigger": events.HLT_PFHT500_PFMET100_PFMHT100_IDTight,
				"Mu_Trigger": events.HLT_Mu50,
				"MET_pt": events.MET_pt,
				"MET_Phi": events.MET_phi,
				"event_weight": ak.ones_like(events.MET_pt), #*0.9,
				"n_electrons": ak.zeros_like(events.MET_pt),
				"n_muons": ak.zeros_like(events.MET_pt),
				"n_tau_electrons": ak.zeros_like(events.MET_pt),
				"n_tau_muons": ak.zeros_like(events.MET_pt),
				"n_tau_hadronic": ak.zeros_like(events.MET_pt),
				"event_num": events.event,
				"run": events.run,
				"Lumi" : events.luminosityBlock,
				"PV_ndof": events.PV_ndof,
				"PV_z": events.PV_z,
				"PV_x": events.PV_x,
				"PV_y": events.PV_y,
				"Num_PV": events.PV_npvs,
				"nFatJet": events.nFatJet,
				"Flag_goodVertices": events.Flag_goodVertices,
				"Flag_globalSuperTightHalo2016Filter": events.Flag_globalSuperTightHalo2016Filter,
				"Flag_HBHENoiseFilter": events.Flag_HBHENoiseFilter,
				"Flag_HBHENoiseIsoFilter": events.Flag_HBHENoiseIsoFilter,
				"Flag_EcalDeadCellTriggerPrimitiveFilter": events.Flag_EcalDeadCellTriggerPrimitiveFilter,
				"Flag_BadPFMuonFilter": events.Flag_BadPFMuonFilter,
				"Flag_BadPFMuonDzFilter": events.Flag_BadPFMuonDzFilter,
				"Flag_hfNoisyHitsFilter": events.Flag_hfNoisyHitsFilter,
				"Flag_eeBadScFilter": events.Flag_eeBadScFilter,
				"Flag_ecalBadCalibFilter": events.Flag_ecalBadCalibFilter,
				#"genWeight": events.genWeight
			},
			with_name="EventArray",
			behavior=candidate.behavior,
		)
		boostedtau = ak.zip( 
			{
				"pt": events.boostedTau_pt,
				"Px": events.boostedTau_pt*np.cos(events.boostedTau_phi),
				"Py": events.boostedTau_pt*np.sin(events.boostedTau_phi),
				"Pz": (events.boostedTau_pt/np.sin(2*np.arctan(np.exp(-events.boostedTau_eta))))*np.cos(2*np.arctan(np.exp(-events.boostedTau_eta))),
				"E": np.sqrt((events.boostedTau_pt/np.sin(2*np.arctan(np.exp(-events.boostedTau_eta))))**2 + events.boostedTau_mass**2),
				"mass": events.boostedTau_mass,
				"eta": events.boostedTau_eta,
				"phi": events.boostedTau_phi,
				"nBoostedTau": events.nboostedTau,
				"charge": events.boostedTau_charge,
				"iso": events.boostedTau_idDeepTau2018v2p7VSjet,
				"DBT": events.boostedTau_rawDeepTau2018v2p7VSjet,
				"decay": events.boostedTau_idDecayModeOldDMs,
			},
			with_name="BoostedTauArray",
			behavior=candidate.behavior,
		)
		electron = ak.zip(
			{
				"pt": events.Electron_pt,
				"eta": events.Electron_eta,
				"phi": events.Electron_phi,
				"charge": events.Electron_charge,
				"nElectron": events.nElectron,
				"Px": events.Electron_pt*np.cos(events.Electron_phi),
				"Py": events.Electron_pt*np.sin(events.Electron_phi),
				"Pz": events.Electron_pt*np.tan(2*np.arctan(np.exp(-events.Electron_eta)))**-1,
				"E": np.sqrt(events.Electron_pt**2 + (events.Electron_pt/np.tan(2*np.arctan(np.exp(-events.Electron_eta))))**2 + events.Electron_mass**2),
				"mass": events.Electron_mass, 
				"SCEta": events.Electron_deltaEtaSC,
				"IDMVANoIso": events.Electron_mvaNoIso,
				"RelIso": events.Electron_pfRelIso03_all,
					
			},
			with_name="ElectronArray",
			behavior=candidate.behavior,
			
		)
		muon = ak.zip(
			{
				"pt": events.Muon_pt,
				"eta": events.Muon_eta,
				"phi": events.Muon_phi,
				"charge": events.Muon_charge,
				"nMuon": events.nMuon,
				"Px": events.Muon_pt*np.cos(events.Muon_phi),
				"Py": events.Muon_pt*np.sin(events.Muon_phi),
				"Pz": events.Muon_pt*np.tan(2*np.arctan(np.exp(-events.Muon_eta)))**-1,
				"E": np.sqrt(events.Muon_pt**2 + (events.Muon_pt/np.tan(2*np.arctan(np.exp(-events.Muon_eta))))**2 + events.Muon_mass**2),
				"nMu": events.nMuon,
				"mass": events.Muon_mass, 
				"IDSelec": events.Muon_mediumId,
				#"IDSelec": events.Muon_tightId,
				"D0": events.Muon_dxy,
				"Dz": events.Muon_dz,
				"LooseId": events.Muon_looseId,
				"RelIso": events.Muon_pfRelIso04_all,
					
			},
			with_name="MuonArray",
			behavior=candidate.behavior,
			
		)

		AK8Jet = ak.zip(
			{
				"AK8JetDropMass": events.FatJet_msoftdrop,
				"pt": events.FatJet_pt,
				"eta": events.FatJet_eta,
				"phi": events.FatJet_phi,
				"nAK8Jet": events.nFatJet,
				"softDropM": events.FatJet_msoftdrop,
				"Id": events.FatJet_jetId,
				"mass": events.FatJet_mass, 
			},
			with_name="AK8JetArray",
			behavior=candidate.behavior,
		)
		
		Jet = ak.zip(
			{
				"pt": events.Jet_pt,
				"JetId": events.Jet_jetId, #Not sure that this is correct
				"eta": events.Jet_eta,
				"phi": events.Jet_phi,
				"mass": events.Jet_mass,
				"nJet": events.nJet,
				#"DeepCSVTags_b": events.Jet_btagCSVV2,
				"DeepCSVTags_b": events.Jet_btagDeepB,
			},
			with_name="PFJetArray",
			behavior=candidate.behavior,
		)


		#############
		#Set Up Histograms
		#############	

		#Obtain MHT
		Jet_MHT = Jet[Jet.pt > 30]
		Jet_MHT = Jet_MHT[np.abs(Jet_MHT.eta) < 5]
		Jet_MHT = Jet_MHT[Jet_MHT.JetId > 0.5]
		event_level["MHT_x"] = ak.sum(Jet_MHT.pt*np.cos(Jet_MHT.phi),axis=1,keepdims=False) 
		event_level["MHT_y"] = ak.sum(Jet_MHT.pt*np.sin(Jet_MHT.phi),axis=1,keepdims=False)
		event_level["MHT"] = np.sqrt(event_level.MHT_x**2 + event_level.MHT_y**2)
		del Jet_MHT
		
		#Obtain HT
		Jet_HT = Jet[Jet.pt > 30]
		Jet_HT = Jet_HT[np.abs(Jet_HT.eta) < 3]
		Jet_HT = Jet_HT[Jet_HT.JetId > 0.5]
		event_level["HT"] = ak.sum(Jet_HT.pt, axis=1, keepdims=False) 
		del Jet_HT

		#############
		#Apply Skim (if needed)
		#############
		if (self.applySkim):
			#Boosted tau selections
			if (self.nBoostedTau_Selec > 0):
				#Impose selections boosted taus
				pT_Cond = boostedtau.pt > 20
				eta_Cond = np.abs(boostedtau.eta) < 2.3
				decayMode_Cond = boostedtau.decay >= 0.5
				DBT_Iso_Cond = boostedtau.DBT >= 0.5 #0.85
				
				boostedtau_selec_cond = pT_Cond & eta_Cond & decayMode_Cond & DBT_Iso_Cond
				boostedtau = boostedtau[boostedtau_selec_cond] #Apply selections to all individual taus
			
				#Require events have at least 1 boosted tau
				lead_boostedtau_cond = ak.num(boostedtau,axis=1) >= 1
					
				boostedtau = boostedtau[lead_boostedtau_cond]
				AK8Jet = AK8Jet[lead_boostedtau_cond]
				Jet = Jet[lead_boostedtau_cond]
				electron = electron[lead_boostedtau_cond]
				muon = muon[lead_boostedtau_cond]
				event_level = event_level[lead_boostedtau_cond]
				
				#Impose selections on Subleading boosted tau
				if (self.nBoostedTau_Selec > 1):
					#Require events have at least 2 boosted tau
					sublead_boostedtau_cond = ak.num(boostedtau,axis=1) >= 2
						
					boostedtau = boostedtau[sublead_boostedtau_cond]
					AK8Jet = AK8Jet[sublead_boostedtau_cond]
					Jet = Jet[sublead_boostedtau_cond]
					electron = electron[sublead_boostedtau_cond]
					muon = muon[sublead_boostedtau_cond]
					event_level = event_level[sublead_boostedtau_cond]
				
				#Impose selections on third-leading boosted tau
				if (self.nBoostedTau_Selec > 2):
					#Require events have at least 2 boosted tau
					thirdlead_boostedtau_cond = ak.num(boostedtau,axis=1) >= 3
						
					boostedtau = boostedtau[thirdlead_boostedtau_cond]
					AK8Jet = AK8Jet[thirdlead_boostedtau_cond]
					Jet = Jet[thirdlead_boostedtau_cond]
					electron = electron[thirdlead_boostedtau_cond]
					muon = muon[thirdlead_boostedtau_cond]
					event_level = event_level[thirdlead_boostedtau_cond]

				
				#Impose selections on fourth-leading boosted tau
				if (self.nBoostedTau_Selec > 3):
					#Require events have at least 2 boosted tau
					fourthlead_boostedtau_cond = ak.num(boostedtau,axis=1) >= 4
						
					boostedtau = boostedtau[fourthlead_boostedtau_cond]
					AK8Jet = AK8Jet[fourthlead_boostedtau_cond]
					Jet = Jet[fourthlead_boostedtau_cond]
					electron = electron[fourthlead_boostedtau_cond]
					muon = muon[fourthlead_boostedtau_cond]
					event_level = event_level[fourthlead_boostedtau_cond]


		#############
		#Trigger Application
		#############
		#h_muon_pT_PreTrigger = hist.Hist.new.Regular(20,0,500, label = r"$\mu$ $p_T$ [GeV]",overflow = True).Double()
		#h_muon_pT_Trigger = hist.Hist.new.Regular(20,0,500, label = r"$\mu$ $p_T$ [GeV]",overflow = True).Double()
		h_muon_pT_PreTrigger = hist.Hist.new.Variable([10,20,30,40,50,70,100,130,160,200,250,300,400,600], label = r"$\mu$ $p_T$ [GeV]",overflow = True).Double()
		h_muon_pT_Trigger = hist.Hist.new.Variable([10,20,30,40,50,70,100,130,160,200,250,300,400,600], label = r"$\mu$ $p_T$ [GeV]",overflow = True).Double()
			
		#Add MET, HT and MHT histogram
	#	h_MET_PreTrigger = hist.Hist.new.Regular(15,0,500, label=r"MET [GeV]",overflow = True).Double()
	#	h_HT_PreTrigger = hist.Hist.new.Regular(20,0,1200, label=r"HT [GeV]",overflow = True).Double()
	#	h_MHT_PreTrigger = hist.Hist.new.Regular(15,0,500, label=r"MHT [GeV]",overflow = True).Double()
		

		h_MET_PreTrigger = hist.Hist.new.Variable([10,20,30,40,50,70,100,130,160,200,250,300,350,400,450,500], label=r"MET [GeV]",overflow = True).Double()
		h_HT_PreTrigger = hist.Hist.new.Variable([20,40,60,80,100,120,140,200,250,500,750,1000], label=r"HT [GeV]",overflow = True).Double()
		h_MHT_PreTrigger = hist.Hist.new.Variable([10,20,30,40,50,70,100,130,160,200,250,300,350,400,450,500], label=r"MHT [GeV]",overflow = True).Double()
		
		h_MET_Trigger = hist.Hist.new.Variable([10,20,30,40,50,70,100,130,160,200,250,300,350,400,450,500], label=r"MET [GeV]",overflow = True).Double()
		h_HT_Trigger = hist.Hist.new.Variable([20,40,60,80,100,120,140,200,250,500,750,1000], label=r"HT [GeV]",overflow = True).Double()
		h_MHT_Trigger = hist.Hist.new.Variable([10,20,30,40,50,70,100,130,160,200,250,300,350,400,450,500], label=r"MHT [GeV]",overflow = True).Double()
		
		#Muon Trigger
		h_muon_pT_PreTrigger.fill(ak.ravel(muon.pt))
		#Apply the trigger
		Mu50_Trigger = event_level.Mu_Trigger
		h_muon_pT_Trigger.fill(ak.ravel(muon[Mu50_Trigger].pt))

		#HT MHT MET Trigger
		h_MET_PreTrigger.fill(ak.ravel(event_level.MET_pt))
		h_HT_PreTrigger.fill(ak.ravel(event_level.HT))
		h_MHT_PreTrigger.fill(ak.ravel(event_level.MHT))
		HTMETMHT_Trigger = event_level.METHTMHT_Trigger
        #Apply the trigger
		h_MET_Trigger.fill(ak.ravel(event_level[HTMETMHT_Trigger].MET_pt))
		h_HT_Trigger.fill(ak.ravel(event_level[HTMETMHT_Trigger].HT))
		h_MHT_Trigger.fill(ak.ravel(event_level[HTMETMHT_Trigger].MHT))

		return{
			dataset: {
					"Muon_pt_PreTrigger": h_muon_pT_PreTrigger,
					"Muon_pt_Trigger": h_muon_pT_Trigger,
					"HT_PreTrigger": h_HT_PreTrigger,
					"HT_Trigger": h_HT_Trigger,
					"MHT_PreTrigger": h_MHT_PreTrigger,
					"MHT_Trigger": h_MHT_Trigger,
					"MET_PreTrigger": h_MET_PreTrigger,
					"MET_Trigger": h_MET_Trigger
				}
			}

		
	def postprocess(self, accumulator):
		pass

