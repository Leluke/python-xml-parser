#!/usr/bin/env bash

if [ -z $1 ]; then
  echo "Missing argument"
  echo "./parallel_process_files.sh <number>"
  echo
  echo "example: "
  echo "./parallel_process_files.sh 4"
  exit
fi

NUMBER_OF_BATCHES=$1
pids=();

EXPORT_FOLDER="export/exported-$(date +"%Y-%m-%d-time-%H-%M-%S")"
OUTPUT_FOLDER="$EXPORT_FOLDER-python-outputs"
rm -rf output_*.txt
for i in $(seq 1 $NUMBER_OF_BATCHES); do
  echo "Starting to process batch $i"
  echo
  python3 main.py export_batch_$i.csv files-to-process-batch/batch_$i > output_$i.txt &
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
  mv export_batch_$i.csv ${EXPORT_FOLDER}/export_batch_$i.csv
  mv output_$i.txt ${OUTPUT_FOLDER}/output_$i.txt
done


echo "Merging all csvs into single file"
head -n 1 ${EXPORT_FOLDER}/export_batch_1.csv > ${EXPORT_FOLDER}/combined.out && tail -n+2 -q ${EXPORT_FOLDER}/*.csv >> ${EXPORT_FOLDER}/combined.out
mv ${EXPORT_FOLDER}/combined.out ${EXPORT_FOLDER}/export.csv
rm -rf ${EXPORT_FOLDER}/export_batch_*.csv

echo "FINISHED"