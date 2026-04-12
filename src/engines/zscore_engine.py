import numpy as np

def zscore_engine(X_train, X_test,confidence:float = 0.95) :
    # 1. compute feature-wise stats (column-wise)
    mu = np.mean(X_train, axis=0)
    sigma = np.std(X_train, axis=0)

    sigma[sigma == 0] = 1e-8  # avoid division error

    # 2. normalize using training distribution
    train_z = (X_train - mu) / sigma
    test_z = (X_test - mu) / sigma

    # 3. collapse features into single anomaly score per row
    train_scores = np.max(np.abs(train_z), axis=1)
    test_scores = np.max(np.abs(test_z), axis=1)

    threshold = np.percentile(train_scores, confidence*100)

    return train_scores,test_scores,threshold;