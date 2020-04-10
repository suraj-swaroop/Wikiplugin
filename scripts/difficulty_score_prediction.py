import difficulty_score_model as dsm
import sys
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pickle

def prediction(data, filename):
    # Select the numeric columns
    numeric_subset = data.select_dtypes('number')
    numeric_subset.fillna(0, inplace=True)

    # Select the categorical columns and one hot encode it
    categorical_subset = data[['Article', 'description']]
    # categorical_subset = data['Article']
    categorical_subset = pd.get_dummies(categorical_subset)

    # combinig the numerical and categorical data
    features = pd.concat([numeric_subset, categorical_subset], axis=1)
    features = features.drop(columns='score')

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler.fit(features)
    features = scaler.transform(features)

    loaded_model = pickle.load(open(filename, 'rb')) #loading the cached model
    final_pred_prob = loaded_model.predict_proba(features)
    final_pred = loaded_model.predict(features)

    data['Score'] = final_pred.tolist()
    data['difficulty'] = final_pred.tolist()
    data['probability'] = final_pred_prob.tolist()

    dict_values = {1.0: 'Easy', 2.0: 'Easy', 3.0: 'Hard'}
    data = data.replace({"difficulty": dict_values})
    data['no_of_words'] = data.description.apply(lambda x: len(str(x).split(' ')))
    data[['prob_easy_1', 'prob_easy_2', 'prob_hard']] = pd.DataFrame(data.probability.values.tolist(), index=data.index)
    data['rank'] = data['prob_hard'].rank(ascending=False)
    data = data[['Article', 'Score', 'probability', 'difficulty', 'no_of_words', 'rank']]

    return data


if __name__ == '__main__':
    summary_file = sys.argv[1]
    score_file = sys.argv[2]
    model_file = sys.argv[3]
    data = dsm.filter_data(summary_file, score_file)
    result = prediction(data, model_file)
    result.to_csv("difficulty_prediction.csv")

    print('Predicted results are in: difficulty_prediction.csv ')