def summary():
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import getpass
    import sqlalchemy

    user = getpass.getpass(prompt='User: ')
    pwd = getpass.getpass()
    DB_URIfix = 'mysql+pymysql://' + user + ':' + pwd + '@35.197.16.55/wiki' + '?charset=utf8mb4'
    engine = sqlalchemy.create_engine(DB_URIfix)

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

    # Article count
    df_cols = df.columns[1:-1]
    new_df = df[df_cols]
    new_df['Topics'] = new_df.idxmax(axis=1)
    new_df = new_df.groupby('Topics')['Topics'].size()

    proportion = proportion.values.tolist()
    proportion = [i * 100 for i in proportion]
    article_count = new_df.values.tolist()

    df.rename(columns={'Topic_0': 'Social Studies', 'Topic_1': 'Hard Science', 'Topic_2': 'Dates',
                       'Topic_3': 'Technical', 'Topic_4': 'Celebrities'}, inplace=True)
    Topics = df.columns[1:-1].tolist()
    result = {'Topics': Topics, 'Article_count': article_count, 'Proportion': proportion}

    # Plots the sunburst(pie) graph
    for key, value in result.items():
        if key == 'Article_count':
            value = [str(i) for i in value]
            result.update({'Article_count': value})

    fig = px.sunburst(result, path=['Topics', 'Article_count'], values='Proportion',
                      color='Proportion', hover_data=['Article_count'], color_continuous_scale='Peach',
                      width=700, height=600)
    fig.update_traces(textfont_size=14, textfont_color='black')
    fig.update_layout(hoverlabel_font_color='black', title_text='Wikipedia Page Summary', font=dict(
        family="Droid Sans Mono", size=16,))
    fig.write_image("wikipediapagesummary.png")

    # Plots the bar graph graph
    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=("Wikipedia Article distribution", "Wikipedia Article proportion"))

    fig.add_trace(go.Bar(x=result['Topics'], y=result['Article_count'], name='Number of Articles', marker_color='indianred',
                         width=0.5, marker_line_width=1.5, opacity=0.8), 1, 1)
    fig.add_trace(go.Bar(x=result['Topics'], y=result['Proportion'], name='Article Distribution', marker_color='lightsalmon',
                         width=0.5, marker_line_width=1.5, opacity=0.8), 1, 2)
    fig.update_layout(hoverlabel_font_color='black', title_text='Wikipedia Page Summary')
    fig.write_image("wikipediapagesummary2.png")

    return result