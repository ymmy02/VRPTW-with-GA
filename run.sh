#!/bin/sh

#========================
DATASETDIR=dataset
TYPE=R1
INDEX=1
# input file is ${TYPE}0${INDEX}.txt ex) R101.txt
RESULTDIR=results
POPULATION=10
GENERATION=10
SELECTION=pareto    # pareto, wsum, ranksum
CROSSOVER=bcrc      # uox, pmx, rc, bcrc
MUTATION=inversion  # inversion, insersion
W_NVWHICLE=100
W_DISTANCE=0.001
ELITE=0
TOURNAMENT=3
CXRATE=0.6
MURATE=0.2
MUIRATE=0.03
SUFFIX=
#========================

FILE=${TYPE}0${INDEX}
INPUT=${DATASETDIR}/${TYPE}/${FILE}.txt
OUTPUT=${RESULTDIR}/${TYPE}/${FILE}

mkdir -p ${OUTPUT}

python3 main.py ${INPUT} ${OUTPUT} ${POPULATION} \
    ${GENERATION} ${SELECTION} ${CROSSOVER} ${MUTATION} \
    ${W_NVWHICLE} ${W_DISTANCE} ${ELITE} ${TOURNAMENT} \
    ${CXRATE} ${MURATE} ${MUIRATE} ${SUFFIX}
