from numpy.core.numeric import NaN
from numpy.lib.function_base import average
import pandas as pd
import numpy as np
from math import ceil
from scipy.spatial.distance import pdist
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


def get_distinct(metrics, relevant_metrics):
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
            msd = __msd(val)
            dist_metrics_dict[path][metric] = msd

    relevant_metrics.append('count')

    df = pd.DataFrame(dist_metrics_dict, relevant_metrics)

    return df


def show_cluster(data, threshold, criterion='distance'):

    data = data.transpose()

    print(data.shape)
    print(data)

    Z = ward(data)

    res = fcluster(Z, threshold, criterion)

    print(res)

    data.insert(0, 'cluster', res)

    data.to_csv('clusters.csv', ';')

    # fig = plt.figure(figsize=(25, 10))

    # dn = dendrogram(Z)

    # plt.show()
