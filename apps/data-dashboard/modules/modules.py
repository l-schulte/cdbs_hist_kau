import modules.architecture as architecture
import modules.history as history


def get_metrics():

    mapping = architecture.get_mapping()
    metrics = {}

    for module in mapping.keys():
        metrics[module] = history.get_metrics(mapping[module])
        break


    return metrics
