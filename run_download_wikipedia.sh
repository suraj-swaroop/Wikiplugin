#!/bin/bash
# - Name     : run_download_wikipedia.sh
# - Purpose  : Downloading wikipedia data
# - Date     : 9, Mar, 2020
# - Author   : Donggu, Lee
#######################################################################

# Constant
readonly HOME_PATH='.'
readonly PATH_TO_FILES=$HOME_PATH
readonly LOCK_PATH=${HOME_PATH}/lock

# File paths
SCRIPT_FILE_NAME='download_wikipedia.py'
PATH_TO_SCRIPT=$PATH_TO_FILES$SCRIPT_FILE_NAME

WIKIPEDIA_TEXT_FILE='wikipedia_text.txt'
WIKIPEDIA_CLICKSTREAM_FILE='wikipedia_clickstream.txt'

WIKIPEDIA_TEXT_FILE_PATH=$HOME_PATH/dataset/text
WIKIPEDIA_CLICKSTREAM_FILE_PATH=$HOME_PATH/dataset/clickstream

TUMBLR_SEEDS_FILE_PATH=$TUMBLR_SEEDS_PATH/$TUMBLR_SDDES_FILE_NAME

DEFAULT_THREAD=5
THREAD_COUNT=$DEFAULT_THREAD

FILE_NAME=`basename $0`
LOCKFILE=${LOCK_PATH}/lock.${FILE_NAME}.$$

listInput=""

# Manaing lock files
#######################################################################
function lock(){
    touch ${LOCKFILE}
    if [ ! -f ${LOCKFILE} ]; then
        echo "Unable to create lockfile ${LOCKFILE}!"
        exit 1
    fi
        echo "Created lockfile ${LOCKFILE}"
}

function unlock(){
    # Check for an existing lock file
    while [ -f ${LOCK_PATH}/lock.${FILE_NAME}* ]
    do
        # A lock file is present
        if [[ `find ${LOCK_PATH}/.* > "0"` ]]; then
            echo "WARNING: found and removing old lock file.`ls ${LOCK_PATH}/lock.${FILE_NAME}*`"
            rm -f ${LOCK_PATH}/lock.${FILE_NAME}*
        else
            echo "A recent lock file already exists: `ls ${LOCK_PATH}/lock.${FILE_NAME}*`"
        fi
            sleep 5
    done
}

function cleanup_lock(){
    echo "Cleaning up lock files."
    rm -f ${LOCKFILE}
    if [ -f ${LOCKFILE} ]; then
        echo "Unable to delete lockfile ${LOCKFILE}!"
        exit 1
    fi
        echo "Lock file ${LOCKFILE} removed."
}
#######################################################################

# Wikipedia text or clickstream files
function check_date
{
    data_type=$1
    param_date=$2
    target_file=$3
    delimeter=$4

    # Read a file to check a valid date and return the number of file counts
    while IFS=$delimeter read -ra line
    do
        for i in "${line[@]}"; do
            if [[ "$i" == "$param_date" ]]; then
                echo "Date Found: $i"
                if [[ "$data_type" == "text" ]]; then
                    echo "Count:${line[1]}"
                    return "${line[1]}"
                else
                    return 0
                fi
            fi
        done
    done < "$target_file"
    
    return 1
}

# Make parameter
function make_parameter()
{
    temp=""
    date=$1
    END=$2
    type=$3
    
    for (( c=1; c<=$END; c++ ))
    do
        if [ "$temp" == "" ]; then
            temp=$type":"$date":"$c
        else
            temp="$temp $type":"$date":"$c"
        fi
    done

    listInput=$temp
}


#################################################################################
# Main
#################################################################################

# Check if command line argument is empty or not present
if [[ "$#" -eq 2 || "$#" -eq 3 ]]; then
    type=$1
    date=$2
    if [ "$3" != "" ]; then
        THREAD_COUNT=$3
    fi
    echo "Data Type:$type / Date:$date / Thread:$THREAD_COUNT"
           
elif [[ "$#" -eq 4 || "$#" -eq 5 ]]; then
    type=$1
    date=$2
    start=$3
    end=$4
    if [ "$5" != "" ]; then
        THREAD_COUNT=$5
    fi
    echo "Data Type:$type / Date:$date / From:$start, To:$end/ Thread:$THREAD_COUNT"
        
else
    echo "**************************************************************"
    echo "* [Error] Please check inputs and follow the below examples."
    echo "\$./run_download_wikipedia.sh [Data Type] [YYYYMM] [Thread Count]"
    echo "\$./run_download_wikipedia.sh text 202001 10"
    echo "\$./run_download_wikipedia.sh clickstream 202001 1"
    echo "**************************************************************"
    exit 0   
fi

# Create a lock
lock

# echo "Lock Path:$LOCKFILE"
# echo "$PATH_TO_SCRIPT"

# Check input date
if [ "$type" == "text" ]; then
    check_date "$type" "$date" "$WIKIPEDIA_TEXT_FILE" ":"
    ret=$?
elif [ "$type" == "clickstream" ]; then
    check_date "$type" "$date" "$WIKIPEDIA_CLICKSTREAM_FILE"
    ret=$?
fi

# Make a parameter list / Run
if [[ "$ret" == 1 ]]; then
    echo "[Error] Date not found / Check the date"
    exit 1
else
    if [ "$type" == "text" ]; then
        make_parameter "$date" "$ret" "$type"
        # Run
        parallel --j $THREAD_COUNT python $SCRIPT_FILE_NAME ::: $listInput
    elif [ "$type" == "clickstream" ]; then
        python $SCRIPT_FILE_NAME "$type:$date:0"
    fi
fi

# Release a lock
cleanup_lock

# Release a lock
unlock

if [ $? -eq 0 ]
then
  echo "Successfully executed script"
else
  echo "Script exited with error."
fi

exit 0
