from dash import Dash, dcc, html
import plotly.graph_objects as go
import pandas as pd


def render(app: Dash, dataset: pd.DataFrame) -> html.Div:
    gdp_growth_df = dataset[['country', 'year', 'GDP_growth_rate']]
    countries = ['Russian Federation', 'United States', 'China']
    data = {country: gdp_growth_df[gdp_growth_df['country']==country] for country in countries}

    fig = go.Figure()

    for country, dataframe in data.items():
        fig.add_trace(go.Scatter(
            x=dataframe['year'],
            y=dataframe['GDP_growth_rate'],
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
        title='GDP growth rate per country',
        xaxis_title='Year',
        yaxis_title='GDP',
        width=1000,
        height=500
    )

    return html.Div(
            dcc.Graph(figure=fig), id='gdp_growth'
        )
    