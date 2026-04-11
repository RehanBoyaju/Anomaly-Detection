from features.intraday import IntradayFeatures
from features.interday import InterdayFeatures

def get_feature_engine(mode,features):
    if(mode == "intraday"):
        return IntradayFeatures(features)
    elif(mode=="interday"):
        return InterdayFeatures(features)
    else:
        raise ValueError(f"Unidentified feature{mode}")
