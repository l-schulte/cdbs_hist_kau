from numpy.core.numeric import NaN
from numpy.lib.function_base import average
import pandas as pd
from scipy.cluster.hierarchy import fcluster, ward, dendrogram
from matplotlib import pyplot as plt


def __msd(r):
    """Mean square displacement

    """

    mean = average(r)
    n = len(r)
    if n > 0:
        return 1/n * sum([pow(x - mean, 2) for x in r])
    return 0


def __soc(r):
    """Sum of change

    """
    n = len(r)
    if n > 0:
        return sum([abs(r[i-1]-r[i]) for i in range(1, n)])
    return 0


def __msc(r):
    """Mean sum of change

    """
    n = len(r)
    if n > 0:
        return 1/n * __soc(r)
    return 0


def get_distinct(metrics, relevant_metrics, method):
    """Distinct table of the files metrics

    """

    metrics = metrics.fillna(0)

    dist_metrics_dict = {}

    for _, row in metrics.iterrows():

        path = row['path']

        if path not in dist_metrics_dict:
            dist_metrics_dict[path] = {}
            dist_metrics_dict[path]['count'] = 0

        dist_metrics_dict[path]['count'] += 1

        for metric in relevant_metrics:

            if metric not in dist_metrics_dict[path]:
                dist_metrics_dict[path][metric] = []

            if row[metric] is not NaN:
                dist_metrics_dict[path][metric].append(int(row[metric]))

    for path in dist_metrics_dict.keys():
        for metric in relevant_metrics:
            val = dist_metrics_dict[path][metric]

            if method == 'msd':
                val = __msd(val)
            elif method == 'msc':
                val = __msc(val)
            elif method == 'soc':
                val = __soc(val)
            dist_metrics_dict[path][metric] = val

    relevant_metrics.append('count')

    df = pd.DataFrame(dist_metrics_dict, relevant_metrics)

    return df


def get_cluster(data, threshold, criterion='distance'):

    Z = ward(data)
    res = fcluster(Z, threshold, criterion)

    print(res)

    data.insert(0, 'cluster', res)

    return data
