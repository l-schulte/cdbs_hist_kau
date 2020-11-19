import modules.architecture as architecture
import modules.history as history


def get_metrics():

    mapping = architecture.get_mapping()
    module_metrics = {}

    module_metrics['cli'] = history.get_metrics_per_day(mapping['cli'])

    return module_metrics
