class FeatureEngine:
    def __init__(self,features):
        self.features = features
    def transform(self,df):
        raise NotImplementedError