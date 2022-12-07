#!/bin/bash

mkdir -p outFiles

input="100-0-0;80-10-10;20-40-40;0-50-50"
IFS=';'
read -a strarr <<< "$input"

for val in "${strarr[@]}";
do
    IFS='-'
    read -a settings <<< "$val"
    for size in 1024 8192
    do  
        MT_CONF=0
        ./x.serial ${size} ${settings[0]} ${settings[1]} ${settings[2]} >> "outFiles/serial_${size}.out"
        for type in "cgl" "fgl" "opt" "lazy" "nb"
        do
            MT_CONF=0
            ./x.${type} ${size} ${settings[0]} ${settings[1]} ${settings[2]} >> "outFiles/${type}_${size}.out"
            MT_CONF=0,1
            ./x.${type} ${size} ${settings[0]} ${settings[1]} ${settings[2]} >> "outFiles/${type}_${size}.out"
            MT_CONF=0,1,2,3
            ./x.${type} ${size} ${settings[0]} ${settings[1]} ${settings[2]} >> "outFiles/${type}_${size}.out"
            MT_CONF=0,1,2,3,4,5,6,7
            ./x.${type} ${size} ${settings[0]} ${settings[1]} ${settings[2]} >> "outFiles/${type}_${size}.out"
            MT_CONF=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
            ./x.${type} ${size} ${settings[0]} ${settings[1]} ${settings[2]} >> "outFiles/${type}_${size}.out"
            MT_CONF=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31
            ./x.${type} ${size} ${settings[0]} ${settings[1]} ${settings[2]} >> "outFiles/${type}_${size}.out"
            MT_CONF=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63
            ./x.${type} ${size} ${settings[0]} ${settings[1]} ${settings[2]} >> "outFiles/${type}_${size}.out"
            MT_CONF=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63
            ./x.${type} ${size} ${settings[0]} ${settings[1]} ${settings[2]} >> "outFiles/${type}_${size}.out"
        done
    done
done