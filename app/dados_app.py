import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np
import dash_table

table_data = []

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap'])

app.layout = dbc.Container([
    html.H1("Laboratorio de probabilidad y estadística", style={"font-weight": "bold", "font-family": "'Roboto', sans-serif","margin-top": "20px"}),
    html.H6("Centro de Investigación Estadística ERGOSTATS", style={"color": "gray", "font-size": "smaller"}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.P("Vamos a aprender sobre variables aleatoria con algunos experimentos sencillos. En este caso, vamos a lanzar dos dados y sumar los resultados. ¿Qué crees que va a pasar? ¿Cuál crees que es la suma más probable? ¿Cuál crees que es el valor medio?"),
                     dbc.Row([
                        html.Label("Lanzar dados"),
                        dbc.Button("Lanzar dados", id="btn", color="primary", className="mr-2")
                    ], style={"margin-top": "10px", "margin-bottom": "10px"}),
                    dbc.Row([
                        html.Label("Paso:"),
                        dcc.Input(id="input-m", type="number", value=1)
                    ], style={"margin-top": "10px", "margin-bottom": "10px"}),
                    dbc.Row([
                        html.Label("Reiniciar contador"),
                        dbc.Button("Reiniciar contador", id="btn-reset", color="danger", className="mr-2")
                    ], style={"margin-top": "10px", "margin-bottom": "10px"})
                ])
            ], className="mb-3")
        ], width=3),
        dbc.Col([
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    dash_table.DataTable(
                        id="table",
                        columns=[
                            {"name": "ID", "id": "ID"},
                            {"name": "Dado 1", "id": "Dado 1"},
                            {"name": "Dado 2", "id": "Dado 2"},
                            {"name": "Total", "id": "Total"}
                        ],
                        data=table_data,
                        page_size=10,
                        style_table={"overflowX": "auto"},
                        sort_action="native",
                        sort_mode="single",
                        sort_by=[{"column_id": "ID", "direction": "desc"}]
                    ),
                ], width=4),
                dbc.Col([
                    dcc.Graph(id="graph"),
                ], width=7)
            ])
        ], width=9)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                html.H3("Permutaciones", style={"color": "gray", "font-size": "smaller"}),
                html.P(["En las permutaciones ", html.Strong("importa el orden de ocurrencia")])
            ]),
            
            dbc.Row([
        dash_table.DataTable(
                        id="table-group",
                        columns=[
                            {"name": "ID", "id": "index"}, 
                            {"name": "Permutación", "id": "Permutación"},
                            {"name": "Suma", "id": "Total"},
                            {"name": "Frecuencia", "id": "Frecuencia"}
                        ],
                        data=table_data,
                        page_size=12,
                        style_table={"overflowX": "auto"},
                        sort_action="native",
                        sort_mode="single",
                        sort_by=[{"column_id": "ID", "direction": "desc"}]
                    ),
                    ])
                ], width=3),
                dbc.Col(width=1),
                dbc.Col([

                    dbc.Row([
                html.H3("Combinaciones", style={"color": "gray", "font-size": "smaller"}),
                html.P(["En las combinaciones ", html.Strong("no importa el orden de ocurrencia")])
                ]),
                dbc.Row([
                dash_table.DataTable(
                        id="table-group-3",
                        columns=[
                            {"name": "ID", "id": "index"}, 
                            {"name": "Combinación", "id": "Combinación"},
                            {"name": "Suma", "id": "Total"},
                            {"name": "Frecuencia", "id": "Frecuencia"}
                        ],
                        data=table_data,
                        page_size=12,
                        style_table={"overflowX": "auto"},
                        sort_action="native",
                        sort_mode="single",
                        sort_by=[{"column_id": "ID", "direction": "desc"}]
                    )
            ]),
                ], width=3),
                dbc.Col(width=1),
                dbc.Col([
                    dbc.Row([
                    html.H3("Sumas", style={"color": "gray", "font-size": "smaller"}),
                html.P(["Mira como distintas combinaciones o permutaciones ", html.Strong("llevan a la misma suma. Ojo con el caso que vas a analizar.")])
                ]),
                    dbc.Row([
                    dash_table.DataTable(
                        id="table-group-2",
                        columns=[
                            {"name": "ID", "id": "index"}, 
                            {"name": "Suma", "id": "Total"},
                            {"name": "Frecuencia", "id": "Frecuencia"}
                        ],
                        data=table_data,
                        page_size=12,
                        style_table={"overflowX": "auto"},
                        sort_action="native",
                        sort_mode="single", 
                        sort_by=[{"column_id": "ID", "direction": "desc"}]
                    )]),
                ], width=3)
                
                
    ])
])

