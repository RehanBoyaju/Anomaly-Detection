import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir():
    sys.path.insert(0, str(_SRC))

from pipeline.run_pipeline import run_pipeline
from engines.isolation_engine import isolation_engine
from engines.zscore_engine import zscore_engine
from engines.residuals_engine import residuals_engine
from analysis.matplotlib_visualizer import plot_results
from analysis.mpf_visualizer import plot_ohlcv
import warnings
warnings.filterwarnings('ignore')



stock_name = "NABIL"

# mode = "Interday"
# train_start_date = "2025-03-08"
# train_end_date = "2026-03-08"
# test_start_date = "2026-03-08"
# test_end_date = "2026-04-08"
# timeframe="1D"

mode = "Intraday"
train_start_date = "2025-07-06"
train_end_date = "2025-09-28"
test_start_date = "2026-04-09"
test_end_date = "2026-04-10"
timeframe="5min"

features = ["quantity", "return", "SMA_5", "SMA_20", "EMA_10"]
# models=["z_score","residuals","isolation_forest"]
models=["isolation_forest"]


n_estimators=200
contamination=0.02


X_train,X_test,df_train,df_test = run_pipeline(stock_name,train_start_date,train_end_date,test_start_date,test_end_date,mode,features,timeframe);

results = {}

for model in models:
    if model == 'z-score':
        train_scores,test_scores,threshold = zscore_engine(X_train,X_test,n_estimators,contamination)
        
    elif model == 'residuals':
        train_scores,test_scores,threshold = residuals_engine(X_train,X_test,n_estimators,contamination)
    
    elif model == 'isolation-forest':
        train_scores,test_scores,threshold = isolation_engine(X_train,X_test,n_estimators,contamination)
    
    
    results[model] = {
        "train_scores" : train_scores,
        "test_scores" : test_scores,
        "threshold" : threshold
    }

     # Use the threshold to get anomalies
    df_train[f"anomaly_score_{model}"] = train_scores
    df_train[f"anomalous_{model}"] = train_scores - threshold<0

    df_test[f"anomaly_score_{model}"] = test_scores
    df_test[f"anomalous_{model}"] = test_scores - threshold < 0 

    #sort and display the highest latest scores
    # df_test[df_test['Anomaly_IF']==True].sort_index(ascending=False).head() 


plot_ohlcv(stock_name,df_train,period="Train")
plot_ohlcv(stock_name,df_test,period="Test")



top_n = 20


for model in models :

    threshold = results[model]["threshold"]
    #Plot training data
    plot_results(mode,stock_name,threshold,df_train,period="Train",model=model)

    #Plot test results
    plot_results(mode,stock_name,threshold,df_test,period="Test",model=model)



    # Inspect and optionally save the top-N anomalies from the test period

    TopAnoms = df_test.sort_values(f"anomaly_score_{model}", ascending=True).head(top_n)
    print(str.upper(f"for{model} model"))
    print(f"The anomaly threshold is {threshold}")
    print(f"Top {top_n} most anomalous dates in test set:")
    print(TopAnoms[['close', 'quantity', 'return', f"anomaly_score_{model}", f"anomalous_{model}"]])
    print()









#MAJOR EVENTS
#2025-09-* is the GENZ Revolution

#20**-07-* is the Federal Budget Season

#2026-03-09 NEPSE Hits 6% circuit breaker after R.S.P Win
#The next day 2026-03-10 ppl boooked profits and it fell

#2026-03-29 After formation of new govt Oli and Lekhak were arrested leading to NEPSE falling
#2026-04-05 Jagadamba Group CEO was arrested leading to NEPSE freefall 
#2026-03-22 Official win of R.S.P


