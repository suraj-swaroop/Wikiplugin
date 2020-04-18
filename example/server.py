from flask import Flask, request, render_template
import sqlalchemy
import pandas as pd
import numpy as np
import sys

# Connection
with open('database.key', 'r') as file:
    DB_URIfix = file.read()
engine = sqlalchemy.create_engine(DB_URIfix)

# Helper Functions
def urlify(s):
    return 'https://en.wikipedia.org/wiki/'+s

#def npify(s):
    return np.fromstring(s[1:-1],dtype=np.float, sep=' ')

#def euclid_dist(c2):
    return np.linalg.norm(c1-c2)



# First Table 
def graphical_similarity(url_or_title):
    
    snapshot = '202001'

    if url_or_title.startswith('https'):
        start = url.find('wiki/')+5
        end = len(url)
        url_last_part = url[start:end] 
    else:
        url_last_part = url_or_title
    
    SQL_graphical = """
    SELECT c.*, d.ProbabilityOfDifficulty, d.AdjustedReadingTimeMinutes
    FROM wiki.Clickstream c
    LEFT JOIN Difficulty d ON d.Article = c.`From`
    WHERE c.`To` = '"""+url_last_part+"""'
    AND c.`From` NOT IN ('other-search','other-empty','Main_Page','other-external','other-internal')
    AND c.Snapshot = """+snapshot+"""
    order by c.`Count` desc
    limit 5;
    """

    df1 = pd.read_sql(SQL_graphical, engine)
    df1['URL'] = df1['From'].apply(urlify)
    df1['Article'] = df1['From']
    df1_return = df1[['Article','URL']]
    
    return df1_return.to_dict()

# Second Table
def semantic_similarity(url_or_title):
    
    if url_or_title[0:5] == 'https':
        start = url.find('wiki/')+5
        end = len(url)
        url_last_part = url[start:end] 
    else:
        url_last_part = url_or_title
    
    SQL_semantic = """
    SELECT max(d.AdjustedReadingTimeMinutes) AS ReadingTime
    FROM wiki.Summary s
    LEFT JOIN Difficulty d ON d.Article = s.Article
    WHERE s.Article = '"""+url_or_title+"""'
    ;
    """

    df2 = pd.read_sql(SQL_semantic, engine)
    #df2['Article Vector Centroid'] = df2['Article Vector Centroid'].apply(npify)
    #c1 = df2[df2['Article'] == url_last_part]['Article Vector Centroid'].values[0]

    #def euclid_dist(c2):
    #    return np.linalg.norm(c1-c2)

    #df2['EuclideanDist'] = df2['Article Vector Centroid'].apply(euclid_dist)
    #df2 = df2.sort_values(by='EuclideanDist')
    #df2 = df2[df2['Article'] != url_last_part]

    #df2['URL'] = df2['Article'].apply(urlify)
    #df2_return = df2[['Article','URL','EuclideanDist','AdjustedReadingTimeMinutes']]

    return df2.head().reset_index()[['ReadingTime']]


app = Flask(__name__)
app.debug = True


@app.route("/", methods=['GET', 'POST'])

def index():
    if request.method == "POST":

        name = request.form["name"]
        
        #print(graphical_similarity(name))
        reading_time =  str(semantic_similarity(name).values[0][0])

        return "the reading time is " + reading_time + ' minutes'
    
    return render_template("index.html")




if __name__ == "__main__":

    app.run()
