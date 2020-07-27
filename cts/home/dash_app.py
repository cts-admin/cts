import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from django_plotly_dash import DjangoDash

app_name = "DPD demo application"

dashboard_name1 = 'dash_example_1'
dash_example1 = DjangoDash(name=dashboard_name1,
                           serve_locally=True,
                           app_name=app_name
                           )

mapbox_access_token = "pk.eyJ1IjoiY3RzYWRtaW4iLCJhIjoiY2ppZHBrMzliMDE4MDNxbXc3dHdxZTZoNyJ9.POFtqsXHCxfk9yR1jpcWNQ"


def get_accession_data():
    import django
    django.setup()
    from plant_database.models import Accession
    df = pd.DataFrame(list(Accession.objects.all().values()))
    df['lat'] = df['location'][0].y
    df['lon'] = df['location'][0].x
    return df


df = get_accession_data()
fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="plant_total",
                        hover_data=["percent_fruiting", "percent_flowering"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
    ])
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

table = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns)[7:10],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df.plant_total, df.sample_size, df.percent_flowering],
               fill_color='lavender',
               align='left'))
])
table.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

dash_example1.layout = html.Div(id='main',
                                children=[
                                    html.Div([dcc.Dropdown(id='my-dropdown1',
                                                           options=[{'label': 'New York City', 'value': 'NYC'},
                                                                    {'label': 'Montreal', 'value': 'MTL'},
                                                                    {'label': 'San Francisco', 'value': 'SF'}
                                                                    ],
                                                           value='NYC',
                                                           className='col-md-12',
                                                           ),
                                              html.Div(id='test-output-div')
                                              ]),
                                    dcc.Dropdown(
                                        id='my-dropdown2',
                                        options=[
                                            {'label': 'Oranges', 'value': 'Oranges'},
                                            {'label': 'Plums', 'value': 'Plums'},
                                            {'label': 'Peaches', 'value': 'Peaches'}
                                        ],
                                        value='Oranges',
                                        className='col-md-12',
                                    ),

                                    html.Div(id='test-output-div2'),

                                    html.Div(
                                        [
                                            dcc.Graph(figure=fig)
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            dcc.Graph(figure=table)
                                        ]
                                    )

                                ])


@dash_example1.expanded_callback(
    dash.dependencies.Output('test-output-div', 'children'),
    [dash.dependencies.Input('my-dropdown1', 'value')])
def callback_test(*args, **kwargs):  # pylint: disable=unused-argument
    'Callback to generate test data on each change of the dropdown'

    # Creating a random Graph from a Plotly example:
    N = 500
    random_x = np.linspace(0, 1, N)
    random_y = np.random.randn(N)

    # Create a trace
    trace = go.Scatter(x=random_x,
                       y=random_y)

    data = [trace]

    layout = dict(title='',
                  yaxis=dict(zeroline=False, title='Total Expense (£)', ),
                  xaxis=dict(zeroline=False, title='Date', tickangle=0),
                  margin=dict(t=20, b=50, l=50, r=40),
                  height=350,
                  )

    fig = dict(data=data, layout=layout)
    line_graph = dcc.Graph(id='line-area-graph2', figure=fig, style={'display': 'inline-block', 'width': '100%',
                                                                     'height': '100%;'})
    children = [line_graph]

    return children


@dash_example1.expanded_callback(
    dash.dependencies.Output('test-output-div2', 'children'),
    [dash.dependencies.Input('my-dropdown2', 'value')])
def callback_test2(*args, **kwargs):
    'Callback to exercise session functionality'

    print(args)
    print(kwargs)

    children = [html.Div(["You have selected %s." % (args[0])]),
                html.Div(["The session context message is '%s'" % (kwargs['session_state']['django_to_dash_context'])])]

    return children
