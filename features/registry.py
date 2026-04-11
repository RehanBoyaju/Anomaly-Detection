from features.intraday import IntradayFeatures
from features.interday import InterdayFeatures

def get_feature_engine(mode,transform):
    if(mode == "intraday"):
        return IntradayFeatures()
    elif(mode=="interday"):
        return InterdayFeatures(window_short=5,window_long=20)
