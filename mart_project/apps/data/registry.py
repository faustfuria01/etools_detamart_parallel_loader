from etools_datamart.apps.mart.data.models.partner import PartnerLoader

_loaders = {
    "mart.partner": PartnerLoader(),
}

def get_loader_for(model_name: str):
    try:
        return _loaders[model_name]
    except KeyError:
        raise ValueError(f"No loader registered for '{model_name}'")
