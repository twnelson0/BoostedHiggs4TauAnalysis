#!/bin/bash

for file in $(pwd)/*.coffea; do
	wp="${file##*/}"
	wp=$(echo $wp | cut -d "_" -f 8)
	python3 CutFlow_Producer.py -n 4 -f "${file##*/}" -o "Cutflow_Table_WP_"$wp"_DBT"
done

