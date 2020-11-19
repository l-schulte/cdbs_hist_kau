import plotly.express as px

# N = 1000
# t = np.linspace(0, 10, 100)
# y = np.sin(t)

# fig = go.Figure(data=go.Scatter(x=t, y=y, mode='markers'))

# fig.show()


def draw_scatter(x, y, title):
    fig = px.line(x=x, y=y, title=title)
    fig.show()
