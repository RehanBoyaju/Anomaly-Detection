from loaders import get_loader
from filters.filter import filter
from aggregators import get_aggregator
from features.registry import get_feature_engine


def run_pipeline(
    stock:str,
    train_start_date,
    train_end_date,
    test_start_date,
    test_end_date,
    mode:str = None,
    features:list = None,
    timeframe:str = None
    ) :

    if not mode:
        mode = "Interday"

    if not features:
        features  = "rate"
    
    if not timeframe:
        timeframe = "5min" if mode == "Intraday" else "1D"

    columns = ["transaction_time"] + features

    #Load Data
    loader = get_loader(mode);
    df = loader.load(stock,train_start_date,test_end_date)


    #Filter only required columns
    df = filter.filter(df,mode,columns)


    #Aggregate the columns depending on the timeframe
    aggregator = get_aggregator(mode,timeframe,features)
    df = aggregator.transform(df);

    
    #finally apply features
    feature_engine = get_feature_engine(mode,features)
    df = feature_engine.transform(df)   


    #Clean
    df = df.dropna()


    #Split
    


    