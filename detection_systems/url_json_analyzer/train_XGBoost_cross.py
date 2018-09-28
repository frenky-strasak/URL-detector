import numpy as np

"""
Import features from files to vectors. 
"""
X_malware = np.load('malware_json_features_2.npy')
X_normal = np.load('normal_json_features_2.npy')
# X_normal = X_normal[:10258]

print('malware shape {}'.format(X_malware.shape))
print('normal shape {}'.format(X_normal.shape))

"""
Merge vectors and create labels.
"""
X = np.concatenate((X_malware, X_normal), axis=0)
y = np.array([1 for i in range(X_malware.shape[0])] + [0 for j in range(X_normal.shape[0])])

print('X shape {}'.format(X.shape))
print('y shape {}'.format(y.shape))



import xgboost as xgb
import pickle
from xgboost import XGBClassifier



# title = "Learning Curves ( XGBoost s)"
# model = XGBClassifier(
#     learning_rate=0.1,
#     n_estimators=1000,
#     max_depth=3,
#     min_child_weight=5,
#     gamma=0.1,
#     subsample=0.8,
#     colsample_bytree=0.8,
#     objective='binary:logistic',
#     nthread=4,
#     scale_pos_weight=1,
#     seed=27)

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
model = RandomForestClassifier(random_state=0)



from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5)

print(scores)
