import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score, f1_score
from scipy.stats import zscore
from itertools import product
import warnings
warnings.filterwarnings("ignore")

# ============================================================================
# SIMPLIFIED TUNING FUNCTIONS (Inline versions)
# ============================================================================

def quick_tune_isolation_forest(X, y_true, verbose=True):
    """Quick tuning of Isolation Forest."""
    results = []
    
    param_grid = {
        'n_estimators': [100, 200, 300],
        'contamination': [0.005, 0.01, 0.02, 0.05]
    }
    
    combinations = list(product(
        param_grid['n_estimators'],
        param_grid['contamination']
    ))
    
    if verbose:
        print(f"Testing {len(combinations)} Isolation Forest combinations...")
    
    for n_est, contam in combinations:
        try:
            from models.isolation_forest import IsolationForest
            
            model = IsolationForest(
                n_trees=n_est,
                contamination=contam,
                random_state=42
            )
            
            predictions = model.fit_predict(X)
            predictions_binary = (predictions == -1).astype(int)
            
            # Skip if no anomalies
            if predictions_binary.sum() == 0:
                continue
            
            f1 = f1_score(y_true, predictions_binary, zero_division=0)
            precision = precision_score(y_true, predictions_binary, zero_division=0)
            recall = recall_score(y_true, predictions_binary, zero_division=0)
            
            results.append({
                'n_estimators': n_est,
                'contamination': contam,
                'f1_score': f1,
                'precision': precision,
                'recall': recall
            })
            
        except Exception as e:
            if verbose:
                print(f"  Error with n_est={n_est}, contam={contam}: {e}")
    
    if not results:
        # Return empty dataframe with proper structure
        return pd.DataFrame({
            'n_estimators': [200],
            'contamination': [0.01],
            'f1_score': [0.0],
            'precision': [0.0],
            'recall': [0.0]
        })
    
    results_df = pd.DataFrame(results).sort_values('f1_score', ascending=False)
    
    if verbose:
        print(f"\n✓ Best F1-Score: {results_df.iloc[0]['f1_score']:.4f}")
        print(f"✓ Best Parameters: n_estimators={int(results_df.iloc[0]['n_estimators'])}, "
              f"contamination={results_df.iloc[0]['contamination']:.4f}\n")
    
    return results_df


def quick_tune_dbscan(X, y_true, verbose=True):
    """Quick tuning of DBSCAN."""
    from models.dbscan import DBSCAN
    
    results = []
    
    param_grid = {
        'eps': [0.5, 1.0, 1.5, 2.0],
        'min_pts': [5, 10, 15]
    }
    
    combinations = list(product(
        param_grid['eps'],
        param_grid['min_pts']
    ))
    
    if verbose:
        print(f"Testing {len(combinations)} DBSCAN combinations...")
    
    for eps, min_pts in combinations:
        try:
            model = DBSCAN(eps=eps, min_pts=min_pts)
            predictions = model.fit_predict(X)
            
            # FIX: Handle case where DBSCAN returns boolean or scalar
            if isinstance(predictions, (bool, np.bool_)):
                if verbose:
                    print(f"  Error with eps={eps}, min_pts={min_pts}: Invalid return type (boolean)")
                continue
            
            # Convert to numpy array if needed
            predictions = np.asarray(predictions)
            
            # Check if it's a scalar
            if predictions.ndim == 0:
                if verbose:
                    print(f"  Error with eps={eps}, min_pts={min_pts}: Scalar return value")
                continue
            
            # Now safe to convert to int
            predictions_binary = (predictions == -1).astype(int)
            
            if predictions_binary.sum() == 0:
                continue
            
            f1 = f1_score(y_true, predictions_binary, zero_division=0)
            precision = precision_score(y_true, predictions_binary, zero_division=0)
            recall = recall_score(y_true, predictions_binary, zero_division=0)
            
            results.append({
                'eps': eps,
                'min_pts': min_pts,
                'f1_score': f1,
                'precision': precision,
                'recall': recall
            })
            
        except Exception as e:
            if verbose:
                print(f"  Error with eps={eps}, min_pts={min_pts}: {str(e)[:60]}")
    
    if not results:
        # Return empty dataframe with proper structure
        return pd.DataFrame({
            'eps': [1.0],
            'min_pts': [5],
            'f1_score': [0.0],
            'precision': [0.0],
            'recall': [0.0]
        })
    
    results_df = pd.DataFrame(results).sort_values('f1_score', ascending=False)
    
    if verbose:
        print(f"\n✓ Best F1-Score: {results_df.iloc[0]['f1_score']:.4f}")
        print(f"✓ Best Parameters: eps={results_df.iloc[0]['eps']:.2f}, "
              f"min_pts={int(results_df.iloc[0]['min_pts'])}\n")
    
    return results_df


