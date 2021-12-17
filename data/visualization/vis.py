import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

app = Dash(__name__)

# -- Import and clean data (importing csv into pandas)
# df = pd.read_csv("intro_bees.csv")
df = pd.read_csv('data/csv/protocol_data.csv')

df = df.groupby(['transformed category'])[['temperature gen2', 'temperature gen1', 'magnetic gen2', 'magnetic gen1', 'thermocycler']].mean()
df.reset_index(inplace=True)
categories = df['transformed category'].unique()
print(df[:5])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Protocol Data by Category", style={'text-align': 'center'}),

    dcc.Dropdown(id="category",
                 options=[{"label": c, "value": c} for c in categories],
                 multi=False,
                 value=categories[0],
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='protocol_data', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output("protocol_data", "figure"),
    [Input("category", "value")])
def update_bar_chart(category):
    mask = df["transformed category"] == category
    fig = px.bar(df[mask], x="transformed category", y="thermocycler",
                 barmode="group")
    fig.update_traces(marker_line_width=0.5)
    return fig

# Nick 12/17
# grouped bar chart w plotly, percentages, date range inputs


if __name__ == '__main__':
    app.run_server(debug=True)
