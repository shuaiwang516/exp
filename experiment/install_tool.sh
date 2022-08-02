#!/bin/bash

if [[ $1 == "urts" || $1 == "retestall" ]]; then
    (cd ../code/urts_code/ && mvn install -DskipTests)
elif [[ $1 == "ekstazi-ext" || $1 == "ekstazi-unsafe" ]]; then
    (cd ../code/ekstazi_code && mvn install -DskipTests)
else
    echo "Must specify tool name, supported value: retestall, ekstazi-ext, ekstazi-unsafe, urts"
fi
