import dash_table
import dash_bootstrap_components as dbc
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
df_delivered = df_delivered.iloc[: , 1:]

df_closed_on_time = pd.DataFrame()  # updated by dates upon app load

# ------------------------------------------------------------------------------
# App layout
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Div([
        html.H2("Protocol Data"),
        html.Img(src="/assets/opentrons-logo.png")
    ], className="banner"),

    html.Div([
        html.Div([
            html.H3('Date range:'),
            dcc.DatePickerRange(
                id='my-date-picker-range',
                clearable=True,
                with_portal=True,
                start_date=date.today() - relativedelta(months=3),
                min_date_allowed=date(2018, 1, 1),
                max_date_allowed=date(2025, 12, 31),
                calendar_orientation='vertical',
                initial_visible_month=date.today(),
                end_date=date.today()
            )], style={'padding-top': '50px', 'padding-left': '100px', 'width': '50%', 'float': 'left', 'display': 'inline-block'}),
        html.Div([
            html.H3('Category:'),
            dcc.Checklist(
                id='category-checklist',
                options=[
                    {'label': c, 'value': c}
                    for c in categories
                ],
                value=categories,
                labelStyle={'display': 'block'}
            )
        ], style={'padding-top': '50px', 'width': '20%', 'float': 'left', 'display': 'inline-block'}),

        html.Div([
            dbc.Button("Download CSV", size="lg", outline=True, color="primary", className="me-1", id="btn-csv"),
            dcc.Download(id="download-dataframe-csv"),
        ], style={'padding-left': '100px', 'width': '100%', 'display': 'inline-block'})
    ]),
    html.Div([dcc.Graph(id='protocol-bar-graph', className='row')], style={'padding': '20px'}),
    html.Div([
        dash_table.DataTable(
            id="protocol-table",
            data=df_delivered.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df_delivered.columns],
            style_table={
                'overflowX': 'scroll',
                'maxHeight': '50ex',
                'overflowY': 'scroll',
                'width': '100%',
                'minWidth': '100%',
            },
            fixed_columns={'headers': True, 'data': 1},
            fill_width=True,
            style_data={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
            style_cell={
                'height': 'auto',
                # all three widths are needed
                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'whiteSpace': 'normal'
            }

        ),
    ], style={'padding-left': '100px'})
])


@app.callback(
    Output('protocol-bar-graph', 'figure'),
    Output('protocol-table', 'data'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('category-checklist', 'value')
)
def update_output(date_start, date_end, categories):
    global df_closed_on_time
    if date_start > date_end:
        raise Exception('Invalid date range selection.')

    df_closed_on_time = df_delivered[
        (df_delivered['delivered'] >= date_start) & (df_delivered['delivered'] <= date_end)]
    df_grouped_means = df_closed_on_time.groupby(['transformed category']).mean()
    df_grouped_means = df_grouped_means.add_suffix('_mean').reset_index()
    labware_modules_pips = ['plate_mean', 'reservoir_mean', 'total tipracks_mean', 'temperature gen2_mean', 'magnetic gen2_mean', 'thermocycler_mean']
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
    return fig, df_closed_on_time.to_dict('records')


@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn-csv", "n_clicks"),
    prevent_initial_call=True,
)
def download(n_clicks):
    today_str = date.today().strftime('%m%d%Y')
    return dcc.send_data_frame(df_closed_on_time.to_csv, f"report{today_str}.csv")


if __name__ == '__main__':
    app.run_server(debug=True)
