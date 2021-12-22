import pandas as pd
from datetime import date
import datetime
from dateutil.relativedelta import relativedelta
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import numpy as np

# -- Import and clean data (importing csv into pandas)
# df = pd.read_csv("intro_bees.csv")
df_protocols = pd.read_csv('data/csv/protocol_data.csv')
df_salesforce = pd.read_csv('data/csv/salesforce.csv')

df = df_protocols.merge(df_salesforce.set_index('id'), how='left')
df['created'] = df['created'].astype('datetime64')
df['delivered'] = df['delivered'].astype('datetime64')

df.to_csv('data/csv/protocols_and_sf.csv')
# df = df.groupby(['transformed category'])[['temperature gen2', 'temperature gen1', 'magnetic gen2', 'magnetic gen1', 'thermocycler']].mean()
# df.reset_index(inplace=True)
categories = df['transformed category'].unique()

df['sf_status'] = df['sf_status'].str.lower()
df_closed = df[df['sf_status'] == 'closed']
df_delivered = df_closed[df_closed['delivered'] != '']

df_closed_on_time = None  # updated by dates upon app load

# ------------------------------------------------------------------------------
# App layout
app = Dash(__name__)

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

app.layout = html.Div([
    html.Div([
        html.H2("Protocol Data"),
        html.Img(src="/assets/opentrons-logo.png")
    ], className="banner"),

    html.Div([

        html.Div([
            dcc.DatePickerSingle(
                id='date-start',
                min_date_allowed=date(2018, 1, 1),
                max_date_allowed=date(2025, 12, 31),
                initial_visible_month=date(2021, 12, 1),
                date=date.today() - relativedelta(months=3)
            ),
            html.H6(id='output-date-start'),
            dcc.DatePickerSingle(
                id='date-end',
                min_date_allowed=date(2018, 1, 1),
                max_date_allowed=date(2025, 12, 31),
                initial_visible_month=date(2021, 12, 1),
                date=date.today()
            ),
            html.H6(id='output-date-end')
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            # dcc.Dropdown(
            #     id='category-dropdown',
            #     options=[{'label': i, 'value': i} for i in categories],
            #     value='category'
            # )
            html.H3('Category:'),
            dcc.Checklist(
                id='category-dropdown',
                options=[
                    {'label': c, 'value': c}
                    for c in categories
                ],
                value=categories,
                labelStyle={'display': 'block'}
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
        html.Button("Download CSV", id="btn-csv"),
        dcc.Download(id="download-dataframe-csv")
    ]),

    dcc.Graph(id='protocol-bar-graph'),
])


@app.callback(
    Output('output-date-start', 'children'),
    Output('output-date-end', 'children'),
    Output('protocol-bar-graph', 'figure'),
    Input('date-start', 'date'),
    Input('date-end', 'date'),
    Input('category-dropdown', 'value')
)
def update_output(date_start, date_end, categories):
    global df_closed_on_time
    df_closed_on_time = df_delivered[
        (df_delivered['delivered'] >= date_start) & (df_delivered['delivered'] <= date_end)]
    df_grouped_means = df_closed_on_time.groupby(['transformed category']).mean()
    df_grouped_means = df_grouped_means.add_suffix('_mean').reset_index()
    labware_modules_pips = ['plate_mean', 'reservoir_mean', 'total tipracks_mean', 'temperature gen2_mean', 'magnetic gen2_mean', 'thermocycler_mean']
    # data = []
    # for c in categories:
    #     if
    #
    fig = go.Figure(
        data=[
            go.Bar(name=c,
                   x=[lmp.split('_')[0] for lmp in labware_modules_pips],
                   y=[df_grouped_means[df_grouped_means['transformed category'] == c][lmp].values[0]
                      if df_grouped_means[df_grouped_means['transformed category'] == c][lmp].values.size > 0
                      else 0 for lmp in labware_modules_pips]
                   # y=[100])
                   )
            for c in categories]
    )
    date_objects = [date.fromisoformat(date_) for date_ in [date_start, date_end]]
    date_strings = [d_o_.strftime('%B %d, %Y') for d_o_ in date_objects]
    return date_strings[0], date_strings[1], fig


@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn-csv", "n_clicks"),
    prevent_initial_call=True,
)
def download(n_clicks):
    return dcc.send_data_frame(df_closed_on_time.to_csv, "mydf.csv")


if __name__ == '__main__':
    app.run_server(debug=True)
