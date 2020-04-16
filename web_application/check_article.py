import sqlalchemy
import wikipedia
import pandas as pd
import sys

with open('web_application/database.key', 'r') as file:
    DB_URIfix = file.read()
engine = sqlalchemy.create_engine(DB_URIfix)


def check_wiki(url_or_title):

    title = url_or_title
    wikipedia.set_lang('en')

    if url_or_title.startswith('https://simple.wikipedia.org/wiki'):
        start = url_or_title.find('wiki/')+5
        end = len(url_or_title)
        title = url_or_title[start:end] 
    
    try:
        wiki = wikipedia.page(title)
        if wiki.title.lower().replace("-","").replace("_","") == title.lower().replace("-","").replace("_",""):
            result = wiki.title.replace(' ', '_')
        else:
            result = '##' + wiki.title.replace(' ', '_')

    except:
        result = '!! Wikipedia does not have an article for ' + title

    return result

def check_db(title):

    if title.startswith('##'):
        title = title[2:]

    try:
        SQL_semantic = """
            SELECT Article
            FROM wiki.Summary
            ;
        """

        df2 = pd.read_sql(SQL_semantic, engine)
        c1 = df2[df2['Article'] == title].values[0]

        result = title

    except:

        result = '!! Our database does not have data for ' + title

    return result


def check_date(date):

    try:
        query = """ SELECT * FROM wiki.Topics WHERE `Snapshot` = """ +date+ """; """
        df = pd.read_sql(query, engine)
        if len(df) == 0:
            result = '!! Our database does not have data for the month ' + date
        else:
            result = date

    except:

        result = '!! Our database does not have data for the month ' + date

    return result

