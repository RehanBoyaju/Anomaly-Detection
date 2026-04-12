from models.isolation_forest import IsolationForest

def engine(X_train,X_test,n_estimators,contamination,max_depth):

    model= IsolationForest(
        n_trees=n_estimators,
        contamination=contamination,
        max_depth = max_depth
    )

    model.fit(X_train)
    train_scores = model.anomaly_score(X_train)
    test_scores = model.anomaly_score(X_test)

    return train_scores,test_scores,model.threshold


    