#!/usr/bin/env bash


options=(
    'dragonnet'
    'tarnet'

)



for i in ${options[@]}; do
    echo $i
    python -m experiment.lalonde_main --data_base_dir '/Users/jessie/OneDrive/Documents/MSc/Q3/DL/ReprodcutionPaper/data/lalonde'\
                                 --knob $i\
                                 --output_base_dir '/Users/jessie/OneDrive/Documents/MSc/Q3/DL/ReprodcutionPaper/output/lalonde'


done
