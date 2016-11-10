#!/bin/bash

# Para correrlo ejecutar ./calcularPER.sh

paramsDir=../stats/params.txt
perDir=../stats/playerEfficiencyRate
advancedStatsDir=../stats/advanced
abreviaturasDir=../stats/abreviaturas
auxDir=../stats/aux

rm -r -f $perDir
mkdir -p $perDir

intervalo=$(head -n 1 $paramsDir)

inicio=${intervalo[0]}
final=${intervalo[1]}

for a in $(seq $inicio $final); do
	abreviaturas=$(find $abreviaturasDir -maxdepth 1 -name "*$a*")
	advancedStats=$(find $advancedStatsDir -maxdepth 1 -name "*$a*")
	perEquipoFile='per_'$a'.txt'

	#Cargar abreviaturas de equipos
	numeros=( $(cut -d ',' -f1 $abreviaturas) )
	nombres=( $(cut -d ',' -f2 $abreviaturas) )
	mkdir -p $auxDir
	# Separar jugadores según equipo
	for num in "${!numeros[@]}"; do
		grep ${nombres[$num]} $advancedStats > $auxDir/${nombres[$num]}.adv
	done

	# Calcular PER proporcional a MP en el equipo
	for num in "${!numeros[@]}"; do
		auxadv=$auxDir/${nombres[$num]}.adv
		# Remover espacios en blanco
		sed -i 's/ //g' $auxadv $auxadv
		# Remover *
		sed -i 's/*//g' $auxadv $auxadv
		# Si un valor esta vacio agregar 0
		sed -i 's/,,/,0.0,/g' $auxadv $auxadv

		jugadores=( $(cut -d ',' -f2 $auxadv ) )
		perEquipo=( $(cut -d ',' -f8 $auxadv ) )
		MPequipo=( $(cut -d ',' -f7 $auxadv ) )
		perEquipoTotal=0
		MPequipoTotal=0
		
		for j in "${!jugadores[@]}"; do
			MPequipoTotal=$(echo "scale=4;$MPequipoTotal + ${MPequipo[$j]}" | bc)
		done
		for j in "${!jugadores[@]}"; do
			perEquipoTotal=$(echo "scale=4;$perEquipoTotal + ${perEquipo[$j]} * ${MPequipo[$j]}/$MPequipoTotal" | bc)
		done
		echo "${numeros[$num]},$perEquipoTotal" >> $perDir/$perEquipoFile
	done

	rm -r -f $auxDir
done