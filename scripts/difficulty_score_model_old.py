import pandas as pd
import numpy as np
import sys
import re
import string
import pickle
import nltk
from nltk import word_tokenize, pos_tag
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import Binarizer, LabelBinarizer


def main(summary_file, score_file):
	print('Loading/preprocessig the data....')

	nltk.download('punkt')

	df = pd.read_csv('../Datasets/'+summary_file) #reads the summary data
	df2 = pd.read_csv('../Datasets/'+score_file) #reads the data where we have manually rated the articles
	df2 = df2[['title','sentences']]

	# Joins both the dataframes
	data = pd.merge(df,df2,left_on='Article',right_on='title')
	data = data.rename(columns = {'Target Complexity': 'score'})

	# Splits the string and converts it into a list
	data['Article Topics Distribution'] = data['Article Topics Distributions'].apply(lambda x:x[1:-1].split(','))
	data['Articles Vector Centroid'] = data['Article Vector Centroid'].apply(lambda x:x[1:-1].split())
	data = data.drop(['Unnamed: 0','title','Article Vector Centroid', 'Article Topics Distributions'],axis=1)

	# Splits the vectors into multiple columns
	data[['ATD_1','ATD_2','ATD_3', 'ATD_4','ATD_5']] = pd.DataFrame(data['Article Topics Distribution'].values.tolist(), index= data.index)
	new_data = pd.DataFrame(data['Articles Vector Centroid'].values.tolist(), index= data.index).add_prefix('AVC_')
	data = pd.concat([data, new_data[:]], axis=1)
	data = data.drop(['Article Topics Distribution','Articles Vector Centroid'],axis=1)

	# filters the sentences to remove unneccesary characters and creates a description of the article
	final_ls = []
	overall_list = []
	for i in range(0, len(data)):
		tokenize = ''
		result_list = []
		fil_sent = data['sentences'][i]
		line = re.sub('[!@#$]', '', fil_sent)
		tokenize= word_tokenize(line)
		for j in tokenize:
			result = j.split('"=')
			result = re.sub('[\W_]+', '', j)
			result_list.append(result)
			result_list = [x for x in result_list if x]
		final_ls.append(result_list)

	joined_list = []
	for i in range(0, len(final_ls)):
		res = ' '.join(final_ls[i])
		res = [res]
		joined_list.append(res)

	data['content'] = joined_list
	data['description'] = data.content.apply(' '.join)
	data = data.drop(['sentences','content'],axis=1)
	data = data[data.score != 0]
	data['Eigenvector Centrality'].fillna(0, inplace=True)
	data['Louvain Community'].fillna(0, inplace=True)

	# Iterate through the columns to select the numeric one's and converts them to float
	for col in list(data.columns):
		if ('Difficulty' in col or 'Centrality' in col or 'Community' in col or 
			'Clicks' in col or 'Length' in col or 'score' in col or 'ATD' in col or 'AVC' in col):
			data[col] = data[col].astype(float)

	'''this part of the code is to find the correlation between the features and the target'''
	# Select the numeric columns
	numeric_subset = data.select_dtypes('number')
	numeric_subset.fillna(0, inplace=True) #replace nan values with 0

	# Create columns with square root and log of numeric columns
	for col in numeric_subset.columns:
		if col == 'score':
			next
		else:
			numeric_subset['sqrt_' + col] = np.sqrt(numeric_subset[col])
			numeric_subset['log_' + col] = np.log(numeric_subset[col])

	# Select the categorical columns and one-hot encode them
	categorical_subset = data[['Article', 'description']]
	categorical_subset = pd.get_dummies(categorical_subset)

	#combinig the numerical and categorical data
	features = pd.concat([numeric_subset, categorical_subset], axis = 1)

	# Find correlations with the score 
	correlations = features.corr()['score'].dropna().sort_values()

	features = data.copy()

	# Select the numeric columns
	numeric_subset = data.select_dtypes('number')
	numeric_subset.fillna(0, inplace=True)
	# numeric_subset = numeric_subset.drop(['AVC_1'], axis=1)

	# Select the categorical columns and one hot encode it
	categorical_subset = data[['Article', 'description']]
	categorical_subset = pd.get_dummies(categorical_subset) 

	#combinig the numerical and categorical data
	features = pd.concat([numeric_subset, categorical_subset], axis = 1)

	#making sure none of the score values are null
	score = features[features['score'].notnull()] 

	#seperating the column we intend to predict
	X = score.drop(columns='score')
	y = pd.DataFrame(score['score']) 

	print('Training the model....')

	transformer = Binarizer(threshold=2, copy=False)
	y = transformer.transform(y)

	#Create the scaler object with a range of 0-1
	scaler = MinMaxScaler(feature_range=(0, 1))
	scaler.fit(X)# Fit on the training data

	# Transform both the training and testing data
	X = scaler.transform(X)

	# Convert y to one-dimensional array (vector)
	y = np.array(y).reshape((-1, ))

	# Create the model to use for hyperparameter tuning
	model = LogisticRegression().fit(X, y)

	# Save the model
	filename = 'complexity_model.sav'
	pickle.dump(model, open(filename, 'wb'))

	print('Saved model: ', filename)


if __name__ == '__main__':
	summary_file = sys.argv[1]
	score_file = sys.argv[2]
	main(summary_file, score_file)
