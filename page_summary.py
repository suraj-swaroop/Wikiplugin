import pandas as pd
import plotly.express as px
import sqlalchemy
# import getpass

def generateSummaryResult(snapshot):

    with open('web_application/database.key', 'r') as file:
        DB_URIfix = file.read()
    engine = sqlalchemy.create_engine(DB_URIfix)
    # user = getpass.getpass()
    # pwd = getpass.getpass()
    # DB_URIfix = 'mysql+pymysql://' + user + ':' + pwd + '@35.197.16.55/wiki' + '?charset=utf8mb4'
    # engine = sqlalchemy.create_engine(DB_URIfix)
    if len(snapshot) == 0:
        snapshot = '202001'
    query = """ SELECT * FROM wiki.Topics WHERE `Snapshot` = """ +snapshot+ """; """
    df = pd.read_sql(query, engine)
    df['Article Topics Distribution'] = df['Article Topics Distributions'].apply(lambda x: x[1:-1].split(','))
    df = df.drop(['Article Topics Distributions'], axis=1)
    new_data = pd.DataFrame(df['Article Topics Distribution'].values.tolist(), index=df.index).add_prefix('Topic_')
    df = pd.concat([df, new_data[:]], axis=1)

    filter_col = [col for col in df if col.startswith('Topic_')]
    filter_col.insert(0, 'Article')
    df = df[filter_col]
    for col in list(df.columns):
        if 'Topic_' in col:
            df[col] = df[col].astype(float)

    df.fillna(0, inplace=True)  # replace nan values with 0
    # calculate the sum of the rows and columns needed for proportion
    df.loc[:, 'Total'] = df.sum(axis=1)
    df.loc['Total', 1:] = df.sum(axis=0)
    df.fillna('', inplace=True)
    proportion = df.iloc[-1, 1:-1].divide(df.iloc[-1, -1], axis='rows').rename("Proportion")
    proportion = proportion.values.tolist()

    df.rename(columns={'Topic_0': 'Social Studies', 'Topic_1': 'Hard Science', 'Topic_2': 'Dates',
                       'Topic_3': 'Technical', 'Topic_4': 'Celebrities'}, inplace=True)
    Topics = df.columns[1:-1].tolist()
    topics = []
    prop = []
    final_df = pd.DataFrame(Topics, columns=['categories'])
    final_df = pd.concat([final_df, pd.DataFrame(proportion, columns=['proportion'])], axis=1)
    final_df = final_df.sort_values(by='proportion', ascending=False)
    final_df = final_df.round({"proportion": 2})
    for i in final_df['categories']:
        topics.append(i)
    for i in final_df['proportion']:
        prop.append(i)
    result = {'Topics': topics, 'Proportion': prop}

    # Plots the sunburst(pie) graph
    fig = px.sunburst(result, path=['Topics'], values='Proportion',
                      color='Proportion',
                      color_continuous_scale='Peach', width=600, height=500)
    fig.update_traces(textfont_size=14, textfont_color='black')
    fig.update_layout(hoverlabel_font_color='black', title_text='Wikipedia Page Summary',
                      font=dict(
        family="Droid Sans Mono", size=16,))
    fig.write_image("wikipediapagesummary.png")

    return result

def get_summary_result(content):
    # input will be "YYYYMMDD" (string)

    result = generateSummaryResult(content)
    result['Date'] = content
    #result = {
    #	'topics': ['T1', 'T2', 'T3'],
    #	'article_count': [4569, 2918, 634],
    #	'proportion': [0.294, 0.191, 0.060],
    #	'date': content
    #}

    return result