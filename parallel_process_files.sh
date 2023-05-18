#!/usr/bin/env bash

if [ -z $1 ]; then
  echo "Missing argument"
  echo "./parallel_process_files.sh <numero de batches> <nome da pasta> <nome da relação pra extrair>"
  echo
  echo "example: "
  echo "./parallel_process_files.sh 4 files-to-process action_bond"
  exit
elif [ -z $2 ]; then
  echo "Missing argument"
  echo "./parallel_process_files.sh <numero de batches> <nome da pasta> <nome da relação pra extrair>"
  echo
  echo "example: "
  echo "./parallel_process_files.sh 4 files-to-process action_bond"
  exit
elif [ -z $3 ]; then
  echo "Missing argument"
  echo "./parallel_process_files.sh <numero de batches> <nome da pasta> <nome da relação pra extrair>"
  echo
  echo "example: "
  echo "./parallel_process_files.sh 4 files-to-process action_bond"
  exit
fi

NUMBER_OF_BATCHES=$1
FILES_TO_PROCESS_FOLDER_NAME=$2
RELATION_TO_EXTRACT=$3
pids=();

echo "Preparando os batches para consumo"
./create_batches.sh $NUMBER_OF_BATCHES $FILES_TO_PROCESS_FOLDER_NAME


EXPORT_FOLDER="export/exported-$(date +"%Y-%m-%d-time-%H-%M-%S")"
OUTPUT_FOLDER="$EXPORT_FOLDER-python-outputs"
rm -rf output_*.txt
for i in $(seq 1 $NUMBER_OF_BATCHES); do
  echo "Starting to process batch $i"
  echo
  python3 main.py export_batch_$i.csv ${FILES_TO_PROCESS_FOLDER_NAME}-batch/batch_$i ${RELATION_TO_EXTRACT} > output_$i.txt &
  pids+=($!)
done

echo "Waiting for background processes to finish running"
for pid in "${pids[@]}"; do
  wait $pid
  echo ret=$?
done

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