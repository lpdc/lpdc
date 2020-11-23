#!/bin/bash

# Intra Data Center MultiPath Optimization with
# Emulated Software Defined Networks
#
# Description: script to generate GNUplot graphics.
# 
# Author: Lucio A. Rocha
# Last update: 23/11/2020

#How to run: ./gerador_grafico.sh nome_arquivo

#Le-se:
# grep sec: linhas com 'sec'
# head -60: do inicio ateh 60 linhas (60 segundos)
# tr - " ": substitua - com espaco
# awk: imprima as colunas 4 e 8

file="dados.txt"
echo "Argumentos: $#"
if [ $# != 1 ]; then
   echo "Sintaxe: ./gerador_grafico.sh <nome_arquivo>"
else
    transfer=`cat $1 | grep sender | awk '{print $5}'`
    transferUnit=`cat $1 | grep sender | awk '{print $6}'`
    bitrateUnit=`cat $1 | grep sender | awk '{print $8}'`
    echo "#Transfered: $transfer" > $file
    echo "#TransferUnit: $transferUnit" >> $file
    echo "#Bitrate: $bitrateUnit" >> $file
    echo "#Second Transfered" >> $file
    cat $1 | grep sec | head -60 | tr - " " | awk '{print $4,$8}' >> $file
    gnuplot -p -c gerador_grafico2.sh $transfer $transferUnit $bitrateUnit
fi
