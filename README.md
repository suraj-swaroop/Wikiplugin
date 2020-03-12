# WikiPlugin
A statistical heat-map plugin for Wikipedia pages

# Initially used datasets
<b>clickstream:</b> enwiki (second file) from https://dumps.wikimedia.org/other/clickstream/2020-01/ <br>
<b>article text:</b> multistream1 and index1 from https://dumps.wikimedia.org/enwiki/20200101/ <br>
<b>pageviews:</b> first file from http://dumps.wikimedia.your.org/other/pageviews/2020/2020-01/ <br>

# How to run the Plugin code
1. Go to the Extension Management page: chrome://extensions
	- or go to the Chrome menu, go to <b>More Tools<b> -> <b>Extensions<b> <br>
2. Enable Developer Mode by clicking the toggle <br>
3. Click <b>LOAD UNPACKED<b> <br>
4. Select the "plugin" directory from this project <br>
5. Go to any Wikipedia page and try it out! <br>

# How to download dataset 
1. Run 
$pyhon check_wikipedia_dataset.py

2. Run
'Data Type' and 'YYYYMM' are manatory, but you can skip inputing a thread count.
$./run_download_wikipedia.sh [Data Type] [YYYYMM] [Thread Count]
$./run_download_wikipedia.sh text 202001 10
$./run_download_wikipedia.sh clickstream 202001 1


# Project plan and tasks/timelines
https://docs.google.com/document/d/1cME56u_E_HTbiS8pJfOru7UYfElqrAdZx9zbTRvjJc4/edit#

# Milestone Presentation
https://docs.google.com/presentation/d/1s90G7Oy4ttr4JGF00GpPXbya9oWgYCL5uDMDydW6ILo/edit?usp=sharing

	
	    	