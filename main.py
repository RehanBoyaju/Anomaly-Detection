import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir():
    sys.path.insert(0, str(_SRC))

import numpy as np
from scipy.stats import zscore
# from statsmodels.tsa.seasonal import seasonal_decompose
from pipeline.run_pipeline import run_pipeline
from engines.engine import engine
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
timeframe="1min"

features = ["quantity", "return", "SMA_5", "SMA_20", "EMA_10"]
models=["z-score","residuals","isolation-forest"]

n_estimators=200
contamination=0.02


X_train,X_test,df_train,df_test = run_pipeline(stock_name,train_start_date,train_end_date,test_start_date,test_end_date,mode,features,timeframe);

max_depth = int(np.ceil(np.log2(len(X_train))))



train_scores,test_scores,threshold = engine(X_train,X_test,n_estimators,contamination,max_depth)

# Use the threshold to get anomalies
df_train['anomaly_score'] = train_scores
df_train['anomalous'] = train_scores - threshold<0

df_test['anomaly_score'] = test_scores
df_test['anomalous'] = test_scores - threshold < 0 

#sort and display the highest latest scores
# df_test[df_test['Anomaly_IF']==True].sort_index(ascending=False).head() 



#Plot training data
plot_ohlcv(stock_name,df_train,period="Train")
plot_results(mode,stock_name,threshold,df_train,period="Train")

#Plot test results
plot_ohlcv(stock_name,df_test,period="Train")
plot_results(mode,stock_name,threshold,df_test,period="Test")



# Inspect and optionally save the top-N anomalies from the test period
top_n = 20

TopAnoms = df_test.sort_values('anomaly_score', ascending=True).head(top_n)
print(f"The anomaly threshold is {threshold}")
print(f"Top {top_n} most anomalous dates in test set:")
print(TopAnoms[['close', 'quantity', 'return', 'anomaly_score', 'anomalous']])







#MAJOR EVENTS
#2025-09-* is the GENZ Revolution

#20**-07-* is the Federal Budget Season

#2026-03-09 NEPSE Hits 6% circuit breaker after R.S.P Win
#The next day 2026-03-10 ppl boooked profits and it fell

#2026-03-29 After formation of new govt Oli and Lekhak were arrested leading to NEPSE falling
#2026-04-05 Jagadamba Group CEO was arrested leading to NEPSE freefall 
#2026-03-22 Official win of R.S.P


