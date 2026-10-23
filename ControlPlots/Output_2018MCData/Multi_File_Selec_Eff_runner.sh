#!/bin/bash

#WP_ARR=('p85' 'p86' 'p87' 'p88' 'p89' 'p9' 'p91' 'p92' 'p93' 'p94' 'p95' 'p96')
WP_ARR=('p931' 'p932' 'p933' 'p934' 'p935' 'p936' 'p937' 'p938' 'p939')

for WP in "${WP_ARR[@]}"; do
	echo $WP
	#python3 CutFlow_Producer.py -n 4 -f "output_4_boosted_tau_selec_4TauSamples_DBTWP_"$WP"_Signal_BothTriggers_Coffea2026.coffea" -o DBT_Out_WP_$WP
	python3 CutFlow_Producer.py -n 4 -f "output_4_boosted_tau_selec_4TauSamples_DBTWP_"$WP"_Signal_WithChargeHist_BothTriggers_Coffea2026.coffea" -o DBT_Out_WP_$WP
done
