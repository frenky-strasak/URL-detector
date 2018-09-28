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


"""
Split data dor training and testing
"""
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)


"""

"""
import xgboost as xgb
import pickle
from xgboost import XGBClassifier



title = "Learning Curves ( XGBoost s)"
model = XGBClassifier(
    learning_rate=0.1,
    n_estimators=1000,
    max_depth=3,
    min_child_weight=5,
    gamma=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    objective='binary:logistic',
    nthread=4,
    scale_pos_weight=1,
    seed=27)


print('training ...')
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# _xgboost_module = pickle.load(open("/home/frenky/PycharmProjects/url_detector/URL-detector/manager/xgboost_2018_09_27_21_56.sav", "rb"))
# y_pred = _xgboost_module.predict(X_test)

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

print()
print('conf matrix')



print(confusion_matrix(y_test, y_pred))
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

print('tn, fp, fn, tp:')
print(tn, fp, fn, tp)

print('Accuracy:')
print(accuracy_score(y_test, y_pred))


