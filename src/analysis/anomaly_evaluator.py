import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix


class AnomalyEvaluator:
    def __init__(self, df):
        self.df = df.copy()
        self.df = self.df.sort_index()

    # -----------------------------
    # 1. FEATURE ENGINEERING RESET
    # -----------------------------
    def compute_base_features(self):
        self.df["returns"] = self.df["close"].pct_change()
        self.df["volatility"] = self.df["returns"].rolling(20).std()
        return self.df

    # -----------------------------
    # 2. ANOMALY INJECTION
    # -----------------------------
    def inject_anomalies(self, fraction=0.01, price_range=(0.01, 0.03), vol_multiplier=(3, 6)):
        n = len(self.df)
        k = int(n * fraction)

        self.df["Injected"] = 0

        idxs = np.random.choice(self.df.index, size=k, replace=False)

        for idx in idxs:
            self.df.loc[idx, "Injected"] = 1

            choice = np.random.choice(["price_up", "price_down", "volume"])

            if choice == "price_up":
                self.df.loc[idx, "close"] *= (1 + np.random.uniform(*price_range))

            elif choice == "price_down":
                self.df.loc[idx, "close"] *= (1 - np.random.uniform(*price_range))

            elif choice == "volume":
                self.df.loc[idx, "volume"] *= np.random.uniform(*vol_multiplier)

        return self.df

    # -----------------------------
    # 3. RECOMPUTE DEPENDENT FEATURES
    # -----------------------------
    def recompute_features(self):
        self.df["returns"] = self.df["close"].pct_change()
        self.df["volatility"] = self.df["returns"].rolling(20).std()
        return self.df

    # -----------------------------
    # 4. CREATE GROUND TRUTH
    # -----------------------------
    def build_ground_truth(self, use_rule=True):
        returns = self.df["returns"]
        rolling_std = returns.rolling(20).std()

        # Is today's movement > 3 times the normal volatility?
        rule_anomaly = returns.abs() > 3 * rolling_std if use_rule else 0

        self.df["True_Anomaly"] = (
            (self.df["Injected"] == 1) | rule_anomaly
        ).astype(int)

        return self.df

    # -----------------------------
    # 5. EVALUATE MODEL
    # -----------------------------
    def evaluate(self, predictions_dict):
        results = []

        y_true = self.df["True_Anomaly"]

        for name, preds in predictions_dict.items():

            y_pred = preds.astype(int)

            precision = precision_score(y_true, y_pred, zero_division=0)
            recall = recall_score(y_true, y_pred, zero_division=0)
            f1 = f1_score(y_true, y_pred, zero_division=0)
            cm = confusion_matrix(y_true, y_pred)

            results.append({
                "Method": name,
                "Precision": precision,
                "Recall": recall,
                "F1-Score": f1,
                "Confusion_Matrix": cm
            })

        return pd.DataFrame(results)







# from anomaly_eval import AnomalyEvaluator

evaluator = AnomalyEvaluator(df)

# 1. base features
evaluator.compute_base_features()

# 2. inject anomalies
evaluator.inject_anomalies(fraction=0.01)

# 3. recompute after injection
evaluator.recompute_features()

# 4. ground truth
evaluator.build_ground_truth()

# 5. run models
predictions = {
    "Z_Score": (abs(evaluator.df["close"].pct_change()) > 0.03),
    "Isolation_Forest": (df["Anomaly_Isolation_Forest"] == -1),
    "DBSCAN": (df["Anomaly_DBSCAN"] == -1)
}

# 6. evaluate
results = evaluator.evaluate(predictions)

print(results)