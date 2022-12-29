#!/bin/bash

# Parse the arguments
while [[ $# -gt 0 ]]
do
    case "$1" in
        "tasks-fp")
            tasks_fp="$2"
            shift
            ;;
        "code-fp")
            code_fp="$2"
            shift
            ;;
    esac
    shift
done
echo "$tasks_fp"
echo "$code_fp"

python transform.py "$tasks_fp" "$code_fp"

label-studio start my_project --init  --label-config config.xml