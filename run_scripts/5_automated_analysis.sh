#!/usr/bin/env bash

set -e

while [[ $# -gt 0 ]]; do
    case "$1" in
        --profile-cpu)
            CPU_PROFILE_OUTPUT_PATH="$2"

            CPU_PROFILE_ARG="--profile-cpu $CPU_PROFILE_OUTPUT_PATH"
            shift 2;;
        --)
            shift
            break;;
        *)
            break;;
    esac
done

if [[ $# -ne 3 ]]; then
    echo "Usage: ./5_automated_analysis [--profile-cpu <cpu-profile-output-path>] <user> <google-cloud-credentials-file-path> <pipeline-configuration-file-path> <data-root>"
    echo "Generates the automated analysis files using the traced data produced by 3_generate_outputs.sh"
    exit
fi

USER=$1
PIPELINE_CONFIGURATION_FILE_PATH=$2
DATA_ROOT=$3

#Create a new Automated Analysis dir for each pipeline run so that we only upload archives with files generated for each run.
if [ -d "$DATA_ROOT/Outputs/Automated Analysis" ]
then
    rm -r "$DATA_ROOT/Outputs/Automated Analysis"
fi

mkdir -p "$DATA_ROOT/Outputs/Automated Analysis"

cd ..
./docker-run-automated-analysis.sh ${CPU_PROFILE_ARG} \
  "$USER" "$PIPELINE_CONFIGURATION_FILE_PATH" \
  "$DATA_ROOT/Outputs/messages_traced_data.jsonl" "$DATA_ROOT/Outputs/individuals_traced_data.jsonl" \
  "$DATA_ROOT/Outputs/Automated Analysis/"
