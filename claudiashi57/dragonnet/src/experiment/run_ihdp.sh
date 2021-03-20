#!/usr/bin/env bash


options=(
    'dragonnet'
    'tarnet'

)



for i in ${options[@]}; do
    echo $i
    python -m experiment.ihdp_main --data_base_dir '/home/suleiman/Documents/Master AI/Q3/Deep learning/Reproduction/claudiashi57/dragonnet/dat/ihdp/csv'\
                                 --knob $i\
                                 --output_base_dir '/home/suleiman/Documents/Master AI/Q3/Deep learning/Reproduction/claudiashi57/dragonnet/results/run'


done