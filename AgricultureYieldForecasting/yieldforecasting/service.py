import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import linear_model

import numpy as np

from yieldforecasting.appconstants import path1,path2

def loaddata():

    df2 = pd.read_csv(path2)
    # ================================================================
    districts = df2['District_Name']
    districts = districts.drop_duplicates()
    district_dict = dict()
    # ====================================================================

    i = 1
    for dist in districts:
        district_dict.update({dist: i})
        i = i + 1

    print(district_dict)

    return district_dict

def forecast(District_Name,Season,Area,temperature,humidity,ph,rainfall):

    df1 = pd.read_csv(path1)
    df2 = pd.read_csv(path2)
    # ================================================================

    crops1 = df1['Crop']
    crops2 = df2['Crop']
    districts = df2['District_Name']

    crops1 = crops1.drop_duplicates()
    crops2 = crops2.drop_duplicates()
    districts = districts.drop_duplicates()

    crop1_dict = dict()
    crop2_dict = dict()
    district_dict = dict()

    # ================================================================
    i = 1
    for crop in crops1:
        crop1_dict.update({crop: i})
        i = i + 1

    df1['Crop'] = df1['Crop'].map(crop1_dict)

    # ====================================================================

    i = 1
    for crop in crops2:
        crop2_dict.update({crop: i})
        i = i + 1

    df2['Crop'] = df2['Crop'].map(crop2_dict)

    # ====================================================================

    i = 1
    for dist in districts:
        district_dict.update({dist: i})
        i = i + 1

    df2['District_Name'] = df2['District_Name'].map(district_dict)

    # ======================================================================

    df2['Crop'] = df1['Crop']

    # ======================================================================

    feature_cols = ["temperature", "humidity", "ph", "rainfall"]
    X = df1[feature_cols]  # Features
    y = df1.Crop  # Target variable

    # Split X and y into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

    clf = DecisionTreeClassifier()
    clf = clf.fit(X_train, y_train)

    # y_pred = clf.predict(X_test)

    my_pred = clf.predict([[temperature, humidity, ph, rainfall]])
    predicted_crop = my_pred[0]

    def get_key(val):
        for key, value in crop1_dict.items():
            if val == value:
                return key

    finacrop=get_key(predicted_crop)
    # ====================================================================

    df2[:] = np.nan_to_num(df2)

    feature_cols = ["District_Name", "Season", "Crop", "Area"]

    X = df2[feature_cols]  # Features
    y = df2.Production  # Target variable

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

    regr = linear_model.LinearRegression()
    regr.fit(X_train, y_train)

    print(type(District_Name),type(Season),type(predicted_crop),type(Area))

    y_pred = regr.predict([[District_Name, Season, predicted_crop, Area]])

    return [finacrop,y_pred[0]]