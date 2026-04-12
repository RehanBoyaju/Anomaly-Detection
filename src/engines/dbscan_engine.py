import numpy as np
from models.dbscan import DBSCANModel

def dbscan_engine(X_train, X_test, eps_list, min_pts_list):

    best_score = -1
    best_eps = None
    best_min_pts = None

    # -------------------------
    # TRAIN: PARAM SEARCH
    # -------------------------
    for eps in eps_list:
        for min_pts in min_pts_list:

            model = DBSCANModel(eps, min_pts)
            model.fit(X_train)

            labels = model.get_labels()

            noise_ratio = np.mean(np.array(labels) == -1)

            clusters = len(set(labels)) - (1 if -1 in labels else 0)

            score = clusters * (1 - noise_ratio)

            if score > best_score:
                best_score = score
                best_eps = eps
                best_min_pts = min_pts


    print(f"For DBSCAN the best params are eps: {best_eps}, min_pts: {best_min_pts}")


    print(f"Rebuilding clusters with the best params..")

    # -------------------------
    # FINAL MODEL (TRAIN)
    # -------------------------
    final_model = DBSCANModel(best_eps, best_min_pts)
    final_model.fit(X_train)

    train_labels = final_model.get_labels()


    print(f"Fitting the test data with the best params..")

    # -------------------------
    # TEST (same params)
    # -------------------------
    test_model = DBSCANModel(best_eps, best_min_pts)
    test_model.fit(X_test)
    test_labels = test_model.get_labels()

    # -------------------------
    # SCORING (match your system)
    # -------------------------
    train_scores = np.where(np.array(train_labels) == -1, 1.0, 0.0)
    test_scores  = np.where(np.array(test_labels) == -1, 1.0, 0.0)

    threshold = 0.5


    return train_scores, test_scores, threshold