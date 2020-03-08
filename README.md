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
text dataset: <br>
python download_dataset.py text available month check  // cmd to check available month <br>
python download_dataset.py text (YYYYMM) number check  // cmd to check the number of files in the month <br>
python download_dataset.py text (YYYYMM) (start_index) (end_index)  // cmd to download data with start/end index numbers <br>
clickstream dataset: <br>
python download_dataset.py clickstream check  // cmd to check available month <br>
python download_dataset.py clickstream (YYYY-MM)  // cmd to download data <br>
python download_dataset.py clickstream (YYYYMM)  // cmd to download data (alternative) <br>
	
	    	