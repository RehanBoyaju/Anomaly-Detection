import numpy as np

class IsolationForest:
    def __init__(self, n_trees=50, max_depth=8, contamination=0.02):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.contamination = contamination
        self.trees = []
        self.threshold = None

    def fit(self, X):
        self.trees = []

        # Build trees
        for _ in range(self.n_trees):
            tree = self._build_tree(X, depth=0)
            self.trees.append(tree)

        # Compute anomaly scores on training data
        train_scores = self.anomaly_score(X)

        # LOWER score = more anomalous → use low percentile
        self.threshold = np.percentile(train_scores, 100 * self.contamination)

        return self

    def _build_tree(self, X, depth):
        if depth >= self.max_depth or len(X) <= 1:
            return {"size": len(X)}

        feature = np.random.randint(X.shape[1])

        min_val = X[:, feature].min()
        max_val = X[:, feature].max()

        if min_val == max_val:
            return {"size": len(X)}

        split = np.random.uniform(min_val, max_val)

        left = X[X[:, feature] < split]
        right = X[X[:, feature] >= split]

        return {
            "feature": feature,
            "split": split,
            "left": self._build_tree(left, depth + 1),
            "right": self._build_tree(right, depth + 1)
        }

    def _path_length(self, x, node, depth=0):
        if "size" in node:
            return depth

        if x[node["feature"]] < node["split"]:
            return self._path_length(x, node["left"], depth + 1)
        else:
            return self._path_length(x, node["right"], depth + 1)

    def anomaly_score(self, X):
        scores = []
        for x in X:
            path_lengths = [self._path_length(x, tree) for tree in self.trees]
            scores.append(np.mean(path_lengths))
        return np.array(scores)

    def decision_function(self, X):
        scores = self.anomaly_score(X)
        return scores - self.threshold
