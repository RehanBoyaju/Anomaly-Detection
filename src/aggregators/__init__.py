from aggregators.interday_aggregator import InterdayAggregator
from aggregators.intraday_aggregator import IntradayAggregator

AGGREGATOR_REGISTRY={
    "Intraday":IntradayAggregator,
    "Interday":InterdayAggregator
}
def get_aggregator(aggregator_type:str,timeframe:str,features:list):
    try:
        return AGGREGATOR_REGISTRY[aggregator_type](timeframe,features)
    except KeyError:
        raise ValueError(f"Unknown Aggregator type: {aggregator_type}")