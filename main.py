import sys
from pathlib import Path
from datetime import datetime

_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir():
    sys.path.insert(0, str(_SRC))

from pipeline.run_pipeline import run_pipeline
from services.orchestrator import orchestrate
from analysis.matplotlib_visualizer import plot_results
from analysis.mpf_visualizer import plot_ohlcv
import warnings
warnings.filterwarnings('ignore')



stock_name = "NABIL"

mode = "Interday"
train_start_date = datetime.strptime("2020-03-08","%Y-%m-%d")
train_end_date = datetime.strptime("2024-04-08","%Y-%m-%d")
test_start_date = datetime.strptime("2025-04-08","%Y-%m-%d")
test_end_date = datetime.strptime("2026-04-08","%Y-%m-%d")
timeframe="1D"

# mode = "Intraday"
# train_start_date = "2025-07-06"
# train_end_date = "2025-09-28"
# test_start_date = "2026-04-09"
# test_end_date = "2026-04-10"
# timeframe="5min"

features = ["quantity", "return", "SMA_5", "SMA_20", "EMA_10"]

models=["z_score","dbscan","isolation_forest"]

isolation_forest_params = {"n_estimators": 200, "contamination": 0.05}

dbscan_params = { "eps_list": [0.3, 0.5, 0.7],"min_pts_list": [3, 5, 10]}

z_score_params = {"confidence_level": 0.95}

params = isolation_forest_params,dbscan_params,z_score_params

dates = {
        "train_start":train_start_date,
        "train_end":train_end_date,
        "test_start":test_start_date,
        "test_end":test_end_date
    }

print(dates);
X,df = run_pipeline(stock_name,dates,mode,features,timeframe);


results,(df_train,df_test) = orchestrate(X,df,models,params);

# plot_ohlcv(stock_name,df_train,period="Train")
plot_ohlcv(stock_name,df_test,period="Test")


top_n = 20

for model in models :

    threshold = results[model]["threshold"]
    #Plot training data
    # plot_results(mode,stock_name,threshold,df_train,period="Train",model=model)

    #Plot test results
    plot_results(mode,stock_name,threshold,df_test,period="Test",model=model)



    # Inspect and optionally save the top-N anomalies from the test period

    TopAnoms = df_test.sort_values(f"anomaly_score_{model}", ascending=False).head(top_n)
    print(str.upper(f"for {model} model"))
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



