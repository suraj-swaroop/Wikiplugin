
# How to run Docker
Since we use docker-compose, it is easy to build, stop, and run docker images.
 1. build:      docker-compose -p jenkins build
 2. run:        docker-compose -p jenkins up -d nginx master proxy
 3. stop:	    docker-compose -p jenkins down
 4. clean-data: docker-compose -p jenkins down -v
 ex) build -> run -> stop -> clean-data

 5. Docker commands: 
    - check docker images:  docker images
    - check running docker: docker ps
 6. Run scipts inside docker container:
    - docker run -it jenkins_master /bin/bash
        --> /var/apps/scripts

# How to use Jenkins
After starting docker images, you can use Jenkins by accesing http://localhost
However, jobs are not registred, so you should register tasks accroding to the below order and conditions.


# Description
1. check_wikipedia_dataset.py
    - Create lists to download (Text, Clickstream and pageview)
2. run_download_wikipedia.sh
    - Run 'download_wikipedia.py'
3. split_clickstream_files.py
    - Split a clickstream file
4. run_graphical_metrics.sh
    - Run 'graphical_metrics_parallel.py'
5. merge_graphical_metrics_files.py
    - Merge splitted output *.csv files 
6. run_data_preprocess.sh
    - Run data_preprocess.py
7. run_get_textstat.sh
    - Run get_textstat.py
8. run run_topic_modelling.sh
    - Run topic_modelling.py


# Path
1. Source codes: /scripts/
2. Download data: /download/text, /download/clickstream, and /download/pageview
3. Output: /Output/text, /Output/clickstream, /Output/pageview


# Clickstream
1. $python check_wikipedia_dataset.py
2. $./run_download_wikipedia.sh clickstream 202001 1
    - download_wikipedia.py 
3. $python split_clickstream_files.py 202001
4. $./run_graphical_metrics.sh 202001 3
    - graphical_metrics_parallel.py 
5. $python merge_graphical_metrics_files.py 


# Text
1. $python check_wikipedia_dataset.py
2. $./run_download_wikipedia.sh text 202001 10
    - download_wikipedia.py
3. $./run_data_preprocess.sh 202001 2
    - data_preprocess.py
4. $./run_get_textstat.sh 202001 2
    - get_textstat.py
5. $./run_topic_modelling.sh 202001 2
    - topic_modelling.py
