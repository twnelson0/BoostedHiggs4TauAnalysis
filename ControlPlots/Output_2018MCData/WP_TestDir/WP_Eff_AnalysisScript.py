import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv

def get_selec_eff(input_file, process):
	csv_frame = pd.read_csv(input_file)
	skim_count = csv_frame[csv_frame["Sample"] == process]["SkimOnly"]
	selec_count = csv_frame[csv_frame["Sample"] == process]["Higgs_dR"]

	return selec_count/skim_count


