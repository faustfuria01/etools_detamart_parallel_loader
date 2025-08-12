from mart_project.apps.mart.loader.loader import EtoolsLoader

class PartnerLoader(EtoolsLoader):
    pass

_loaders = {
    "mart.partner": PartnerLoader(),
}

def get_loader_for(model_name: str):
    try:
        return _loaders[model_name]
    except KeyError:
        raise ValueError(f"No loader registered for '{model_name}'")