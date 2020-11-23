#!/bin/bash


# Intra Data Center MultiPath Optimization with
# Emulated Software Defined Networks
#
# Description: script used by gerador_grafico.sh to generate GNUplot graphics.
# 
# Author: Lucio A. Rocha
# Last update: 23/11/2020

set grid
set xlabel sprintf("Time (s)\n(Transfered: %s %s)",ARG1,ARG2)
set ylabel sprintf('Bitrate: %s',ARG3)
plot 'dados.txt' t 'TCP Flow' w linespoints
