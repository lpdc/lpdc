#!/bin/bash

# Intra Data Center MultiPath Optimization with
# Emulated Software Defined Networks
#
# Description: script used by gerador_grafico.sh to generate GNUplot graphics.
# 
# Author: Lucio A. Rocha
# Last update: 23/11/2020

#Recover the throughput of all edge hosts

#To run: ./gerador_grafico_multi.sh <baseFileName> <numberOfFiles>
#Example:./gerador_grafico_multi.sh ../iperf3multi/client_h  16

#Le-se:
# grep sec: linhas com 'sec'
# head -60: do inicio ateh 60 linhas (60 segundos)
# tr - " ": substitua - com espaco
# awk: imprima as colunas 4 e 8

#echo $2
#echo `expr $3 - 1`

i=0
#while [ `expr $i != $2` = 1 ]; do
#    i=`expr $i + 1`
#    file=`echo $1$i`
#    echo $file
#done
      
echo "Argumentos: $#"
if [ $# != 3 ]; then
    echo " Sintax:  ./gerador_grafico_multi.sh <SOURCE_PATH> <baseFileName> <numberOfFiles>"
    echo "Example:  ./gerador_grafico_multi.sh ../iperf3multi client_h 16"
else
    while [ `expr $i != $3` = 1 ]; do
	i=`expr $i + 1`
	file=`echo dados_$2$i.txt`
	echo $file
	transfer=`cat $1/$2$i | grep sender | awk '{print $5}'`
	transferUnit=`cat $1/$2$i | grep sender | awk '{print $6}'`
	bitrateUnit=`cat $1/$2$i | grep sender | awk '{print $8}'`
	echo "#Transfered: $transfer" > $file
	echo "#TransferUnit: $transferUnit" >> $file
	echo "#Bitrate: $bitrateUnit" >> $file
	echo "#Second Transfered" >> $file
	cat $1/$2$i | grep sec | head -60 | tr - " " | awk '{print $4,$8}' >> $file
	#gnuplot -p -c gerador_grafico2.sh $transfer $transferUnit $bitrateUnit	
    done
fi
