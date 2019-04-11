import pandas as pd
import numpy as np
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def make_prediction(value_height, value_weight, value_age, sport, gender, data):
	print(value_height)
	print(value_weight)
	print(value_age)
	if sport == 'swimming':
		if gender == 'm':
			data = pd.DataFrame(data[data['Sex'] == 'M'])
			data = pd.DataFrame(data[data['Sport'] == 'Swimming'])
			X = data[['Age','Height','Weight']]
			y = data['Medal_num']
			# implementing train-test-split
			X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=66)

			# random forest model creation
			rfc = RandomForestClassifier()
			rfc.fit(X_train,y_train)

			# predictions
			return rfc.predict([[value_age, value_height, value_weight]])[0]
		else:
			data = pd.DataFrame(data[data['Sex'] == 'F'])
			data = pd.DataFrame(data[data['Sport'] == 'Swimming'])
			X = data[['Age','Height','Weight']]
			y = data['Medal_num']
			# implementing train-test-split
			X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=66)

			# random forest model creation
			rfc = RandomForestClassifier()
			rfc.fit(X_train,y_train)

			# predictions
			return rfc.predict([[value_age, value_height, value_weight]])[0]
	elif sport == 'athletics':
		if gender == 'm':
			data = pd.DataFrame(data[data['Sex'] == 'M'])
			data = pd.DataFrame(data[data['Sport'] == 'Athletics'])
			X = data[['Age','Height','Weight']]
			y = data['Medal_num']
			# implementing train-test-split
			X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=66)

			# random forest model creation
			rfc = RandomForestClassifier()
			rfc.fit(X_train,y_train)

			# predictions
			return rfc.predict([[value_age, value_height, value_weight]])[0]
		else:
			data = pd.DataFrame(data[data['Sex'] == 'F'])
			data = pd.DataFrame(data[data['Sport'] == 'Athletics'])
			X = data[['Age','Height','Weight']]
			y = data['Medal_num']
			# implementing train-test-split
			X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=66)

			# random forest model creation
			rfc = RandomForestClassifier()
			rfc.fit(X_train,y_train)

			# predictions
			return rfc.predict([[value_age, value_height, value_weight]])[0]
	elif sport == 'gymnastics':
		if gender == 'm':
			data = pd.DataFrame(data[data['Sex'] == 'M'])
			data = pd.DataFrame(data[data['Sport'] == 'Gymanstics'])
			X = data[['Age','Height','Weight']]
			y = data['Medal_num']
			# implementing train-test-split
			X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=66)

			# random forest model creation
			rfc = RandomForestClassifier()
			rfc.fit(X_train,y_train)

			# predictions
			return rfc.predict([[value_age, value_height, value_weight]])[0]

		else:
			data = pd.DataFrame(data[data['Sex'] == 'F'])
			data = pd.DataFrame(data[data['Sport'] == 'Gymanstics'])
			X = data[['Age','Height','Weight']]
			y = data['Medal_num']
			# implementing train-test-split
			X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=66)

			# random forest model creation
			rfc = RandomForestClassifier()
			rfc.fit(X_train,y_train)

			# predictions
			return rfc.predict([[value_age, value_height, value_weight]])[0]
	return 0