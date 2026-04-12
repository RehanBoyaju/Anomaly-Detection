from engines.isolation_engine import isolation_engine
from engines.zscore_engine import zscore_engine
from engines.dbscan_engine import dbscan_engine


def orchestrate(X, df, models, params):

    results = {}

    isolation_forest_params, dbscan_params, z_score_params = params
    X_train, X_test = X
    df_train, df_test = df
    df_train, df_test = df_train.copy(), df_test.copy()

    for model in models:

        if model == "z_score":
            print("Calculating z-scores...")
            train_scores, test_scores, threshold = zscore_engine(
                X_train, X_test, z_score_params["confidence_level"]
            )
            print("Z-scores calculated successfully.")

        elif model == "dbscan":
            print("Finding the best params from the given dataset for DBSCAN")
            train_scores, test_scores, threshold = dbscan_engine(
                X_train,
                X_test,
                dbscan_params["eps_list"],
                dbscan_params["min_pts_list"],
            )
            print("DBSCAN Analysis successful")

        elif model == "isolation_forest":
            print("Applying isolation forest..")
            train_scores, test_scores, threshold = isolation_engine(
                X_train,
                X_test,
                isolation_forest_params["n_estimators"],
                isolation_forest_params["contamination"],
            )
            print("Isolation Forest Successful.")

        results[model] = {
            "train_scores": train_scores,
            "test_scores": test_scores,
            "threshold": threshold,
        }

        # Use the threshold to get anomalies
        df_train[f"anomaly_score_{model}"] = train_scores
        df_train[f"anomalous_{model}"] = train_scores > threshold

        df_test[f"anomaly_score_{model}"] = test_scores
        df_test[f"anomalous_{model}"] = test_scores > threshold

        # sort and display the highest latest scores
        # df_test[df_test['Anomaly_IF']==True].sort_index(ascending=False).head()

    df = df_train, df_test

    return results, df
