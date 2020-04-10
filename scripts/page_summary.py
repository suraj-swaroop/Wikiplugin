import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from plotly.subplots import make_subplots

def main(df):
    year = '2020'
    month = '01'
    date = int(year + month)

    df = df.loc[df['Snapshot']== date]  # filter data based on monthly date
    df['Article Topics Distribution'] = df['Article Topics Distributions'].apply(lambda x: x[1:-1].split(','))
    df = df.drop(['Article Topics Distributions'], axis=1)
    new_data = pd.DataFrame(df['Article Topics Distribution'].values.tolist(), index=df.index).add_prefix(
        'Article Topics Distribution_')
    df = pd.concat([df, new_data[:]], axis=1)
    df = df[df['Article Topics Distribution'].apply(len).gt(2)]
    filter_col = [col for col in df if col.startswith('Article Topics Distribution')]
    filter_col.remove('Article Topics Distribution')
    filter_col.insert(0, 'Article')
    df = df[filter_col]
    for col in list(df.columns):
        if ('Article Topics Distribution_' in col):
            df[col] = df[col].astype(float)

    df.rename(columns={'Article Topics Distribution_0': 'Topic 1', 'Article Topics Distribution_1': 'Topic 2',
                       'Article Topics Distribution_2': 'Topic 3',
                       'Article Topics Distribution_3': 'Topic 4', 'Article Topics Distribution_4': 'Topic 5'}, inplace=True)

    df.fillna(0, inplace=True)  # replace nan values with 0
    df.loc[:, 'Total'] = df.sum(axis=1)
    df.loc['Total', 1:] = df.sum(axis=0)
    df.fillna('', inplace=True)
    df_cols = df.columns[1:-1]

    # Article count
    new_df = df[df_cols]
    new_df['Topics'] = new_df.idxmax(axis=1)
    new_df = new_df.groupby('Topics')['Topics'].size()

    # calculate the proportion
    proportion = df.iloc[-1, 1:-1].divide(df.iloc[-1, -1], axis='rows').rename("Proportion")

    proportion = proportion.values.tolist()
    article_count = new_df.values.tolist()
    Topics = df_cols.tolist()
    result = {'Topics': Topics, 'Article_count': article_count, 'Proportion': proportion}

    return result

def plot_pie(result):
    for key, value in result.items():
        if key == 'Article_count':
            value = [str(i) for i in value]
            result.update({'Article_count': value})

    fig = px.sunburst(result, path=['Topics', 'Article_count'], values='Proportion',
                      color='Proportion', hover_data=['Article_count'], color_continuous_scale='Peach')
    fig.update_traces(textfont_size=12, textfont_color='black')
    fig.update_layout(hoverlabel_font_color='black', title_text='Wikipedia Page Summary')

    fig.show()

def plot_bar(result):
    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=("Wikipedia Article distribution", "Wikipedia Article proportion"))

    fig.add_trace(go.Bar(x=result['Topics'], y=result['Article_count'], name='Number of Articles', marker_color='indianred',
                         width=0.5, marker_line_width=1.5, opacity=0.8), 1, 1)
    fig.add_trace(go.Bar(x=result['Topics'], y=result['Proportion'], name='Article Distribution', marker_color='lightsalmon',
                         width=0.5, marker_line_width=1.5, opacity=0.8), 1, 2)

    fig.show()


if __name__ == '__main__':
    summary_file = sys.argv[1]
    df = pd.read_csv(summary_file)
    result = main(df)
    plot_pie(result)
    plot_bar(result)