def quick_tune_z_score(df, y_true, feature='close', verbose=True):
    """Quick tuning of Z-Score threshold."""
    
    results = []
    thresholds = np.arange(1.5, 4.5, 0.5)
    
    if verbose:
        print(f"Testing {len(thresholds)} Z-Score thresholds...")
    
    z_scores = zscore(df[feature].dropna())
    
    for threshold in thresholds:
        predictions_binary = (np.abs(z_scores) > threshold).astype(int)
        
        if predictions_binary.sum() == 0:
            continue
        
        # Need to align with y_true
        valid_idx = df[feature].notna()
        y_valid = y_true[valid_idx]
        
        if len(y_valid) != len(predictions_binary):
            continue
        
        f1 = f1_score(y_valid, predictions_binary, zero_division=0)
        precision = precision_score(y_valid, predictions_binary, zero_division=0)
        recall = recall_score(y_valid, predictions_binary, zero_division=0)
        
        results.append({
            'threshold': threshold,
            'f1_score': f1,
            'precision': precision,
            'recall': recall,
            'n_anomalies': predictions_binary.sum()
        })
    
    if not results:
        # Return empty dataframe with proper structure
        return pd.DataFrame({
            'threshold': [3.0],
            'f1_score': [0.0],
            'precision': [0.0],
            'recall': [0.0],
            'n_anomalies': [0]
        })
    
    results_df = pd.DataFrame(results).sort_values('f1_score', ascending=False)
    
    if verbose:
        print(f"\n✓ Best F1-Score: {results_df.iloc[0]['f1_score']:.4f}")
        print(f"✓ Best Threshold: {results_df.iloc[0]['threshold']:.2f}\n")
    
    return results_df


# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def plot_if_tuning(results_df):
    """Plot Isolation Forest tuning results."""
    try:
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        
        for n_est in results_df['n_estimators'].unique():
            subset = results_df[results_df['n_estimators'] == n_est].sort_values('contamination')
            axes[0].plot(subset['contamination'], subset['f1_score'], 
                        marker='o', label=f'n_est={int(n_est)}')
        
        axes[0].set_xlabel('Contamination')
        axes[0].set_ylabel('F1-Score')
        axes[0].set_title('Isolation Forest: F1-Score vs Contamination')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Top results
        top_10 = results_df.head(10).sort_values('f1_score')
        axes[1].barh(range(len(top_10)), top_10['f1_score'], color='steelblue')
        labels = [f"n_est={int(row['n_estimators'])}, cont={row['contamination']:.3f}" 
                  for _, row in top_10.iterrows()]
        axes[1].set_yticks(range(len(top_10)))
        axes[1].set_yticklabels(labels, fontsize=9)
        axes[1].set_xlabel('F1-Score')
        axes[1].set_title('Top 10 Parameter Combinations')
        
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Could not plot Isolation Forest results: {e}")


def plot_dbscan_tuning(results_df):
    """Plot DBSCAN tuning results as heatmap."""
    try:
        import seaborn as sns
        
        # Check if we have enough data to pivot
        if len(results_df) < 2:
            print("Not enough DBSCAN results to plot")
            return
        
        # Pivot for heatmap
        pivot_table = results_df.pivot_table(
            index='min_pts',
            columns='eps',
            values='f1_score',
            aggfunc='mean'
        )
        
        if pivot_table.empty:
            print("Could not create pivot table for DBSCAN")
            return
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(pivot_table, annot=True, fmt='.3f', cmap='RdYlGn', 
                    cbar_kws={'label': 'F1-Score'})
        plt.title('DBSCAN: F1-Score Heatmap')
        plt.xlabel('eps')
        plt.ylabel('min_pts')
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Could not plot DBSCAN results: {e}")


