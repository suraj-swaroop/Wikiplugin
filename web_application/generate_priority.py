import getpass
import sqlalchemy
import pandas as pd
import pymysql
import wikipedia

def generatePriorityResult():
	with open('web_application/database.key', 'r') as file:
		DB_URIfix = file.read()
	engine = sqlalchemy.create_engine(DB_URIfix)

	sql_query = """
		SELECT * 
		FROM wiki.Difficulty  ;
	"""
	df = pd.read_sql(sql_query, engine)

	wikipedia.set_lang('simple')
	titles = df['Article'].tolist()
	diff = df['ProbabilityOfDifficulty'].tolist()
	rtime = df['AdjustedReadingTimeMinutes'].tolist()

	simple_list = []
	no_simple_page = []
	result = {'article': [], 'url': [], 'difficulty': [], 'rtime': []}
	i = 0
	while len(no_simple_page) < 5:
		try:

			wiki = wikipedia.page(titles[i])
			if wiki.title.lower().replace("-","").replace("_","") == titles[i].lower().replace("-","").replace("_",""):
				simple_list.append(wiki.title)
			else:
				no_simple_page.append(titles[i])

				url = 'https://en.wikipedia.org/wiki/'+titles[i]
				result['article'].append(titles[i])
				result['url'].append(url)
				result['difficulty'].append(diff[i])
				result['rtime'].append(rtime[i])
			i += 1

		except:
			no_simple_page.append(titles[i])

			url = 'https://en.wikipedia.org/wiki/'+titles[i]
			result['article'].append(titles[i])
			result['url'].append(url)
			result['difficulty'].append(diff[i])
			result['rtime'].append(rtime[i])

	return result


def get_priority_result():

	result = generatePriorityResult()
	#result = ['art1', 'art2', 'art3', 'art4', 'art5']

	return result

