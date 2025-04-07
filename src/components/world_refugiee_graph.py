from dash import Dash, dcc, html
import plotly.graph_objects as go
import pandas as pd


def render(app: Dash, dataset: pd.DataFrame) -> html.Div:
    refugiee_df = dataset[['country', 'year', 'Refugiee_Population']]
    refugiee_df = refugiee_df[refugiee_df['country']=='World']

    fig = go.Figure()

    fig.add_trace(go.Scatter(
            x=refugiee_df['year'],
            y=refugiee_df['Refugiee_Population'],
            mode='lines',
        ))

    fig.add_vline(
        x=2020,
        line=dict(color='red', width=2, dash='dash'),
        annotation=dict(
            text='COVID crisis start',
            font=dict(color='red'),
            showarrow=False,
            yanchor='bottom',
            y=1.0
        )
    )

    fig.update_layout(
        title='Refugiee Population in the world over the years',
        xaxis_title='Year',
        yaxis_title='Number of Refugiees',
        width=1000,
        height=500
    )


    return html.Div(
            dcc.Graph(figure=fig), id='world_refugiee'
        )
    