import numpy as np

"""
Import features from files to vectors. 
"""
X_malware = np.load('malware_json_features.npy')
X_normal = np.load('normal_json_features.npy')
# X_normal = X_normal[:10258]

print('malware shape {}'.format(X_malware.shape))
print('normal shape {}'.format(X_normal.shape))

"""
Merge vectors and create labels.
"""
X = np.concatenate((X_malware, X_normal), axis=0)
y = np.array([1 for i in range(X_malware.shape[0])] + [0 for j in range(X_normal.shape[0])])

# X = X[:10]
# y = y[:10]

print('X shape {}'.format(X.shape))
print('y shape {}'.format(y.shape))


import xgboost as xgb
import pickle
from xgboost import XGBClassifier
from xgboost import Booster

# title = "Learning Curves ( XGBoost s)"
# model = XGBClassifier(
#     learning_rate=0.1,
#     n_estimators=1,
#     max_depth=3,
#     min_child_weight=5,
#     gamma=0.01,
#     subsample=0.8,
#     colsample_bytree=0.8,
#     objective='binary:logistic',
#     nthread=4,
#     scale_pos_weight=1,
#     seed=27)


from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()

print('training ...')
model.fit(X, y)


from datetime import datetime
date = datetime.now().strftime('%Y_%m_%d_%H_%M')

# # God Save the Queen
filename = 'xgboost_' + date + '.sav'
pickle.dump(model, open(filename, 'wb'))


# sample_download = [2.0, 2.0, 2.0, 30410.5, 17172.5, 2.0, 0.5, 1.0, 50.0, 0.02, 0.02, 0.98, 0.5, 48.06, 18.537971841601227, 0.2, 0.0, 4.0, 0.5, 2.0, 0.0, 1.0, 63072000.0, 0.0, 0.6814429875856151, 0.0, 2.0, 100.0, 0.0, 6.0, 3.0550504633038935, 0.0, -1.0, -1.0, -1.0, -1.0, 10.0, 8.414273587185052, 980618.4, 772962.8699164275, 787343.0, 874571.2909879903, 0.0, 0.0, 3.1399999999999997, 1.9074590428106182, 1.2, 0.4, 1.2, 0.4, 50.0, 0.0, 4903092.0, 0.0, 3936715.0, 0.0, 2.0, 0.0, 2.0, 0.0, 25.0, 24.0, 2451546.0, 2451546.0, 1968357.5, 1968357.5, 1.0, 0.0, 1.0, 0.0, 0.5, 0.5, 49.0, 0.0, 4903092.0, 0.0, 3936715.0, 0.0, 1.0, 0.0, 1.0, 0.0, 25.0, 24.0, 2451546.0, 2451546.0, 1968357.5, 1968357.5, 1.5, 0.5, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 25.0, 24.0, 2451546.0, 2451546.0, 1968357.5, 1968357.5, 1.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2451546.0, 2451546.0, 1968357.5, 1968357.5, 25.0, 24.0, 0.0, 0.0, 1.0, 0.0, 25.0, 24.0, 1.0, 0.0, 1.0, 2.0, 50.0, 2.0, 4.0, 0.0, 50.0, 0.98, 0.13999999999999999, 0.04, 0.19595917942265428, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 78734.3, 99826.69559055835, 98061.84, 117827.38065515333, 317.42, 349.83367991089705, 22420931.883598577, 0.2455274216212905, -1.0, 0.0, -1.0, 0.0, -0.75408, 0.6474067605454858, -0.6893, 0.8305126910529423, -0.6893, 0.8305126910529423, 2.37336, 8.75843774142398, -1.0, 0.0, -1.0, 0.0, -1.0, 0.0, -1.0, 0.0, 20.895979999999998, 33.437227923074005, 20.928800000000003, 33.43665673897437, 0.0, 0.0, 0.0, 0.0, 54.57676000000001, 34.773463751866885, 0.98, 0.13999999999999999, 0.8, 12.6, -0.96, 0.27999999999999997, 1261439.02, 8830080.139999999, -0.96, 0.27999999999999997, 121260.74, 143975.07125510444, 7.0, 933001758.2482007, 813783329.2140613, -605117397.8647993, 813783329.2140613, 83.0, 61.62327946018916, 1.2857142857142858, 0.45175395145262565, 1.0, 0.0, 1.4285714285714286, 0.4948716593053935, 4.0, 0.0, 0.0, 2.0, 14.0, 3.0]
# sample_here = [2.0, 2.0, 2.0, 30410.5, 17172.5, 2.0, 0.5, 1.0, 50.0, 0.02, 0.02, 0.98, 0.5, 48.06, 18.537971841601227, 0.2, 0.0, 4.0, 0.5, 2.0, 0.0, 1.0, 63072000.0, 0.0, 0.6697387665683646, 0.0, 2.0, 100.0, 0.0, 6.0, 3.0550504633038935, 0.0, -1.0, -1.0, -1.0, -1.0, 10.0, 8.414273587185052, 969882.8, 755207.2310793641, 776608.0, 856418.6024747478, 0.0, 0.0, 3.1399999999999997, 1.9074590428106182, 1.2, 0.4, 1.2, 0.4, 50.0, 0.0, 4849414.0, 0.0, 3883040.0, 0.0, 2.0, 0.0, 2.0, 0.0, 25.0, 24.0, 2424707.0, 2424707.0, 1941520.0, 1941520.0, 1.0, 0.0, 1.0, 0.0, 0.5, 0.5, 49.0, 0.0, 4849414.0, 0.0, 3883040.0, 0.0, 1.0, 0.0, 1.0, 0.0, 25.0, 24.0, 2424707.0, 2424707.0, 1941520.0, 1941520.0, 1.5, 0.5, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 25.0, 24.0, 2424707.0, 2424707.0, 1941520.0, 1941520.0, 1.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2424707.0, 2424707.0, 1941520.0, 1941520.0, 25.0, 24.0, 0.0, 0.0, 1.0, 0.0, 25.0, 24.0, 1.0, 0.0, 1.0, 2.0, 50.0, 2.0, 4.0, 0.0, 50.0, 0.98, 0.13999999999999999, 0.04, 0.19595917942265428, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 77660.8, 100250.5672714125, 96988.28, 118362.16682809418, 317.42, 349.83367991089705, 21682723.37580844, 0.23033628456505356, -1.0, 0.0, -1.0, 0.0, -0.8138200000000001, 0.4742897295957398, -0.22396000000000002, 4.086972189579959, -0.22396000000000002, 4.086972189579959, 3.5960799999999993, 13.138623955102757, -0.38594, 4.29842, 0.28486000000000006, 8.994019999999999, -1.0, 0.0, -1.0, 0.0, 16.42392, 32.08227349041211, 16.602919999999997, 32.02540228183871, 0.0, 0.0, 0.0, 0.0, 49.82178, 38.23515316108463, 0.98, 0.13999999999999999, 0.8, 12.6, -0.96, 0.27999999999999997, 1261439.02, 8830080.139999999, -0.96, 0.27999999999999997, 120187.4, 144585.33404284128, 7.0, 932579924.6963717, 813420606.5558317, -604801022.7886283, 813420606.5558317, 83.0, 61.62327946018916, 1.2857142857142858, 0.45175395145262565, 1.0, 0.0, 1.4285714285714286, 0.4948716593053935, 4.0, 0.0, 0.0, 2.0, 14.0, 3.0]
# res = model.predict(np.array([sample_download, sample_here]))
# print(res)