import pandas as pd
import numpy as np
import requests

#building networks
from tensorflow import keras
from keras.models import Sequential
from keras import Input
from keras.layers import Dense, SimpleRNN

#model eval
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler

import plotly
import plotly.express as px
import plotly.graph_objects as go

import math
import matplotlib


def prep_data(datain, time_step):
    y_indices = np.arange(start=time_step, stop=len(datain), step=time_step)
    y_tmp = datain[y_indices]
    rows_X = len(y_tmp)
    X_tmp = datain[range(time_step*rows_X)]
    X_tmp = np.reshape(X_tmp, (rows_X, time_step, 1))
    return X_tmp, y_tmp

# modelling adapted from https://towardsdatascience.com/rnn-recurrent-neural-networks-how-to-successfully-model-sequential-data-in-python-5a0b9e494f92

def train_and_predict():

    data = pd.read_csv("database/completed_data_gw.csv")
    cleandata = data

    drop = [ 'Unnamed: 0', 'season_x', 'position', 'team_x', 'element', 'fixture',
           'kickoff_time', 'opponent_team', 'opp_team_name',
           'selected', 'transfers_balance', 'transfers_in', 'transfers_out', 'GW', 'threat', 'team_a_score', 'team_h_score',
           'ict_index', 'influence']
    data = data.drop(drop,axis=1)
    data["was_home"] = data["was_home"].astype(int)

    info = {'name':data.name.unique()}
    newdf = pd.DataFrame(info)
    newdf['total_points']=0
    newdf['GW_Adjusted'] = data.GW_Adjusted.max()+1
    data = pd.concat([data,newdf])

    playernames = []
    predictions = []

    sum = 0

    # do for each player in dataset
    for x in data['name'].unique():

        print(x)

        df=data[data['name']==x].copy()
        # prediction is on total points
        X=df[['total_points']]
        scaler = MinMaxScaler()
        X_scaled=scaler.fit_transform(X)

        # split into train and test
        train_data, test_data = train_test_split(X_scaled, test_size=0.2, shuffle=False)


        # use every 4 games to predict the 5th
        time_step = 10
        X_train, y_train = prep_data(train_data, time_step)
        X_test, y_test = prep_data(test_data, time_step)


        # model specs
        model = Sequential(name="Per-Player-RNN-Model") # Model
        model.add(Input(shape=(time_step,1), name='Input-Layer'))
        model.add(SimpleRNN(units=1, activation='tanh', name='Hidden-Recurrent-Layer'))
        model.add(Dense(units=1, activation='tanh', name='Hidden-Layer'))
        model.add(Dense(units=1, activation='linear', name='Output-Layer'))

        model.compile(optimizer='adam',
                      loss='mean_squared_error',
                      metrics=['MeanSquaredError', 'MeanAbsoluteError'],
                      run_eagerly=True,
                     )

        model.fit(X_train, y_train, batch_size = 1,epochs=20, verbose=0)

        X_every=df[['total_points']]
        X_every=scaler.transform(X_every)

        for i in range(0, len(X_every)-time_step):
            if i==0:
                X_comb=X_every[i:i+time_step]
            else:
                X_comb=np.append(X_comb, X_every[i:i+time_step])
                X_comb=np.reshape(X_comb, (math.floor(len(X_comb)/time_step), time_step, 1))
        df['points_prediction'] = np.append(np.zeros(time_step), scaler.inverse_transform(model.predict(X_comb)))
        playerpred = df[df.GW_Adjusted==df.GW_Adjusted.max()]
        playernames.append(playerpred['name'].iloc[0])
        predictions.append(playerpred['points_prediction'].iloc[0])


    for i,x in enumerate(predictions):
        if x < 0:
            predictions[i]=0

    d = {'name':playernames,'pred_points':predictions}
    df = pd.DataFrame(data=d)

    return df
