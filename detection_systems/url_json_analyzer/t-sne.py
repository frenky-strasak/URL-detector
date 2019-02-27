"""
t-sne
"""
import numpy as np

"""
Import features from files to vectors. 
"""
X_malware = np.load('raw_features_2/malware_json_features.npy')
X_normal = np.load('raw_features_2/normal_json_features.npy')
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

from sklearn.manifold import TSNE
tsne = TSNE(n_components=2, random_state=0)


X_2d = tsne.fit_transform(X)

target_ids = range(len(y))


from matplotlib import pyplot as plt


plt.figure(figsize=(10, 5))
# plt.subplot(121)
plt.scatter(X_2d[:, 0], X_2d[:, 1], c=y)


plt.legend()
plt.show()
