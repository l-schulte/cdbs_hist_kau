import pandas as pd
import plotly.express as px
import progressbar

from __init__ import db_commits


def get_success_graph():

    dataframes = []

    for commit in progressbar.progressbar(db_commits.find({'sonarqube': {'$exists': True}})):

        success = 'status' in commit['sonarqube'] and commit['sonarqube']['status'] is True
        df = pd.DataFrame([success], [commit['date']], ['success'])
        dataframes.append(df)

    result = pd.concat(dataframes)

    fig = px.scatter(result, x=result.index, y=result.columns, title='Import Success')
    fig.show()
