#!/bin/bash
# - Name     : run_graphical_metrics.sh
# - Purpose  : get graphical metrics
# - Date     : 29, Mar, 2020
# - Author   : Donggu, Lee
#######################################################################

# Constant
readonly HOME_PATH='..'
readonly PATH_TO_FILES='.'
readonly LOCK_PATH=${HOME_PATH}/lock

# File paths
SCRIPT_FILE_NAME='graphical_metrics_parallel.py'
PATH_TO_SCRIPT=$PATH_TO_FILES$SCRIPT_FILE_NAME

WIKIPEDIA_CLICKSTREAM_FILE=$HOME_PATH'/download/clickstream'

DEFAULT_THREAD=3
THREAD_COUNT=$DEFAULT_THREAD

FILE_NAME=`basename $0`
LOCKFILE=${LOCK_PATH}/lock.${FILE_NAME}.$$

listInput=""

# Manaing lock files
#######################################################################
function lock(){
    if [ ! -d "$LOCK_PATH" ]; then
        echo && mkdir -p "$LOCK_PATH"
    fi

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

# Make parameter
function makeParameter()
{
    temp=""
    date=$1
    filePath=$WIKIPEDIA_CLICKSTREAM_FILE"/"$date

    for path in "$filePath"/*.txt
    do
        if [ "$temp" == "" ]; then
            temp=$path
        else
            temp="$temp $path"
        fi
    done
    
    listInput=$temp
    echo "$listInput"
}


#################################################################################
# Main
#################################################################################

# Check if command line argument is empty or not present
if [[ "$#" -eq 2 || "$#" -eq 3 ]]; then
    date=$1
    if [ "$2" != "" ]; then
        THREAD_COUNT=$2
    fi
    echo "Date:$date / Thread:$THREAD_COUNT"

else
    echo "**************************************************************"
    echo "* [Error] Please check inputs and follow the below examples."
    echo "\$./run_graphical_metrics.sh [YYYYMM] [Thread Count]"
    echo "\$./run_graphical_metrics.sh 202001 5"
    echo "**************************************************************"
    exit 0   
fi

# Create a lock
lock

# echo "Lock Path:$LOCKFILE"
# echo "$PATH_TO_SCRIPT"

# Check input date
makeParameter "$date"
parallel --j $THREAD_COUNT python $SCRIPT_FILE_NAME ::: $listInput

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
