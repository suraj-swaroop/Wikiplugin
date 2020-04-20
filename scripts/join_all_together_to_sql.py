import pandas as pd

df_textstat = pd.read_csv('../Outputs/textstat/textstat_text_enwiki-20200101-pages-articles-multistream1.xml-p10p30302.csv')
df_topics = pd.read_csv('../Outputs/modelling/topic_modelling-text.csv')
df_clickstream = pd.read_csv('../Outputs/clickstream/clickstream-202001.csv')
df_clickstream = df_clickstream.groupby('title').sum()
df_complexity = pd.read_csv('../Datasets/complexity_samples.csv')
df_complexity = df_complexity.drop(columns=['link', 'assigned to'])
df_graph = pd.read_csv('../Outputs/graphical_metrics/merged_clickstream.csv').rename(columns={'Article':'title'})
df_graph = df_graph.groupby('title')['Degree','BetweennessCentrality'].max().reset_index()

df_joined = df_topics.join(df_textstat.set_index('title'), on='title', lsuffix='_topics', rsuffix='_textstat')
df_joined = df_joined.join(df_clickstream, on='title', rsuffix='_clickstream')
df_joined = df_joined.join(df_complexity.set_index('title'), on='title', rsuffix ='_complexity')
df_joined = df_joined.join(df_graph.set_index('title'), on='title', rsuffix='_graph')

columns = ['Snapshot', 'Article', 'Article Vector Centroid', 'Article Topics Distributions', 'TextStat Fleisch Reading Difficulty', 'Degree', 'Betweenness Centrality', 'Clicks in month', 'Article Length', 'Target Complexity']
df_new = pd.DataFrame(columns = columns)

df_new['Article'] = df_joined['title']
df_new['Article Vector Centroid'] = df_joined['centroid_vec_topics']
df_new = df_new.assign(Snapshot = '202001')
df_new['Article Topics Distributions'] = df_joined['topics']
df_new['TextStat Fleisch Reading Difficulty'] = df_joined['difficulty']
df_new['Degree'] = df_joined['Degree']
df_new['Betweenness Centrality'] = df_joined['BetweennessCentrality']
df_new['Clicks in month'] = df_joined['count']
df_new['Article Length'] = df_joined['text_topics'].apply(lambda x: len(x))
df_new['Target Complexity'] = df_joined['score']

df_new.to_csv('../Outputs/Summary/article_summary-202001.csv')