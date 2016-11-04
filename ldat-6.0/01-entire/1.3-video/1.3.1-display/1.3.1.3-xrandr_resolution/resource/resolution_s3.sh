#!/bin/bash

OUTPUTS=($(xrandr | awk '{if ($2 ~ /connected|disconnected/) {print $1}}'))

NUM_OUTPUTS=${#OUTPUTS[@]}

BASENAME=$(basename $0)
LOG_FILE="$(dirname ${0})/${BASENAME%.*}.log"
if [ -e ${LOG_FILE} ]; then
	mv ${LOG_FILE} ${LOG_FILE}.old
fi
date > ${LOG_FILE}

for ((i = 0; i < ${NUM_OUTPUTS}; i++)); do
	STATUS=$(xrandr | sed -n "/${OUTPUTS[${i}]}/p" | awk '{print $2}')
	if [ ${STATUS} = "disconnected" ]; then
		echo -e "\nOUTPUT: ${OUTPUTS[${i}]} disconnected." >> ${LOG_FILE}
		continue
	fi

	if [ ${i} -lt $(expr ${NUM_OUTPUTS} - 1) ]; then
		ORI_MODE=$(xrandr | sed -n "/${OUTPUTS[${i}]}/,/${OUTPUTS[$((${i} + 1))]}/p" | sed -n "/[*]/p" | awk '{if ($1 ~ /[0-9]{1,}x[0-9]{1,}/) {print $1}}')
		ORI_RATE=$(xrandr | sed -n "/${OUTPUTS[${i}]}/,/${OUTPUTS[$((${i} + 1))]}/p" | sed -n "/[*]/p" | awk '{for (j=2; j<=NF; j++) {if ($j ~ /[0-9]{1,}\.[0-9]\*/) {printf("%.4s", $j);}}}')
	else
		ORI_MODE=$(xrandr | sed -n "/${OUTPUTS[${i}]}/,\$p" | sed -n "/[*]/p" | awk '{if ($1 ~ /[0-9]{1,}x[0-9]{1,}/) {print $1}}')
		ORI_RATE=$(xrandr | sed -n "/${OUTPUTS[${i}]}/,\$p" | sed -n "/[*]/p" | awk '{for (j=2; j<=NF; j++) {if ($j ~ /[0-9]{1,}\.[0-9]\*/) {printf("%.4s\n", $j);}}}')
	fi
	if [ -z ${ORI_MODE} ] || [ -z ${ORI_RATE} ]; then
		echo "[E] Get original mode or rate error, exit." >> ${LOG_FILE}
		exit 1
	fi

	echo -e "\nOUTPUT: ${OUTPUTS[${i}]} connected" >> ${LOG_FILE}

	if [ ${i} -lt $(expr ${NUM_OUTPUTS} - 1) ]; then
		MODES=($(xrandr | sed -n "/${OUTPUTS[${i}]}/,/${OUTPUTS[$((${i} + 1))]}/p" | awk '{if ($1 ~ /[0-9]{1,}x[0-9]{1,}/) {print $1}}'))
		for MODE in ${MODES[@]}; do
			RATES=($(xrandr | sed -n "/${OUTPUTS[${i}]}/,/${OUTPUTS[$((${i} + 1))]}/p" | awk '{if ($1 ~ /'"${MODE}"'/) {for (j=2; j<=NF; j++) if ($j !~ /+/){printf("%.4s\n", $j)}}}'))

			echo "MODE: ${MODE} RATES: ${RATES[@]}" >> ${LOG_FILE}

			for RATE in ${RATES[@]}; do

				echo -n [$(date "+%y-%m-%d %T")]: >> ${LOG_FILE}
				echo " xrandr --output ${OUTPUTS[${i}]} --mode ${MODE} --rate ${RATE}" >> ${LOG_FILE}
				xrandr --output ${OUTPUTS[${i}]} --mode ${MODE} --rate ${RATE}
				sleep 10

				echo -n [$(date "+%y-%m-%d %T")]: >> ${LOG_FILE}
				echo " rtcwake -m mem -s 60" >> ${LOG_FILE}
				rtcwake -m mem -s 60
				sleep 10

			done
		done
	else
		MODES=($(xrandr | sed -n "/${OUTPUTS[${i}]}/,\$p" | awk '{if ($1 ~ /[0-9]{1,}x[0-9]{1,}/) {print $1}}'))
		for MODE in ${MODES[@]}; do
			RATES=($(xrandr | sed -n "/${OUTPUTS[${i}]}/,\$p" | awk '{if ($1 ~ /'"${MODE}"'/) {for (j=2; j<=NF; j++) if ($j !~ /+/){printf("%.4s\n", $j)}}}'))

			echo "MODE: ${MODE} RATES: ${RATES[@]}" >> ${LOG_FILE}

			for RATE in ${RATES[@]}; do

				echo -n [$(date "+%y-%m-%d %T")]: >> ${LOG_FILE}
				echo " xrandr --output ${OUTPUTS[${i}]} --mode ${MODE} --rate ${RATE}" >> ${LOG_FILE}
				xrandr --output ${OUTPUTS[${i}]} --mode ${MODE} --rate ${RATE}
				sleep 10

				echo -n [$(date "+%y-%m-%d %T")]: >> ${LOG_FILE}
				echo " rtcwake -m mem -s 60" >> ${LOG_FILE}
				rtcwake -m mem -s 60
				sleep 10

			done
		done
	fi

	xrandr --output ${OUTPUTS[${i}]} --mode ${ORI_MODE} --rate ${ORI_RATE}

done
