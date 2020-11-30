from modules import modules
from files import files
from importer import importer
import pandas as pd

DEG_LIMIT = 5

# importer.get_success_graph()

df = pd.read_csv('source-target-total.csv', ';')

arch_deg_targets = df[df['source'] <= DEG_LIMIT]
arch_deg_targets = arch_deg_targets[arch_deg_targets['target'] > DEG_LIMIT]
arch_deg_targets['color'] = 'red'

arch_deg_sources = df[df['target'] <= DEG_LIMIT]
arch_deg_sources = arch_deg_sources[arch_deg_sources['source'] > DEG_LIMIT]
arch_deg_sources['color'] = 'blue'


files.get_graphs_per_metric(arch_deg_targets)
files.get_graphs_per_metric(arch_deg_sources)

# files.get_graphs_per_file(f)
# importer.get_success_graph()
