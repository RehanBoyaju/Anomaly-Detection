from models.isolation_forest import IsolationForest

def engine(X_train,X_test,n_estimators,contamination,max_depth):

    model= IsolationForest(
        n_trees=n_estimators,
        contamination=contamination,
        max_depth = max_depth
    )

    model.fit(X_train)
    
    scores = model.anomaly_score(X_test)

    return scores


    