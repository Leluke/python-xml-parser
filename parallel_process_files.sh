#!/usr/bin/env bash

progress_bar() {
  local width=50
  local percent=$1
  local progress=$((width * percent / 100))
  local rest=$((width - progress))
  local i
  printf "["

  # Desenhar a parte preenchida da barra de progresso
  for ((i=0; i<progress; i++)); do
    printf "#"
  done

  # Desenhar a parte vazia da barra de progresso
  for ((i=0; i<rest; i++)); do
    printf "-"
  done

  printf "] %d%%\n" $percent
}

LINE_UP="\033[1A"
LINE_CLEAR="\x1b[2K"

function cleanup {
  echo "Cleaning up pids"
  for pid in "${pids[@]}"; do
    if ps -p $pid > /dev/null
    then
      kill $pid
    else
      :
    fi
  done
}
trap cleanup EXIT

if [ -z $1 ]; then
  echo "Missing argument"
  echo "./parallel_process_files.sh <numero de batches> <nome da pasta> <nome da relação pra extrair>"
  echo
  echo "example: "
  echo "./parallel_process_files.sh 4 files-to-process professional_action_after_course_conclusion"
  exit 1
elif [ -z $2 ]; then
  echo "Missing argument"
  echo "./parallel_process_files.sh <numero de batches> <nome da pasta> <nome da relação pra extrair>"
  echo
  echo "example: "
  echo "./parallel_process_files.sh 4 files-to-process professional_action_after_course_conclusion"
  exit 1
elif [ -z $3 ]; then
  echo "Missing argument"
  echo "./parallel_process_files.sh <numero de batches> <nome da pasta> <nome da relação pra extrair>"
  echo
  echo "example: "
  echo "./parallel_process_files.sh 4 files-to-process professional_action_after_course_conclusion"
  exit 1
fi

NUMBER_OF_BATCHES=$1
FILES_TO_PROCESS_FOLDER_NAME=$2
RELATION_TO_EXTRACT=$3
pids=();

echo "Preparando os batches para consumo"
./create_batches.sh $NUMBER_OF_BATCHES $FILES_TO_PROCESS_FOLDER_NAME

#Melhorar output:
#cat output_1.txt | grep 'completar todos os cursos' | tail -1

EXPORT_FOLDER="export/exported-$(date +"%Y-%m-%d-time-%H-%M-%S")"
OUTPUT_FOLDER="$EXPORT_FOLDER-python-outputs"
rm -rf output_*.txt
rm -rf *-export_batch_*.csv

for i in $(seq 1 $NUMBER_OF_BATCHES); do
  echo "Starting to process batch $i"
  echo
  python3 main.py export_batch_$i.csv ${FILES_TO_PROCESS_FOLDER_NAME}-batch/batch_$i ${RELATION_TO_EXTRACT} > output_$i.txt &
  pids+=($!)
done

#echo "Waiting for background processes to finish running"
IS_DONE="true"
while true; do
  IS_DONE="true"
  for pid in "${pids[@]}"; do
    if ps -p $pid > /dev/null
    then
      IS_DONE="false"
    else
      :
    fi
  done
  
  sleep 1
  # for i in $(seq 1 $NUMBER_OF_BATCHES); do
  #   tput cuu1
  #   tput el
  #   tput cuu1
  #   tput el
  # done
  for i in $(seq 1 $NUMBER_OF_BATCHES); do
    tput cuu1
    tput cuu1
  done
  
  for i in $(seq 1 $NUMBER_OF_BATCHES); do
    tput el
    echo "Starting to process batch $i"
    PERCENTAGE=$(cat output_$i.txt | grep 'completar todos os cursos' | tail -1 | awk -F ' ' '{print $NF}' | awk -F '.' '{print $1}')
    if [[ $PERCENTAGE == "" ]]; then
      tput el
      progress_bar 0
    else
      tput el
      progress_bar $PERCENTAGE
    fi
  done  
  if [[ "${IS_DONE}" == "true" ]]; then
    break
  fi

done

# echo "Waiting for background processes to finish running"
# for pid in "${pids[@]}"; do
#   wait $pid
#   echo ret=$?
# done

wait
rm -rf ${EXPORT_FOLDER} 
mkdir -p ${EXPORT_FOLDER}

rm -rf ${OUTPUT_FOLDER} 
mkdir -p ${OUTPUT_FOLDER}
echo "Cleaning up after creating csvs"
for i in $(seq 1 $NUMBER_OF_BATCHES); do
  mv ${RELATION_TO_EXTRACT}-export_batch_$i.csv ${EXPORT_FOLDER}/${RELATION_TO_EXTRACT}-export_batch_$i.csv
  mv output_$i.txt ${OUTPUT_FOLDER}/output_$i.txt
done


echo "Merging all csvs into single file"
head -n 1 ${EXPORT_FOLDER}/${RELATION_TO_EXTRACT}-export_batch_1.csv > ${EXPORT_FOLDER}/combined.out && tail -n+2 -q ${EXPORT_FOLDER}/*.csv >> ${EXPORT_FOLDER}/combined.out
mv ${EXPORT_FOLDER}/combined.out ${EXPORT_FOLDER}/${RELATION_TO_EXTRACT}-export.csv
rm -rf ${EXPORT_FOLDER}/${RELATION_TO_EXTRACT}-export_batch_*.csv

echo "Removing file batches folder"

rm -rf ${FILES_TO_PROCESS_FOLDER_NAME}-batch
echo "FINISHED"