from modules import modules
from plotter import plotter

modules_metrics = modules.get_metrics()

for module, metrics in modules_metrics.items():

    for metric, days in metrics.items():
        try:
            x = [*days.keys()]
            y = [v['value'] / v['count'] for v in days.values()]
            plotter.draw_scatter(x, y, metric)
        except Exception:
            print('{} metric skipped'.format(metric))
