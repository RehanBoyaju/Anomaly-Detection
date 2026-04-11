#%%
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.stats import zscore 
# from statsmodels.tsa.seasonal import seasonal_decompose
from models.isolation_forest import IsolationForest
from pathlib import Path
import warnings
from pipeline.run_pipeline import run_pipeline
from engines.engine import engine

warnings.filterwarnings('ignore')
matplotlib.use("TkAgg")



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



# plot_results(df_train,df_test)

# Plot rate with detected anomalies on the test period

plt.figure(figsize=(20, 10))
# Plot test rate rates
plt.plot(df_test.index, df_test['rate'], label=f"{stock_name} rate (Test Period)")

# Plot moving averages (only for test period)
plt.plot(df_test.index, df_test['SMA_5'], label='SMA 5', linestyle='--', zorder=3)
plt.plot(df_test.index, df_test['SMA_20'], label='SMA 20', linestyle='--', zorder=3)
plt.plot(df_test.index, df_test['EMA_10'], label='EMA 10', linestyle='-.', zorder=3)

# Highlight anomalies
anomaly_idx = df_test.index[df_test['Anomaly_IF']]
plt.scatter(
    anomaly_idx,
    df_test.loc[anomaly_idx, 'rate'],
    color='red',
    label='Detected anomalies (test)',
    zorder=5
)
#draws points with x-axis anomalies, 
# y-axis is rate of the anomalies. df_test is the test data, loc lets you select the rows by labels and specific columns. i.e the label is the list or index of dates where indexes appear
#so we select all the rows in anomaly idx and from each row get the value of 'rate Column'

plt.title(f"{stock_name} rate with IsolationForest anomalies & Moving Averages (test period)")
plt.xlabel('Date')
plt.ylabel('rate')
plt.legend()
plt.show()

# df_to_save = df[['rate','quantity','return','SMA_5', 'SMA_20', 'EMA_10']].copy()

# df_to_save.to_csv("output_plotted_data.csv")







# Diagnostics: distribution of anomaly scores and counts
plt.figure(figsize=(12, 5))
plt.hist(df_test['anomaly_score'], bins=50, color='steelblue', edgecolor='black')
#draws 50 histogram blocks with blue fills and black borders based on the anomaly score of test data
plt.axvline(model_if.threshold, color='red', linestyle='--', label='Anomaly threshold')
#draws a vertical red line at threshold value. right side of threshold is anomalies
plt.title('Distribution of IsolationForest anomaly scores (test set)')
plt.xlabel('Anomaly score (higher = more anomalous)')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout() #this is to make sure the plot is not too crowded
plt.show()

print('Anomaly counts in test set:')
print(df_test['Anomaly_IF'].value_counts())

#shows the count of anomalies and normal points
#also shows that roughly 2% of data were anomalies 





# Inspect and optionally save the top-N anomalies from the test period
top_n = 20

TopAnoms = df_test.sort_values('anomaly_score', ascending=True).head(top_n)
print(f"The anomaly threshold is {model_if.threshold}")
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
