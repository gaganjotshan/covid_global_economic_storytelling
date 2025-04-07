import dash
from dash import html
import dash_bootstrap_components as dbc
from src.components.layout import create_layout
import pandas as pd


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "COVID"

file_name = 'src/components/app_content.txt'
df = pd.read_csv('data/processed/global_dataset.csv')

app.layout = html.Div(
    children=[
        create_layout(app, file_name, df)
    ],
    style={
        'maxWidth': '1100px',
        'margin': '0 auto', 
        'padding': '30px',
        'border': '1px solid black',
        'borderRadius': '10px'
    }
)

if __name__ == '__main__':
    app.run(debug=True)