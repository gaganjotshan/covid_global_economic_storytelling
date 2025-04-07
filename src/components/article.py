from dash import Dash, dcc, html

def render(app: Dash, text: str = None) -> html.Div:
    return html.Div([dcc.Markdown(dangerously_allow_html=False, children=text)])