def plot_zscore_tuning(results_df):
    """Plot Z-Score tuning results."""
    try:
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        
        axes[0].plot(results_df['threshold'], results_df['f1_score'], 
                    marker='o', color='red', linewidth=2, markersize=8)
        axes[0].set_xlabel('Threshold')
        axes[0].set_ylabel('F1-Score')
        axes[0].set_title('Z-Score: F1-Score vs Threshold')
        axes[0].grid(True, alpha=0.3)
        
        axes[1].plot(results_df['threshold'], results_df['n_anomalies'], 
                    marker='s', color='purple', linewidth=2, markersize=8)
        axes[1].set_xlabel('Threshold')
        axes[1].set_ylabel('Number of Anomalies')
        axes[1].set_title('Z-Score: Anomaly Count vs Threshold')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Could not plot Z-Score results: {e}")


# ============================================================================
# MAIN EXECUTION SECTION - INSERT INTO YOUR NOTEBOOK
# ============================================================================

def run_hyperparameter_tuning(df, features, verbose=True):
    """
    Complete hyperparameter tuning pipeline.
    
    Usage:
    ------
    best_params = run_hyperparameter_tuning(df, features=['close', 'volume', 'returns', 'volatility'])
    
    Returns:
    --------
    best_params : dict
        Dictionary with best parameters for each method
    """
    
    print("\n" + "="*60)
    print("HYPERPARAMETER TUNING FOR ANOMALY DETECTION")
    print("="*60 + "\n")
    
    # Create ground truth
    df["True_Anomaly"] = df["close"].pct_change().abs() > 0.05
    
    # Prepare data
    X = df[features].values
    X = StandardScaler().fit_transform(X)
    y_true = df["True_Anomaly"].values
    
    best_params = {}
    
    # =====================
    # 1. ISOLATION FOREST
    # =====================
    print("1️⃣  TUNING ISOLATION FOREST")
    print("-" * 60)
    
    results_if = quick_tune_isolation_forest(X, y_true, verbose=verbose)
    
    best_params['isolation_forest'] = {
        'n_estimators': int(results_if.iloc[0]['n_estimators']),
        'contamination': float(results_if.iloc[0]['contamination'])
    }
    
    if verbose and len(results_if) > 0:
        print("Results:")
        print(results_if[['n_estimators', 'contamination', 'precision', 'recall', 'f1_score']].head())
    
    try:
        plot_if_tuning(results_if)
    except Exception as e:
        print(f"Could not plot Isolation Forest: {e}")
    
    # =====================
    # 2. DBSCAN
    # =====================
    print("\n2️⃣  TUNING DBSCAN")
    print("-" * 60)
    
    results_dbscan = quick_tune_dbscan(X, y_true, verbose=verbose)
    
    best_params['dbscan'] = {
        'eps': float(results_dbscan.iloc[0]['eps']),
        'min_pts': int(results_dbscan.iloc[0]['min_pts'])
    }
    
    if verbose and len(results_dbscan) > 0:
        print("Results:")
        cols_to_show = [c for c in ['eps', 'min_pts', 'precision', 'recall', 'f1_score'] 
                       if c in results_dbscan.columns]
        print(results_dbscan[cols_to_show].head())
    
    try:
        plot_dbscan_tuning(results_dbscan)
    except Exception as e:
        print(f"Could not plot DBSCAN: {e}")
    
    # =====================
    # 3. Z-SCORE
    # =====================
    print("\n3️⃣  TUNING Z-SCORE")
    print("-" * 60)
    
    results_zscore = quick_tune_z_score(df, y_true, verbose=verbose)
    
    best_params['z_score'] = {
        'threshold': float(results_zscore.iloc[0]['threshold'])
    }
    
    if verbose and len(results_zscore) > 0:
        print("Results:")
        print(results_zscore[['threshold', 'precision', 'recall', 'f1_score', 'n_anomalies']])
    
    try:
        plot_zscore_tuning(results_zscore)
    except Exception as e:
        print(f"Could not plot Z-Score: {e}")
    
    # =====================
    # SUMMARY
    # =====================
    print("\n" + "="*60)
    print("SUMMARY OF BEST PARAMETERS")
    print("="*60)
    
    for method, params in best_params.items():
        print(f"\n{method.upper()}:")
        for param, value in params.items():
            print(f"  {param}: {value}")
    
    return best_params, {'if': results_if, 'dbscan': results_dbscan, 'zscore': results_zscore}


if __name__ == "__main__":
    print("This module is ready to be imported and used in your notebook.")
    print("\nUsage:")
    print("  best_params = run_hyperparameter_tuning(df, features=['close', 'volume', 'returns', 'volatility'])")