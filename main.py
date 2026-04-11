import pandas as pd
import numpy as np
from scipy.stats import zscore 
# from statsmodels.tsa.seasonal import seasonal_decompose
from models.isolation_forest import IsolationForest
from pathlib import Path
from pipeline.run_pipeline import run_pipeline
from engines.engine import engine
from analysis.visualizer import plot_results
import warnings
warnings.filterwarnings('ignore')



stock_name = "NABIL"
mode = "intraday"
train_start_date = "2020-01-01"
train_end_date = "2025-01-01"
test_start_date = "2025-01-01"
test_end_date = "2026-04-08"
features = ['rate', 'quantity', 'return', 'SMA_5', 'SMA_20', 'EMA_10']
n_estimators=200
contamination=0.05


X_train,X_test,df_train,df_test = run_pipeline(stock_name,train_start_date,test_end_date,mode,features,timeframe="1D");

max_depth = int(np.ceil(np.log2(len(X_train))))
#ceil(log2(max_samples))

scores,threshold = engine(X_train,X_test,n_estimators,contamination,max_depth)

df_test['anomaly_score'] = scores

# Use the threshold to get anomalies 
df_test['Anomaly_IF'] = scores - threshold < 0 

# df_test[df_test['Anomaly_IF']==True].sort_index(ascending=False).head()


#Plot Results
plot_results(df_train,df_test)



# Inspect and optionally save the top-N anomalies from the test period
top_n = 20

TopAnoms = df_test.sort_values('anomaly_score', ascending=True).head(top_n)
print(f"The anomaly threshold is {threshold}")
print(f"Top {top_n} most anomalous dates in test set:")
print(TopAnoms[['rate', 'quantity', 'return', 'anomaly_score', 'Anomaly_IF']])







#MAJOR EVENTS
#2025-09-* is the GENZ Revolution

#20**-07-* is the Federal Budget Season

#2026-03-09 NEPSE Hits 6% circuit breaker after R.S.P Win
#The next day 2026-03-10 ppl boooked profits and it fell

#2026-03-29 After formation of new govt Oli and Lekhak were arrested leading to NEPSE falling
#2026-04-05 Jagadamba Group CEO was arrested leading to NEPSE freefall 
#2026-03-22 Official win of R.S.P




# %%
