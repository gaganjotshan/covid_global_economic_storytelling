from dash import Dash, html, dash_table
import re
import pandas as pd

from src.components import (
    article,
    gdp_graph,
    merch_trade_graph,
    world_refugiee_graph,
    highest_refugiee_growths
)

GRAPHS = {
    'name=gdp_graph': gdp_graph,
    'name=merch_trade_graph': merch_trade_graph,
    'name=world_refugiee_graph': world_refugiee_graph,
    'name=highest_refugiee_growths': highest_refugiee_growths
}

def parse_content(text):
    components = []
    for bloc in text.split("\#"):
        if match := re.match(r'(\w+)\{(.*?)\}', bloc.strip(), re.DOTALL):
            components.append({
                'type': match.group(1),  
                'data': match.group(2)
            })
    return components

def get_html_content(app: Dash, file_name: str, dataset: pd.DataFrame):
    with open(file_name, 'r') as f:
        components = parse_content(''.join(f.readlines()))

    graphs = {'name=gdp_graph': gdp_graph}

    html_components = []
    for comp in components:
        if comp['type'] == 'line':
            html_components.append(html.Hr())
        if comp['type'] == 'space':
            html_components.append(html.Br())
        if comp['type'] == 'markdown':
            html_components.append(article.render(app, text=comp['data']))
        if comp['type'] == 'graph':
            html_components.append(GRAPHS[comp['data']].render(app, dataset))
            
    return html_components



def create_layout(app: Dash, file_name: str, dataset: pd.DataFrame) -> html.Div:

    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title, style={'textAlign': 'center'}),
            html.Hr(),
            html.Div(
                className="article",
                children=get_html_content(app, file_name, dataset),
            ),
        ],
    )