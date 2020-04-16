from flask import Flask, render_template, url_for, request, flash
from flask_wtf import FlaskForm
from web_application import app
#from web_application.generate_result import get_blog_result, get_web_result
#from web_application.popular_result import pop_result_blog, pop_result_web, pop_topics_blog, pop_topics_web

from web_application.generate_drilldown import graphical_similarity, semantic_similarity
from web_application.generate_summary import get_summary_result
from web_application.generate_priority import get_priority_result
from web_application.check_article import check_wiki, check_db, check_date
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError


web_name = 'WikiPlugin Analysis'


class PostForm(FlaskForm):
	content = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('OK')


@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', name=web_name)

@app.route('/drilldown', methods=['GET', 'POST'])
def drilldown():
	form = PostForm()
	if form.validate_on_submit():
		article = form.content.data
		result = check_wiki(article)

		if result.startswith('!!'):
			flash('Something is wrong with the input. Please try again with correct input/format.')
			print('Something is wrong with the input: ', result)
		else:
			if result.startswith('##'):
				flash('Wikipedia does not have such an article. Looking for a similar article....')

			db_result = check_db(result)
			if db_result.startswith('!!'):
				# alert!
				flash('Our DB does not have the article you inserted.')
				print('Our DB does not have: ', db_result)
			else:
				gs = graphical_similarity(db_result)
				ss = semantic_similarity(db_result)
				g_titles = gs['Article']
				g_links = gs['URL']
				#g_difficulty = gs['ProbabilityOfDifficulty']
				#g_time = gs['AdjustedReadingTimeMinutes']
				s_titles = ss['Article']
				s_links = ss['URL']
				s_distance = ss['EuclideanDist']
				s_time = ss['AdjustedReadingTimeMinutes']
				print(s_titles)
				return render_template('result_drilldown.html', name=web_name, \
					g_titles=g_titles, g_links=g_links, db_result=db_result, \
					s_titles=s_titles, s_links=s_links, s_distance=s_distance, s_time=s_time)
	return render_template('drilldown.html', name=web_name, form=form)

@app.route('/result_drilldown')
def result_drilldown():
	# topic = request.args['topic']
	# if len(topic) > 0:
	# 	returned = pop_result_web(topic)
	# 	colors = returned['colors']
	# 	fonts = returned['fonts']
	return render_template('result_drilldown.html', name=web_name, \
			g_titles=g_titles, g_links=g_links, g_difficulty=g_difficulty, \
			g_time=g_time, s_titles=s_titles, s_distance=s_distance, \
			s_difficulty=s_difficulty, s_time=s_time)

@app.route('/summary', methods=['GET', 'POST'])
def summary():
	form = PostForm()
	if form.validate_on_submit():
		result = check_date(form.content.data)
		if result.startswith('!!'):
			flash('Our database does not have data for the month you inserted. Please try with different month.')
			print('Our database does not have data for the month: ', result)
		else:
			returned = get_summary_result(result)
			topics = returned['Topics']
			proportion = returned['Proportion']
			date = returned['Date']
			return render_template('result_summary.html', name=web_name, \
				topics=topics, proportion=proportion, date=date)
	return render_template('summary.html', name=web_name, form=form) 

@app.route('/result_summary')
def result_summary():
	return render_template('result_summary.html', name=web_name, \
			topics=topics, article_count=article_count, proportion=proportion, date=date)

@app.route('/priority')
def priority():
	returned = get_priority_result()
	titles = returned['article']
	links = returned['url']
	difficulty = returned['difficulty']
	rtime = returned['rtime']
	return render_template('priority.html', name=web_name, \
			titles=titles, links=links, difficulty=difficulty, rtime=rtime)

@app.route('/about')
def about():
	return render_template('about.html', title='About', name=web_name)

if __name__ == '__main__':
	app.run(debug=True)


