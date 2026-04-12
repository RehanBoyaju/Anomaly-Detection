import numpy as np
from models.isolation_forest import IsolationForest

def isolation_engine(X_train,X_test,n_estimators,contamination):

    max_depth = int(np.ceil(np.log2(len(X_train))))

    model= IsolationForest(
        n_trees=n_estimators,
        contamination=contamination,
        max_depth = max_depth
    )
    print("Building isolation trees..")
    model.fit(X_train)
    print("Calculating anomaly scores for test data")
    train_scores = model.anomaly_score(X_train)

    print("Calculating anomaly scores for train data")
    test_scores = model.anomaly_score(X_test)

    return train_scores,test_scores,model.threshold


    