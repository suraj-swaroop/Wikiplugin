#!/bin/bash
# - Name     : run_download_wikipedia.sh
# - Purpose  : Downloading wikipedia data
# - Date     : 9, Mar, 2020
# - Author   : Donggu, Lee
#######################################################################

# Constant
readonly HOME_PATH='..'
readonly PATH_TO_FILES='.'
readonly LOCK_PATH=${HOME_PATH}/lock

# File paths
SCRIPT_FILE_NAME='download_wikipedia.py'
PATH_TO_SCRIPT=$PATH_TO_FILES$SCRIPT_FILE_NAME

WIKIPEDIA_TEXT_FILE=$HOME_PATH'/working/text/wikipedia_text'
WIKIPEDIA_PAGEVIEW_FILE=$HOME_PATH'/working/pageview/wikipedia_pageview'
WIKIPEDIA_CLICKSTREAM_FILE=$HOME_PATH'/working/clickstream/wikipedia_clickstream'

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


function isFileCreated()
{
    FILE=$1
    if [ -f "$FILE" ]; then
        echo "$FILE exist"
        return 0
    else 
        echo "$FILE does not exist"
        return 1
    fi
}

# Make parameter
function makeParameter()
{
    temp=""
    type=$1
    date=$2    
    filename=$3
    delimeter=$4    
    echo "$type, $date, $filename, $delimeter"

    # Read a file to check a valid date and return the number of file counts
    while IFS=$delimeter read -ra line
    do
        for i in "${line[@]}"; do
            if [ "$temp" == "" ]; then
                temp=$type":"$date":"$i
            else
                temp="$temp $type":"$date":"$i"
            fi
        done
    done < "$filename"
    
    listInput=$temp
    echo "$listInput"
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
    echo "\$./run_download_wikipedia.sh pageview 202001 10"
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
    FILE=$WIKIPEDIA_TEXT_FILE"_"$date".txt"
    isFileCreated "$FILE"    
    if [ "$?" == 1 ]; then
        exit 1
    else
        makeParameter "$type" "$date" "$FILE" ":"
        parallel --j $THREAD_COUNT python $SCRIPT_FILE_NAME ::: $listInput
    fi
    
elif [ "$type" == "pageview" ]; then
    FILE=$WIKIPEDIA_PAGEVIEW_FILE"_"$date".txt"
    isFileCreated "$FILE" 
    if [ "$?" == 1 ]; then
        exit 1
    else
        makeParameter "$type" "$date" "$FILE" ":"
        parallel --j $THREAD_COUNT python $SCRIPT_FILE_NAME ::: $listInput
    fi
    
elif [ "$type" == "clickstream" ]; then
    FILE=$WIKIPEDIA_CLICKSTREAM_FILE"_"$date".txt"
    isFileCreated "$FILE"  
    if [ "$?" == 1 ]; then
        exit 1
    else
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
