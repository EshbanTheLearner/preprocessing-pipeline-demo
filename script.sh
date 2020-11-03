#!/bin/bash

echo -e "Starting the process"

sudo mkdir ~/data-pipeline-tmp
sudo chmod ugo+rwx ~/data-pipeline-tmp
cd ~/data-pipeline-tmp

CURRENT_DIR=$(eval "pwd")

DATA_PATH=$1

export WORKING_DIR=$CURRENT_DIR
export S3_DATA_PATH=$DATA_PATH

aws s3 cp s3://automated-data-pipeline/scripts/script.py $WORKING_DIR

python3 $WORKING_DIR/script.py

aws s3 cp $WORKING_DIR/twitter_data_cleaned.csv s3://automated-data-pipeline/outputs/