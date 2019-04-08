import numpy as np
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn import metrics

def make_prediction(value_height, value_weight, value_age, sport, gender, data):
	print(value_height)
	print(value_weight)
	print(value_age)
	if sport == 'swimming':
		if gender == 'm':
			#Extract male swimmers
			male = data.Sex == "M"
			swim = data[male].Sport == "Swimming"
			male_swim = data[male][swim]
			male_swim_2 = male_swim[['Age','Height','Weight','Medal_num']]

			# Reset row indices
			male_swim_2 = male_swim_2.reset_index()
			male_swim_2.reset_index(drop=True)
			male_swim_2 = male_swim_2.drop('index', 1)

			#convert data frame to array
			X = male_swim_2[['Age','Weight','Height']].values
			y = male_swim_2[['Medal_num']].values

			# Split the Dataset into Train and Test
			X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

			# Train multinomial logistic regression
			mul_lr = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg').fit(X_train, y_train)
			return mul_lr.predict([[value_age, value_weight, value_height]])[0]
		else:
			#Extract female swimmers
			female = data.Sex == "F"
			swim = data[female].Sport == "Swimming"
			female_swim = data[female][swim]
			female_swim_2 = female_swim[['Age','Height','Weight','Medal_num']]
			# Reset row indices
			female_swim_2 = female_swim_2.reset_index()
			female_swim_2.reset_index(drop=True)
			female_swim_2 = female_swim_2.drop('index', 1)
			#convert data frame to array
			X2 = female_swim_2[['Age','Weight','Height']].values
			y2 = female_swim_2[['Medal_num']].values

			# Split the Dataset into Train and Test
			X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size = 0.25)

			# Train multinomial logistic regression
			mul_lr = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg').fit(X2_train, y2_train)

			return mul_lr.predict([[value_age, value_weight, value_height]])[0]
	elif sport == 'athletics':
		if gender == 'm':
			#Extract male athlete
			male = data.Sex == "M"
			athletic = data[male].Sport == "Athletics"
			male_athletic = data[male][athletic]
			male_athletic_2 = male_athletic[['Age','Height','Weight','Medal_num']]
			# Reset row indices
			male_athletic_2 = male_athletic_2.reset_index()
			male_athletic_2.reset_index(drop=True)
			male_athletic_2 = male_athletic_2.drop('index', 1)

			#convert data frame to array
			X3 = male_athletic_2[['Age','Weight','Height']].values
			y3 = male_athletic_2[['Medal_num']].values

			# Split the Dataset into Train and Test
			X3_train, X3_test, y3_train, y3_test = train_test_split(X3, y3, test_size = 0.25)


			# Train multinomial logistic regression
			mul_lr = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg').fit(X3_train, y3_train)

			return mul_lr.predict([[value_age, value_weight, value_height]])[0]
		else:
			#Extract female athlete
			female = data.Sex == "F"
			athletic = data[female].Sport == "Athletics"
			female_athletic = data[female][athletic]
			female_athletic_2 = female_athletic[['Age','Height','Weight','Medal_num']]
			# Reset row indices
			female_athletic_2 = female_athletic_2.reset_index()
			female_athletic_2.reset_index(drop=True)
			female_athletic_2 = female_athletic_2.drop('index', 1)

			#convert data frame to array
			X4 = female_athletic_2[['Age','Weight','Height']].values
			y4 = female_athletic_2[['Medal_num']].values

			# Split the Dataset into Train and Test
			X4_train, X4_test, y4_train, y4_test = train_test_split(X4, y4, test_size = 0.25)


			# Train multinomial logistic regression
			mul_lr = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg').fit(X4_train, y4_train)
			return mul_lr.predict([[value_age, value_weight, value_height]])[0]
	elif sport == 'gymnastics':
		if gender == 'm':
			#Extract male gymnast
			male = data.Sex == "M"
			gymnast = data[male].Sport == "Gymnastics"
			male_gymnast = data[male][gymnast]
			male_gymnast_2 = male_gymnast[['Age','Height','Weight','Medal_num']]
			# Reset row indices
			male_gymnast_2 = male_gymnast_2.reset_index()
			male_gymnast_2.reset_index(drop=True)
			male_gymnast_2 = male_gymnast_2.drop('index', 1)

			#convert data frame to array
			X5 = male_gymnast_2[['Age','Weight','Height']].values
			y5 = male_gymnast_2[['Medal_num']].values

			# Split the Dataset into Train and Test
			X5_train, X5_test, y5_train, y5_test = train_test_split(X5, y5, test_size = 0.25)


			# Train multinomial logistic regression
			mul_lr = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg').fit(X5_train, y5_train)

			return mul_lr.predict([[value_age, value_weight, value_height]])[0]

		else:
			#Extract female gymnast
			female = data.Sex == "F"
			gymnast = data[female].Sport == "Gymnastics"
			female_gymnast = data[female][gymnast]
			female_gymnast_2 = female_gymnast[['Age','Height','Weight','Medal_num']]
			# Reset row indices
			female_gymnast_2 = female_gymnast_2.reset_index()
			female_gymnast_2.reset_index(drop=True)
			female_gymnast_2 = female_gymnast_2.drop('index', 1)

			#convert data frame to array
			X6 = female_gymnast_2[['Age','Weight','Height']].values
			y6 = female_gymnast_2[['Medal_num']].values

			# Split the Dataset into Train and Test
			X6_train, X6_test, y6_train, y6_test = train_test_split(X6, y6, test_size = 0.25)


			# Train multinomial logistic regression
			mul_lr = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg').fit(X6_train, y6_train)

			return mul_lr.predict([[value_age, value_weight, value_height]])[0]
	return 0