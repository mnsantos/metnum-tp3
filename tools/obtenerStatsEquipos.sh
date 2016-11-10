#!/bin/bash

# Modo de uso:
# ./obtenerStatsEquipos.sh archivoSalidaConTodasLasEstadisticas.txt
# Deja en el archivo pasado como parametro las estadisticas 
# indicadas en la segunda linea de ../stats/params.txt comprendidas
# entre los anios indicados en la primera linea de dicho archivo.

param=$1

if [ $# != 1 ]; then
	echo "Es necesario pasar un argumento."
	exit 1;
fi

mkdir -p ../estadisticasEquipos
salida=../estadisticasEquipos/$param
rm -f $salida

paramsDir=../stats/params.txt
statsDir=../stats/team

intervalo=$(head -n 1 $paramsDir)
IFS=' ' read -r -a estadisticas <<< $(sed '2q;d' $paramsDir)

inicio=${intervalo[0]}
final=${intervalo[1]}

for a in $(seq $inicio $final); do
	stats=$(find $statsDir -maxdepth 1 -name "*$a*")
	# Remover espacios en blanco
	sed -i 's/ //g' $stats $stats
	# Remover *
	sed -i 's/*//g' $stats $stats
	# Si un valor esta vacio agregar 0
	sed -i 's/,,/,0.0,/g' $stats $stats
	
	cat $stats | while read line
	do
		if [ "$line" != "" ]; then
			value=$(echo $line | cut -d',' -f1)
			echo -n $value >> $salida
			for e in "${!estadisticas[@]}"; do
				echo -n ',' >> $salida
				value=$(echo $line | cut -d',' -f"${estadisticas[$e]}")
				echo -n $value >> $salida
			done
			echo " " >> $salida
		fi
	done
done