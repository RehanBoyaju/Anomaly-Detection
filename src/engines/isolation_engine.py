import numpy as np
from models.isolation_forest import IsolationForest

def isolation_engine(X_train,X_test,n_estimators,contamination):

    max_depth = int(np.ceil(np.log2(len(X_train))))

    model= IsolationForest(
        n_trees=n_estimators,
        contamination=contamination,
        max_depth = max_depth
    )

    model.fit(X_train)
    train_scores = model.anomaly_score(X_train)
    test_scores = model.anomaly_score(X_test)

    return train_scores,test_scores,model.threshold


    