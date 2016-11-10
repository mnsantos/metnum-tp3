#!/bin/bash

# Para correrlo ejecutar ./calcularFourFactors.sh

paramsDir=../stats/params.txt
fourFactorsDir=../stats/fourFactors
miscellaneousStatsDir=../stats/miscellaneous
abreviaturasDir=../stats/abreviaturas

rm -r -f $fourFactorsDir
mkdir -p $fourFactorsDir

intervalo=$(head -n 1 $paramsDir)

inicio=${intervalo[0]}
final=${intervalo[1]}


for a in $(seq $inicio $final); do
	abreviaturas=$(find $abreviaturasDir -maxdepth 1 -name "*$a*")
	miscellaneousStats=$(find $miscellaneousStatsDir -maxdepth 1 -name "*$a*")
	fourFactorsEquipoFile='fourFactors_'$a'.txt'

	# Remover espacios en blanco
	sed -i 's/ //g' $miscellaneousStats $miscellaneousStats
	# Remover *
	sed -i 's/*//g' $miscellaneousStats $miscellaneousStats

	#Cargar abreviaturas de equipos
	numeros=( $(cut -d ',' -f1 $abreviaturas) )
	nombres=( $(cut -d ',' -f2 $abreviaturas) )

	teams=( $(cut -d ',' -f2 $miscellaneousStats) )
	eFGPercent=( $(cut -d ',' -f15 $miscellaneousStats) )
	TOVPercent=( $(cut -d ',' -f16 $miscellaneousStats) )
	ORBPercent=( $(cut -d ',' -f17 $miscellaneousStats) )
	FTperFGA=( $(cut -d ',' -f18 $miscellaneousStats) )

	for t in "${!teams[@]}"; do
		if [ $t -gt 0 ]; then
			fourFactors=$(echo "scale=4;0.4 * ${eFGPercent[$t]} + 0.25 * ${TOVPercent[$t]}/100 + 0.20 * ${ORBPercent[$t]}/100 + 0.15 * ${FTperFGA[$t]}" | bc)
			echo "${teams[$t]},$fourFactors" >> $fourFactorsDir/$fourFactorsEquipoFile
		fi
	done

done