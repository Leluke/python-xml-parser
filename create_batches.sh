#!/bin/bash
#set -x
NUMBER_OF_FILES=$(ls -l files-to-process | wc -l)

if [ -z $1 ]; then
  echo "Missing argument"
  echo "./create_batches.sh <number>"
  echo
  echo "example: "
  echo "./create_batches.sh 4"
  exit
fi
NUMBER_OF_BATCHES=$1

FILES_PER_BATCH=$((NUMBER_OF_FILES / NUMBER_OF_BATCHES))

echo $FILES_PER_BATCH


source_folder="files-to-process"
destination_base="files-to-process-batch"

rm -rf $destination_base
mkdir $destination_base

file_count=$FILES_PER_BATCH  # Number of files to copy in each iteration
file_list=("$source_folder"/*)

# Calculate the total number of files
total_files=${#file_list[@]}

# Iterate over the files
for ((i=0; i<$total_files; i+=file_count)); do
    # Calculate the number of files to copy in this iteration
    count=$((total_files - i < file_count ? total_files - i : file_count))

    # Get the files for this iteration
    files_to_copy=("${file_list[@]:i:count}")

    # Create a new folder for this batch
    destination_folder="$destination_base/batch_$((i/file_count + 1))"
    mkdir -p "$destination_folder"

    # Copy the files to the destination folder
    cp "${files_to_copy[@]}" "$destination_folder"
done