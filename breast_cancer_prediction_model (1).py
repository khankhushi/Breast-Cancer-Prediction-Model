# -*- coding: utf-8 -*-
"""Breast Cancer Prediction Model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GZPsjam7zjxwqVMs77U588pUSMZyV85O

#**Breast Cancer Prediction**

Importing Libraries
"""

import numpy
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

"""Reading Data from file"""

from google.colab import files
data_frame= files.upload()

data_frame=pd.read_csv("data_cancer.csv")

"""This is a copy of UCI ML Breast Cancer Wisconsin (Diagnostic) datasets. https://goo.gl/U2Uwz2

Features are computed from a digitized image of a fine needle aspirate (FNA) of a breast mass. They describe characteristics of the cell nuclei present in the image.

Separating plane described above was obtained using Multisurface Method-Tree (MSM-T) [K. P. Bennett, "Decision Tree Construction Via Linear Programming." Proceedings of the 4th Midwest Artificial Intelligence and Cognitive Science Society, pp. 97-101, 1992], a classification method which uses linear programming to construct a decision tree. Relevant features were selected using an exhaustive search in the space of 1-4 features and 1-3 separating planes.

The actual linear program used to obtain the separating plane in the 3-dimensional space is that described in: [K. P. Bennett and O. L. Mangasarian: "Robust Linear Programming Discrimination of Two Linearly Inseparable Sets", Optimization Methods and Software 1, 1992, 23-34].

This database is also available through the UW CS ftp server:

ftp ftp.cs.wisc.edu cd math-prog/cpo-dataset/machine-learn/WDBC/

References
W.N. Street, W.H. Wolberg and O.L. Mangasarian. Nuclear feature extraction for breast tumor diagnosis. IS&T/SPIE 1993 International Symposium on Electronic Imaging: Science and Technology, volume 1905, pages 861-870, San Jose, CA, 1993.
O.L. Mangasarian, W.N. Street and W.H. Wolberg. Breast cancer diagnosis and prognosis via linear programming. Operations Research, 43(4), pages 570-577, July-August 1995.
W.H. Wolberg, W.N. Street, and O.L. Mangasarian. Machine learning techniques to diagnose breast cancer from fine-needle aspirates. Cancer Letters 77 (1994) 163-171.
"""

data_frame.head()

data_frame.info()

"""Return all the columns with null value count"""

data_frame.isna().sum()

"""Returns the size of dataset"""

data_frame.shape

"""Remove the column"""

data_frame=data_frame.dropna(axis=1)

"""Shape of dataset after removing null column"""

data_frame.shape

"""Describe the dataset"""

data_frame.describe()

"""Getting the count of Malignant [M] and Benign cells [B]"""

data_frame['diagnosis'].value_counts()

sns.countplot(data_frame['diagnosis'],label="count")

"""Label encoding (Convering the value of M and B into 1 and 0)"""

from sklearn.preprocessing import LabelEncoder
labelencoder_Y = LabelEncoder()
data_frame.iloc[:,1]=labelencoder_Y.fit_transform(data_frame.iloc[:,1].values)

data_frame.head()

sns.pairplot(data_frame.iloc[:,1:5],hue="diagnosis")

"""Getting the Correlation"""

data_frame.iloc[:,1:32].corr()

"""Visualising the Correlation"""

plt.figure(figsize=(10,10))
sns.heatmap(data_frame.iloc[:,1:10].corr(),annot=True,fmt=".0%")

"""Split the dataset into dependent (X) and Independent (Y) datasets"""

X=data_frame.iloc[:,2:31].values
Y=data_frame.iloc[:,1].values

from sklearn.model_selection import train_test_split
X_train, X_test,Y_train,Y_test= train_test_split(X,Y,test_size=0.20,random_state=0)

from sklearn.preprocessing import StandardScaler
X_train=StandardScaler().fit_transform(X_train)
X_test=StandardScaler().fit_transform(X_test)

"""Algorithms"""

def models(X_train,Y_train):
        #logistic regression
        from sklearn.linear_model import LogisticRegression
        log =LogisticRegression(random_state=0)
        log.fit(X_train,Y_train)
        
        
        #Decision Tree
        from sklearn.tree import DecisionTreeClassifier
        tree=DecisionTreeClassifier(random_state=0,criterion="entropy")
        tree.fit(X_train,Y_train)
        
        #Random Forest
        from sklearn.ensemble import RandomForestClassifier
        forest=RandomForestClassifier(random_state=0,criterion="entropy",n_estimators=10)
        forest.fit(X_train,Y_train)
        
        print('[0]logistic regression accuracy:',log.score(X_train,Y_train))
        print('[1]Decision tree accuracy:',tree.score(X_train,Y_train))
        print('[2]Random forest accuracy:',forest.score(X_train,Y_train))
        
        return log,tree,forest

model=models(X_train,Y_train)

"""Testing the model/result"""

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

for i in range(len(model)):
    print("Model",i)
    print(classification_report(Y_test,model[i].predict(X_test)))
    print('Accuracy : ',accuracy_score(Y_test,model[i].predict(X_test)))

from joblib import dump
dump(model[2],"Cancer_prediction.joblib")

import pickle

filename = 'trained_model.sav'
pickle.dump(model[2], open(filename, "wb"))

loaded_model= pickle.load(open('trained_model.sav', 'rb'))