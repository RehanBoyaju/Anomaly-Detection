from loaders import get_loader
from filters.filter import filter
from aggregators import get_aggregator
from features.registry import get_feature_engine
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


def run_pipeline(
    stock:str,
    train_start,
    train_end,
    test_start,
    test_end,
    mode:str = None,
    features:list = None,
    timeframe:str = None
    ) :

    if not mode:
        mode = "Interday"

    if not features:
        features  = ["rate"]
    
    if not timeframe:
        timeframe = "5min" if mode == "Intraday" else "1D"

    columns = ["transaction_time"] + features



    #Load Data
    loader = get_loader(mode);
    df = loader.load(stock,train_start,test_end)


    #Filter only required columns
    df = filter.filter(df,mode,columns)


    #Aggregate the columns depending on the timeframe
    aggregator = get_aggregator(mode,timeframe,features)
    df = aggregator.transform(df);

    
    #finally apply features
    feature_engine = get_feature_engine(mode,features)
    df = feature_engine.transform(df)   


    #Clean
    df[features] = df[features].apply(pd.to_numeric, errors='coerce') #converts every value in features columns to numeric value & convert incompatible values to nan
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()


    #Split the data sets
    df_train = df.loc[train_start:train_end].copy()
    df_test = df.loc[test_start:test_end].copy()


    #Difference between df and X is that df(Dataframe) is a raw pandas dataframe with columns and timestamps whereas X is a numpy array with only numbers no columns names


    #Scale or Standardize
    #convert the data to have a mean of 0 and a standard deviation of 1 such that the data is normalized and the model can learn better
    #this is important because the model is sensitive to the scale of the data as return maybe in the range of -0.2 to 0.2 but the other features are in the range of 1000 to 1000000 like quantity

    scaler = StandardScaler() 
    X_train = scaler.fit_transform(df_train[features]) 
    X_test = scaler.transform(df_test[features]) 


    return X_train,X_test,df_train,df_test;
    


    