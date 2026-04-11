from loaders import get_loader
from filters.filter import Filter
from aggregators import get_aggregator
from features.registry import get_feature_engine


def run_pipeline(mode:str,stock:str,timeframe:str = None) :

    #Load Data
    loader = get_loader(mode);
    df = loader.load(stock)


    #Filter only required columns
    filter = Filter(df,mode)
    df = filter.filter(df,mode)


    #Aggregate the columns depending on the timeframe
    aggregator = get_aggregator(mode,timeframe)
    df = aggregator.transform(df);

    
    #finally apply features
    feature_engine = get_feature_engine(mode)
    df = feature_engine.transform(df)   


    #Clean
    df = df.dropna()


        