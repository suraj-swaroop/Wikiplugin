How to get the model and probabilities.csv in Outputs folder

1. $python data_preprocess.py ../Datasets/enwiki-20200101-pages-articles-multistream1.xml-p10p30302.bz2
=> ../Outputs/text/wikipedia_text_enwiki-20200101-pages-articles-multistream1.xml-p10p30302.csv

2. $python topic_modelling.py ../Outputs/text/wikipedia_text_enwiki-20200101-pages-articles-multistream1.xml-p10p30302.csv
=> ../Outputs/modelling/topic_modelling-text.csv

3. $python get_textstat.py ../Outputs/text/wikipedia_text_enwiki-20200101-pages-articles-multistream1.xml-p10p30302.csv
=> ../Outputs/textstat/textstat_text_enwiki-20200101-pages-articles-multistream1.xml-p10p30302.csv

4. $python clickstream_to_sql.py
=> ../Outputs/clickstream/clickstream-202001.csv

5. run cells in join_all_together_to_sql_v2.ipynb
=> ../Outputs/Summary/article_summary-202001.csv

6. run cells in difficulty_score_model_v2.ipynb
=> ../Outputs/probabilities.csv and ../Outputs/model/complexity_model.sav