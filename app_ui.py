import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

app_layout = html.Div([
    html.Div(
        children=[
            html.H4("Puss in Boots Consulting", className="logo-title")
        ],
        className="header-row margin-bottom-10"
    ),
    dbc.Row([
        dbc.Col([
            dbc.Stack([
                html.Div(
                    "Enter the client's name",
                    id="client_name_div",
                    className="black-text-color"
                ),
                dcc.Input(
                    id="client_name_input",
                    type="text",
                    className="margin-bottom-10"
                ),
                html.Div(
                    "Enter the problem title",
                    id="problem_title_div",
                    className="black-text-color"
                ),
                dcc.Input(
                    id="problem_title_input",
                    type="text",
                    className="margin-bottom-10"
                ),
                html.Div("Estimate education costs"),
                dcc.Slider(
                    id="costs_slider",
                    min=20,
                    max=30,
                    step=1,
                    value=20,
                    marks={
                        20: '20',
                        22: '22',
                        24: '24',
                        26: '26',
                        28: '28',
                        30: '30'
                    }
                ),
                html.Div("Estimate expected revenue"),
                dcc.Slider(
                    id="revenue_slider",
                    min=40,
                    max=50,
                    step=1,
                    value=40,
                    marks={
                        40: '40',
                        42: '42',
                        44: '44',
                        46: '46',
                        48: '48',
                        50: '50'
                    }
                ),
                dbc.Button(
                    "Start training",
                    id="start_training_button",
                    n_clicks=0,
                    size="md",
                    class_name="start-training-button"
                ),
            ], className="submit-request-form"),
            html.Hr(className="margin-left-10"),
            html.Img(
                src='assets/images/puss_in_boots.png',
                className="cat-image"
            )
        ], width=2),
        dbc.Col([
            dbc.Stack([
                html.H5(
                    "All trainings",
                    className="text-align-center"
                ),
                html.Div(
                    id="all_trainings_table_div",
                    className="all-trainings-table",
                    children=[
                        html.Div("Enter id of the training to finish"),
                        dbc.Stack([
                            dcc.Input(
                                id="finish_training_id_input",
                                type="number",
                                min=0,
                                value=0,
                                className="input-number"
                            ),
                            dbc.Button(
                                "Finish training",
                                id="finish_training_button",
                                n_clicks=0,
                                size="md",
                                class_name="start-training-button"
                            ),
                            html.Div(
                                children="",
                                id="finish_training_warning_div",
                                className="red-text-color margin-left-10"
                            )
                        ], direction="horizontal"),
                        dash.dash_table.DataTable(
                            id="all_trainings_table",
                            columns=[
                                {'name': 'id', 'id': 'id'},
                                {'name': 'client', 'id': 'client'},
                                {'name': 'problem', 'id': 'problem'},
                                {'name': 'cost of training', 'id': 'cost of training'},
                                {'name': 'expected revenue', 'id': 'expected revenue'},
                                {'name': 'received revenue', 'id': 'received revenue'},
                                {'name': 'completed', 'id': 'completed'},
                                {'name': 'success', 'id': 'success'}
                            ],
                            data=[],
                            page_size=10,
                            style_cell={
                                'fontSize': '12px', 'max-width': '130px', 'textAlign': 'center'
                            },
                            style_header={
                                'color': 'black', 'fontWeight': 'bold'
                            },
                            cell_selectable=False,
                            filter_action='native',
                            sort_action='native'
                        )
                    ]
                )
            ])
        ], className="border-left"),
        dbc.Col([
            dbc.Stack([
                html.H5("Overall statistics", className="text-align-center"),
                html.Div(
                    html.Ul(
                        children=[
                            html.Li("Trainings requested: 0"),
                            html.Li("Trainings completed: 0"),
                            html.Li("Education costs: 0 meowcoins"),
                            html.Li("Revenue from clients: 0 meowcoins"),
                            html.Li("Total revenue: 0 meowcoins", className="total-revenue")
                        ],
                        className="overall-stats-list"
                    ),
                    id="total_stats_div", 
                    className="text-align-center"
                ),
                html.Div(
                    id="total_revenue_div",
                ),
                html.Hr(),
                html.H5("Clients information", className="text-align-center"),
                dbc.Stack([
                    dcc.Dropdown(
                        id="client_name_dropdown",
                        className="margin-right-10 dashboard-dropdown",
                        value=None,
                        multi=False,
                        options=[],
                        placeholder="Select the client"
                    ),
                    dbc.Button(
                        "Show details",
                        id="client_info_button",
                        n_clicks=0,
                        size="md",
                        class_name="start-training-button"
                    )
                ], direction="horizontal", className="margin-auto"),
                html.Div(
                    id="client_info_div",
                    hidden=True,
                    className="text-align-center"
                )
            ])             
        ], width=3, className="border-left")
    ])
])
