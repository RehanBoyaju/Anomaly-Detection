from loaders.interday_loader import InterdayLoader
from loaders.intraday_loader import IntradayLoader

LOADER_REGISTRY = {
    "intraday":IntradayLoader,
    "interday":InterdayLoader
}

def get_loader(loader_type:str):
    try:
        return LOADER_REGISTRY[loader_type]();
    except KeyError:
        raise ValueError(f"Unknown loader type: {loader_type}")