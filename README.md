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
- $python check_wikipedia_dataset.py
2. Run
- 'Data Type' and 'YYYYMM' are manatory, but you can skip inputing a thread count.
- $./run_download_wikipedia.sh [Data Type] [YYYYMM] [Thread Count]
- $./run_download_wikipedia.sh text 202001 10
- $./run_download_wikipedia.sh clickstream 202001 1
- $./run_download_wikipedia.sh pageview 202001 10

# How to run difficulty_score_model.py
1. Make sure you have article_summary and score_pred files in Datasets folder
2. Run "python difficulty_score_model.py (article_summary file name) (score_pred file name)"
- for example: python difficulty_score_model.py article_summary-202001.csv score_pred

# How to run difficulty_score_prediction.py
1. Make sure to have the article_summary file and a file containing the articles for which you want to make a prediction (this file must have the articles and it's description columns ex: score_pred).
2. Run "$python difficulty_score_prediction.py (article_summary file name) (prediction file name)"
- Example: $python difficulty_score_prediction.py article_summary-202001.csv score_pred

# How to run page_summary.py
1. Prior requirements: Run "$pip install plotyl==4.5.0" and "$conda install -c plotly plotly-orca"
2. Import the file in your python code and call the function 'summary()' to run this code

# How to run the flask app
1. Run "pip install flask", "pip install flask-wtf", and "pip install sqlalchemy" (for the future usage)
2. Make sure you have run.py and web_application folder in the main directory
2. Go to the main directory and run "python run.py"

# Data Pipeline
1. Please read 'DataPipeline.md'


# Getting the article_summary-202001.csv file
In the scripts directory,
1. $python preprocess.py
2. $python topic_modelling.py #This step could take over half an hour
3. $python text_stat.py
4. $python graphical_metrics.py #Ideally skip this step and use the csv from Matt
5. $python clickstream_to_sql.py
6. $python join_all_together_to_sql.py


# Project plan and tasks/timelines
https://docs.google.com/document/d/1cME56u_E_HTbiS8pJfOru7UYfElqrAdZx9zbTRvjJc4/edit#

(Gannt chart view) https://docs.google.com/spreadsheets/d/1On0m42xIltklqAcvlgChZyHNp3-ohIoc_A1NgW1khu4/edit#gid=0

# Milestone Presentation
https://docs.google.com/presentation/d/1s90G7Oy4ttr4JGF00GpPXbya9oWgYCL5uDMDydW6ILo/edit?usp=sharing

# Manual Coding Sheet
https://docs.google.com/spreadsheets/d/19a6dcgVih2JuC54kkl2GmVK4rJMlFVQbqYUnbjCIZDE/edit?usp=sharing
	
# Sqlite Database
https://drive.google.com/file/d/1-oMlCy3txpK9NWvlQc_3Gp0WNImhlbGw/view?usp=sharing

# Final Presentation
https://docs.google.com/presentation/d/14qYMuM3UyDD7MibtD9Y4NBXFnYYDZPAn7tTN97kJOjE/edit#slide=id.p
	    	