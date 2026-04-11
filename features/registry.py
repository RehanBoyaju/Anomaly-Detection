from features.intraday import IntradayFeatures
from features.interday import InterdayFeatures

def get_feature_engine(mode,features):
    if(mode == "Intraday"):
        return IntradayFeatures(features)
    elif(mode=="Interday"):
        return InterdayFeatures(features)
    else:
        raise ValueError(f"Unidentified feature{mode}")
