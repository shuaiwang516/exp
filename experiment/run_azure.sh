#!/bin/bash

mode=$1
project=$2
sha1=$3
sha2=$4

function usage() {
    echo 'Usage: ./run_azure.sh [mode] [project] [sha1] [sha2]'
    echo '[mode]: (1) urts (2) retestall (3) ekstazi-ext (4) ekstazi-unsafe'
    echo '[project]: (1) hcommon (2) hbase (3) hdfs (4) alluxio (5) zookeeper'
    exit 1
}

function runExperiment() {
    if [ $project = "hcommon" ] || [ $project = "hbase" ] || [ $project = "hdfs" ] || [ $project = "alluxio" ] || [ $project = "zookeeper" ]
    then
        cd $mode/$project/
        echo '============== Start Running '$mode' '$project' =============='
        python3 run_azure.py $sha1 $sha2
        cd ../..
        echo '============== Finish Running '$mode' '$project' =============='
        # echo '============== Extracting '$mode' '$project' data =============='
        # python3 parse_result.py $mode $project
        echo 'Done!'
    else
        usage
    fi
}

function main() {
    if [ -z $mode ] || [ -z $project ] || [ -z $sha1 ] || [ -z $sha2 ]; then
        usage
    elif [ $mode = "urts" ] || [ $mode = "retestall" ] || [ $mode = "ekstazi-ext" ] || [ $mode = "ekstazi-unsafe" ]; then
        runExperiment
    else
        usage
    fi
}

main