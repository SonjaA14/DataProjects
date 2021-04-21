# https://www.kaggle.com/c/titanic/data
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import seaborn as sns 


def eda():
    train = pd.read_csv('train.csv')
    test= pd.read_csv('test.csv')
    
    train['train_test'] = 1
    test['train_test'] = 0
    test['Survived'] = np.NaN
    all_data = pd.concat([train,test])

    train['Sex'] = train['Sex'].astype('category')
    train['Embarked'] = train['Embarked'].astype('category')

    df_num = train[['Age','SibSp','Parch','Fare']]
    df_cat = train[['Survived','Pclass','Sex','Ticket','Cabin','Embarked']]

    tmp_f = train.loc[train['Sex'] == 'female', :]
    mean_f = tmp_f['Age'].mean()
    train.Age[train['Sex'] == 'female'] = train.Age[train['Sex'] == 'female'].fillna(mean_f)

    tmp_m = train.loc[train['Sex'] == 'male', :]
    mean_m = tmp_m['Age'].mean()
    train.Age[train['Sex'] == 'male'] = train.Age[train['Sex'] == 'male'].fillna(mean_m)

    train.Fare = train.Fare.fillna(train.Fare.mean())

    train.dropna(subset=['Embarked'], inplace = True)

    train['Surname'], train['Tmp'] =  train['Name'].str.split(',',1).str
    train['Title'], train['Name'] = train['Tmp'].str.split('.',1).str


    train['Cabin_1'] = train.Cabin.str.slice(0,1)
    train['Cabin_2'] = train.Cabin.str.slice(1,)
    train['Familysize'] = train['Parch'] + train['SibSp'] + 1

    train.drop(['Cabin', 'Tmp'], inplace=True, axis =1)

    train['Title'] = train['Title'].astype('category')

    return train, test


if __name__ == "__getData__":
    train, test = eda()
