#!/bin/bash

#========================
DATASETDIR=dataset
#TYPE=R1
#INDEX=1
# input file is ${TYPE}0${INDEX}.txt ex) R101.txt
RESULTDIR=results
POPULATION=80
GENERATION=80
SELECTION=wsum       # pareto, wsum, ranksum
#CROSSOVER=bcrc      # uox, pmx, rc, bcrc
MUTATION=inversion  # inversion, insersion
W_NVWHICLE=100
W_DISTANCE=0.001
ELITE=0
TOURNAMENT=3
#CXRATE=0.6
#MURATE=0.2
MUIRATE=0.03
SUFFIX=
#========================

if [ $# -ge 2 ]; then
    echo "[usage] $0 [wsum, pareto, ranksum]" 1>&2
    exit 1
fi
SELECTION=${1}      # wsum, pareto, ranksum

cd ../

for TYPE in R1 C1 RC1 R2 C2 RC2
do
    for INDEX in `seq 1 3`
    do
        for CROSSOVER in uox pmx bcrc
        do
            for CXRATE in 0.6 0.7 0.8 0.9
            do
                for MURATE in 0.1 0.2 0.3 0.4
                do
                    for i in `seq 1 10`
                    do
                        FILE=${TYPE}0${INDEX}
                        INPUT=${DATASETDIR}/${TYPE}/${FILE}.txt
                        OUTPUT=${RESULTDIR}/ex1/${CROSSOVER}/${FILE}/${CXRATE}/${MURATE}

                        mkdir -p ${OUTPUT}

                        python3 main.py ${INPUT} ${OUTPUT} ${POPULATION} \
                            ${GENERATION} ${SELECTION} ${CROSSOVER} ${MUTATION} \
                            ${W_NVWHICLE} ${W_DISTANCE} ${ELITE} ${TOURNAMENT} \
                            ${CXRATE} ${MURATE} ${MUIRATE} ${i}
                    done
                done
            done
        done
    done
done
