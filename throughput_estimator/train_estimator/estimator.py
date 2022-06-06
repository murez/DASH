from sklearnex import patch_sklearn
patch_sklearn()
import numpy as np
import pandas as pd
import sklearn as sk
import xgboost as xgb
from kernals_1080 import *
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.multioutput import MultiOutputRegressor
import joblib

pca = joblib.load('pca.pkl')
predictor = joblib.load('predictor.pkl')

test_target_rate = [0.4453172 , 0.44768044, 0.84611183]
test_batch_size = 2
test_data = np.array([ 0.24,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,
        0.57,  2.86,  0.55,  0.41,  0.  ,  0.  ,  0.  ,  0.54,  0.  ,
        0.  ,  0.85, 48.38,  0.36,  0.  ,  0.  , 35.08,  0.  ,  0.36,
        0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.47,  0.  ,  0.  ,  0.  ,
        0.  ,  1.26,  0.  ,  0.35,  0.48,  0.  ,  0.  ,  0.  ,  0.16,
        0.61,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,
        0.  ,  0.  ,  0.28,  0.1 ,  0.6 ,  0.63,  2.24,  0.  ,  0.  ,
        0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,
        0.  ,  3.58,  0.  ,  0.  ,  8.18,  2.51,  3.34,  0.28,  0.  ,
        0.  ,  0.  ,  8.08, 15.07,  0.  ,  2.58,  0.  ,  0.  ,  0.  ,
        0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,
        0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,
        0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.09]).reshape(1,-1)


kernal_pcaed_data = pca.transform(test_data)[0]
input_data = np.concatenate((kernal_pcaed_data, [test_batch_size]))
test_pred = predictor.predict(input_data.reshape(1, -1))

print(test_target_rate, test_pred)

