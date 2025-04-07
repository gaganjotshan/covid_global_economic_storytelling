from dash import Dash, dcc, html
import plotly.graph_objects as go
import pandas as pd


def render(app: Dash, dataset: pd.DataFrame) -> html.Div:
    merch_tarde_df = dataset[['country', 'year', 'Merchandise_Trade']]
    countries = ['Russian Federation', 'United States', 'China']
    data = {country: merch_tarde_df[merch_tarde_df['country']==country] for country in countries}

    fig = go.Figure()

    for country, dataframe in data.items():
        fig.add_trace(go.Scatter(
            x=dataframe['year'],
            y=dataframe['Merchandise_Trade'],
            mode='lines',
            name=country
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
        title='Merch Trade per country',
        xaxis_title='Year',
        yaxis_title='Merch Trade',
        width=1000,
        height=500
    )

    return html.Div(
            dcc.Graph(figure=fig), id='merch_trade'
        )
    