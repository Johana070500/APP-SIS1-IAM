# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
        
dt = pd.read_csv('heart.csv')
dt.head()

dt.info()

Y = dt[dt.target == 1]
N = dt[dt.target == 0]

# Ajuste de escalas o estandarizar las escalas
plt.scatter(Y.age,Y.thalach, color = "red", label = "Heart attack")
plt.scatter(N.age,N.thalach, color = "green", label = "NOT Heart attack")
plt.xlabel("age")
plt.ylabel("thalach")
plt.legend()
plt.show()

y = dt.target.values
x_dt = dt.drop(["target"], axis = 1)
x = (x_dt - np.min(x_dt))/(np.max(x_dt)-np.min(x_dt))

# Creamos el conjunto de entrenamiento y conjunto de prueba. 80% entrenar. 20% prueba.

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.2, random_state = 42)

# Entrenamiento del modelo KNN

knn = KNeighborsClassifier(n_neighbors = 2) # I chose K = 3 just for now.
knn.fit(x_train, y_train)

# Predicción del conjunto de prueba
prediction = knn.predict(x_test)
print("{} nn score: {} ".format(2,knn.score(x_test,y_test)))

# Matriz de confusion

cm = confusion_matrix(y_test, prediction)
print(confusion_matrix(y_test, prediction))

print(classification_report(y_test, prediction))

# Visualizacion de los datos de prueba
score_list = []
for each in range(1,30):
    knn2 = KNeighborsClassifier(n_neighbors = each)
    knn2.fit(x_train,y_train)
    score_list.append(knn2.score(x_test,y_test))
    
plt.plot(range(1,30),score_list)
plt.xlabel("K values")
plt.ylabel("Accuracy")
plt.show()

#95% precision
#Rojo heart attack
#Verde NOT heart attack