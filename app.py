import dash
import dash_bootstrap_components as dbc
import pandas as pd
import random
import uvicorn

from dash import dcc, html, Input, Output, State
from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware

from app_ui import app_layout

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title='Cat Consulting'
)
server = app.server
fastapi_server = FastAPI()
fastapi_server.mount("/", WSGIMiddleware(server))

app.layout = app_layout


@app.callback(
    [Output('all_trainings_table', 'data'),
     Output('total_stats_div', 'children'),
     Output('client_name_dropdown', 'options'),
     Output('client_name_div', 'className'),
     Output('problem_title_div', 'className'),
     Output('finish_training_warning_div', 'children'),
     Output('client_name_input', 'value'),
     Output('problem_title_input', 'value'),],
    [Input('start_training_button', 'n_clicks'),
     Input('finish_training_button', 'n_clicks')],
    [State('finish_training_id_input', 'value'),
     State('client_name_input', 'value'),
     State('problem_title_input', 'value'),
     State('costs_slider', 'value'),
     State('revenue_slider', 'value'),
     State('all_trainings_table', 'data'),
     State('total_stats_div', 'children'),
     State('client_name_dropdown', 'options'),
     State('finish_training_warning_div', 'children')],
    prevent_initial_call=True
)
def all_trainings_table(
    n_clicks_start, n_clicks_finish, training_to_finish_id, 
    name, problem, costs, revenue, trainings_data, 
    total_stats, client_name_options, finish_warning
):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if changed_id == 'start_training_button.n_clicks':
        name_color_class = 'black-text-color' if name else 'red-text-color'
        problem_color_class = 'black-text-color' if problem else 'red-text-color'
        if not (name and problem):
            return (
                trainings_data, total_stats, client_name_options, 
                name_color_class, problem_color_class, 
                finish_warning, name, problem
            )
        training_id = len(trainings_data)
        training = {
            "id": training_id,
            "client": name,
            "problem": problem,
            "cost of training": costs,
            "expected revenue": revenue,
            "received revenue": 0,
            "completed": False,
            "success": False
        }
        trainings_data.append(training)
    if changed_id == 'finish_training_button.n_clicks':
        name_color_class = 'black-text-color'
        problem_color_class = 'black-text-color'
        if training_to_finish_id + 1 > len(trainings_data):
            finish_warning = f"Training {training_to_finish_id} not found"
            return (
                trainings_data, total_stats, client_name_options, 
                name_color_class, problem_color_class, 
                finish_warning, name, problem
            )
        completed_bool = trainings_data[training_to_finish_id]["completed"]
        if completed_bool:
            finish_warning = f"Training {training_to_finish_id} has already been completed"
            return (
                trainings_data, total_stats, client_name_options,
                name_color_class, problem_color_class, 
                finish_warning, name, problem
            )            
        finish_warning = ""
        trainings_data[training_to_finish_id]["completed"] = True
        success_bool = random.randint(1, 10) > 1
        if success_bool:
            received_revenue = trainings_data[training_to_finish_id]["expected revenue"]
            trainings_data[training_to_finish_id]["received revenue"] = received_revenue
            trainings_data[training_to_finish_id]["success"] = True
    trainings_df = pd.DataFrame(trainings_data)
    if len(trainings_df) == 0:
        received_revenue = 0
        total_revenue = 0
        completed_trainings = 0
        education_costs = 0
    else:
        completed_trainings = trainings_df["completed"].sum()
        education_costs = trainings_df["cost of training"].sum()
        received_revenue = trainings_df["received revenue"].sum()
        total_revenue = received_revenue - education_costs
    total_stats = html.Ul(
        children=[
            html.Li(f"Trainings requested: {len(trainings_df)}"),
            html.Li(f"Trainings completed: {completed_trainings}"),
            html.Li(f"Education costs: {education_costs} meowcoins"),
            html.Li(f"Revenue from clients: {received_revenue} meowcoins"),
            html.Li(f"Total revenue: {total_revenue} meowcoins", className="total-revenue")
        ],
        className="overall-stats-list"
    )
    client_name_options = [
        {'label': val, 'value': val} for val in trainings_df["client"].unique()
    ]
    return (
        trainings_data, total_stats, client_name_options,
        name_color_class, problem_color_class, 
        finish_warning, "", ""
    )


@app.callback(
    [Output('client_info_div', 'children'),
     Output('client_info_div', 'hidden')],
    [Input('client_info_button', 'n_clicks')],
    [State('all_trainings_table', 'data'),
     State('client_name_dropdown', 'value')]
)
def get_client_info(n_clicks, trainings_data, name):
    if not name:
        return [], True
    trainings_df = pd.DataFrame(trainings_data)
    if len(trainings_df) == 0:
        return [], True
    trainings_df = trainings_df.loc[trainings_df["client"] == name]
    completed_trainings = trainings_df["completed"].sum()
    education_costs = trainings_df["cost of training"].sum()
    received_revenue = trainings_df["received revenue"].sum()
    total_revenue = received_revenue - education_costs
    client_stats = html.Ul(
        children=[
            html.Li(f"Trainings requested: {len(trainings_df)}"),
            html.Li(f"Trainings completed: {completed_trainings}"),
            html.Li(f"Education costs: {education_costs} meowcoins"),
            html.Li(f"Revenue from clients: {received_revenue} meowcoins"),
            html.Li(f"Total revenue: {total_revenue} meowcoins", className="total-revenue")
        ],
        className="overall-stats-list"
    )
    return client_stats, False


if __name__ == "__main__":
    uvicorn.run("app:fastapi_server", host="127.0.0.1", port=8000, reload=True)
    # app.run_server(debug=True, host="127.0.0.1", port=8000)
