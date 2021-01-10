from modules import modules
from files import files
from importer import importer
import pandas as pd
from clusters import clusters
from __init__ import Metric

DEG_LIMIT = 5

# importer.get_success_graph()


def graphs_source_target():

    df = pd.read_csv('source-target-total.csv', ';')

    arch_deg_targets = df[df['source'] <= DEG_LIMIT].sort_values('source', ascending=False)
    arch_deg_targets = arch_deg_targets[arch_deg_targets['target'] > DEG_LIMIT]

    arch_deg_sources = df[df['target'] <= DEG_LIMIT].sort_values('source', ascending=False)[:len(arch_deg_targets)]
    arch_deg_sources = arch_deg_sources[arch_deg_sources['source'] > DEG_LIMIT]

    files.get_graphs_per_metric(arch_deg_targets, category='deg_targets')
    files.get_graphs_per_metric(arch_deg_sources, category='deg_sources')


def graphs_good_bad():
    df = pd.read_csv('source-target-total.csv', ';')

    count = 30

    good = df[df['total'] == 0][:count]
    good['legend'] = 'good'

    bad = df[df['total'] > 0].sort_values('total', ascending=False)[:count]
    bad['legend'] = 'bad'

    df = pd.concat([good, bad])

    print(df)

    files.get_graphs_per_metric(df, category='good_bad', legend='legend')


graphs_good_bad()

# metrics = pd.read_csv('metrics.csv', ';')
# # metrics.to_csv('metrics.csv', sep=';')

# relevant_metrics = [m.value for m in [Metric.FUNCTIONS, Metric.COMPLEXITY, Metric.NCLOC, Metric.DUPLICATED_LINES]]

# data = clusters.get_distinct(metrics, relevant_metrics)
# clusters.show_cluster(data, 1600, 'distance')

# files.get_graphs_per_file(f)
# importer.get_success_graph()
