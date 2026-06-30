#!/bin/bash

python3 PlotProducer.py -f $1 -n 4 -r All
python3 PlotProducer.py -f $1 -n 4 -r ZCR
python3 PlotProducer.py -f $1 -n 4 -r TCR
python3 PlotProducer.py -f $1 -n 4 -r FakeCR