@app.callback(
    [Output("table-group-3", "data"),Output("table-group-2", "data"),Output("table-group", "data"),Output("table", "data"), Output("graph", "figure")],
    [Input("btn", "n_clicks"), Input("btn-reset", "n_clicks")],
    [State("input-m", "value")]
)

def update_output(n, n_reset, m):
    global table_data  # Usar la variable global table_data

    ctx = dash.callback_context
    if not ctx.triggered:
        return table_data, px.bar()
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "btn-reset" and n_reset:
        # Si se ha pulsado el botón de reinicio, borrar los datos de la tabla y actualizar el gráfico
        table_data = []
        return table_data, px.bar()

    if button_id == "btn" and n:
        for _ in range(m):  # Realizar m lanzamientos adicionales
            dice1 = np.random.randint(1, 7)
            dice2 = np.random.randint(1, 7)
            total = dice1 + dice2

            new_row = {
                "ID": len(table_data) + 1,
                "Dado 1": dice1,
                "Dado 2": dice2,
                "Total": total
            }

            table_data.append(new_row)

        # Crear DataFrame con todas las sumas en table_data
        df = pd.DataFrame(table_data)
        df.sort_values("ID", ascending=True, inplace=True)

        # Segunda tabla:
        df["Permutación"] = df["Dado 1"].astype(str) + " + " + df["Dado 2"].astype(str)

        g_table_2 = df.groupby("Total").size().reset_index(name = "Frecuencia")

        g_table = df.groupby(["Total","Permutación"]).size().reset_index(name = "Frecuencia")

        # Segunda tabla:
        df["Combinación"] = df.apply(lambda row: ' + '.join(sorted([str(row["Dado 1"]), str(row["Dado 2"])])), axis=1)

        g_table_3 = df.groupby(["Total","Combinación"]).size().reset_index(name='Frecuencia')

        g_table = g_table.reset_index()
        g_table_2 = g_table_2.reset_index()
        g_table_3 = g_table_3.reset_index()

                # Sumar 1 al índice
        g_table['index'] = g_table['index'] + 1

        # Haz lo mismo para las otras tablas
        g_table_2 = g_table_2.reset_index()
        g_table_2['index'] = g_table_2['index'] + 1

        g_table_3 = g_table_3.reset_index()
        g_table_3['index'] = g_table_3['index'] + 1
        

        fig = px.histogram(df, x="Total", nbins=11, range_x=[2, 12],
                           title=f"Histograma de la suma de dos dados ({len(table_data)} lanzamientos)",
                           labels={"Total": "Suma", "count": "Frecuencia"})
        
        fig.update_yaxes(title="Frecuencia")

        mean = df["Total"].mean()
        std = df["Total"].std()

        fig.add_shape(type = "line", x0 = mean, x1 = mean, y0 = 0,y1 = 1, yref = "paper", line = dict(color = "red", width = 2, dash = "dash"))

               
        fig.add_annotation(x=mean, y=0.95, yref='paper', showarrow=False,
                       text=f'Media: {mean:.2f}<br>Desviación estándar: {std:.2f}',
                       bgcolor='white', bordercolor='rgba(255, 255, 255, 0)',  opacity=0.8,borderpad=10)
        
        
               
        return g_table_3.to_dict('records', index=True), g_table_2.to_dict('records', index=True), g_table.to_dict('records', index=True), table_data, fig

    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update


if __name__ == "__main__":
    app.run_server(debug=True)