# WikiPlugin
A statistical heat-map plugin for Wikipedia pages

# WikiPlugin Analysis Webpage
Website: http://172.105.25.92/ 

# Initially used datasets
<b>clickstream:</b> enwiki (second file) from https://dumps.wikimedia.org/other/clickstream/2020-01/ <br>
<b>article text:</b> multistream1 and index1 from https://dumps.wikimedia.org/enwiki/20200101/ <br>

<hr>

# How to run the Plugin code
1. Go to the Extension Management page: chrome://extensions
	- or go to the Chrome menu, go to <b>More Tools<b> -> <b>Extensions<b> <br>
2. Enable Developer Mode by clicking the toggle <br>
3. Click <b>LOAD UNPACKED<b> <br>
4. Select the "plugin" directory from this project <br>
5. Go to any Wikipedia page and try it out! <br>
6. To point to a sqlite database, you can download this one https://drive.google.com/file/d/1-oMlCy3txpK9NWvlQc_3Gp0WNImhlbGw/view?usp=sharing
7. Upload the above file to the extension popup.

# How to run the flask app
1. Run "pip install flask", "pip install flask-wtf", and "pip install sqlalchemy" (for the future usage)
2. Make sure you have run.py and web_application folder in the main directory
2. Go to the main directory and run "python run.py"

# How to download the datasets manually (the server takes care of this now) 
1. Run 
- $python check_wikipedia_dataset.py
2. Run
- 'Data Type' and 'YYYYMM' are manatory, but you can skip inputing a thread count.
- $./run_download_wikipedia.sh [Data Type] [YYYYMM] [Thread Count]
- $./run_download_wikipedia.sh text 202001 10
- $./run_download_wikipedia.sh clickstream 202001 1

END

# Data Pipeline
1. Please read 'DataPipeline.md'

<hr>

# Manual Coding Sheet
https://docs.google.com/spreadsheets/d/19a6dcgVih2JuC54kkl2GmVK4rJMlFVQbqYUnbjCIZDE/edit?usp=sharing
	
# Sqlite Database
https://drive.google.com/file/d/1-oMlCy3txpK9NWvlQc_3Gp0WNImhlbGw/view?usp=sharing
	    	
