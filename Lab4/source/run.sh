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
        export MT_CONF=0
        ./x.serial ${size} ${settings[0]} ${settings[1]} ${settings[2]} >> "outFiles/serial_${size}.out"
        for type in "cgl"
        do
            export MT_CONF=0
            ./x.${type} ${size} ${settings[0]} ${settings[1]} ${settings[2]} >> "outFiles/${type}_${size}.out"
            export MT_CONF=0,1
            ./x.${type} ${size} ${settings[0]} ${settings[1]} ${settings[2]} >> "outFiles/${type}_${size}.out"
            export MT_CONF=0,1,2,3
            ./x.${type} ${size} ${settings[0]} ${settings[1]} ${settings[2]} >> "outFiles/${type}_${size}.out"
            export MT_CONF=0,1,2,3,4,5,6,7
            ./x.${type} ${size} ${settings[0]} ${settings[1]} ${settings[2]} >> "outFiles/${type}_${size}.out"
        done
    done
done