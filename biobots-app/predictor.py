import sqlite3
import pandas as pd
from sklearn_pandas import DataFrameMapper
import sklearn.preprocessing
import numpy as np
from sklearn.ensemble import RandomForestRegressor


def getdata():
    conn = sqlite3.connect('biodata.db')
    info = pd.read_sql('select * from session_info', conn)
    data = pd.read_sql('select * from session_data', conn)

    all_data = info.append(data)
    all_data = all_data.pivot('session_id', 'meta_key', 'meta_value')

    return all_data


# global predictor for now
all_data = getdata()
all_data = all_data.apply(lambda x: pd.to_numeric(x, errors='ignore'))
mapper = DataFrameMapper([
        ('cl_duration', None),
        ('cl_enabled', sklearn.preprocessing.LabelBinarizer()),
        ('cl_intensity', None),
        ('extruder1', None),
        ('extruder2', None),
        ('layerHeight', None),
        ('layerNum', None),
        ('wellplate', sklearn.preprocessing.LabelBinarizer())
    ])

dataset = mapper.fit_transform(all_data.copy())

live_regressor = RandomForestRegressor()
elasticity_regressor = RandomForestRegressor()

live_regressor.fit(dataset, all_data.livePercent)
elasticity_regressor.fit(dataset, all_data.elasticity)




def makePrediction(cl_duration, cl_enabled, cl_intensity, extruder1, extruder2, layerHeight, layerNum, wellplate):
    input_data = pd.DataFrame({'cl_duration': cl_duration, 'cl_enabled': cl_enabled, 'cl_intensity': cl_intensity,
                               'extruder1': extruder1, 'extruder2': extruder2, 'layerHeight': layerHeight,
                               'layerNum': layerNum, 'wellplate': wellplate}, index=[0])
    input_vector = mapper.transform(input_data)

    livePercent = live_regressor.predict(input_vector)
    deadPercent = 100.0 - livePercent
    elasticity = elasticity_regressor.predict(input_vector)

    return {'deadPercent': deadPercent, 'elasticity': elasticity, 'livePercent': livePercent}