import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Crear la aplicación Dash
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Leer los datos
df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')
df['Month'] = pd.to_datetime(df['Date']).dt.month_name() # Nombres de los meses
df['Year'] = pd.to_datetime(df['Date']).dt.year

# Definir el layout de la aplicación
app.layout = html.Div(children=[
    html.H1('Australia Wildfire Dashboard', style={
        'textAlign': 'center', 
        'color': '#503D36',
        'font-size': '36px', 
        'font-family': 'Arial, sans-serif',
        'margin-bottom': '30px'
    }),
    html.Div([
        html.Div([
            html.H2('Select Region:', style={
                'margin-right': '2em',
                'font-family': 'Arial, sans-serif'
            }),
            dcc.RadioItems(
                options=[
                    {"label": "New South Wales", "value": "NSW"},
                    {"label": "Northern Territory", "value": "NT"},
                    {"label": "Queensland", "value": "QL"},
                    {"label": "South Australia", "value": "SA"},
                    {"label": "Tasmania", "value": "TA"},
                    {"label": "Victoria", "value": "VI"},
                    {"label": "Western Australia", "value": "WA"}
                ],
                value="NSW", 
                id='region', 
                inline=True,
                style={'font-family': 'Arial, sans-serif'}
            )
        ], style={'padding': '10px', 'border': '1px solid #ddd', 'border-radius': '5px', 'margin-bottom': '20px'}),
        html.Div([
            html.H2('Select Year:', style={
                'margin-right': '2em',
                'font-family': 'Arial, sans-serif'
            }),
            dcc.Dropdown(
                options=[{'label': str(year), 'value': year} for year in df.Year.unique()],
                value=2005,
                id='year',
                style={'font-family': 'Arial, sans-serif'}
            )
        ], style={'padding': '10px', 'border': '1px solid #ddd', 'border-radius': '5px', 'margin-bottom': '20px'}),
        html.Div([
            html.Div([], id='plot1', style={'width': '50%', 'padding': '10px'}),
            html.Div([], id='plot2', style={'width': '50%', 'padding': '10px'})
        ], style={'display': 'flex'}),
    ], style={'width': '90%', 'margin': '0 auto'})
])

# Definir el callback para actualizar los gráficos
@app.callback(
    [Output(component_id='plot1', component_property='children'),
     Output(component_id='plot2', component_property='children')],
    [Input(component_id='region', component_property='value'),
     Input(component_id='year', component_property='value')]
)
def update_graphs(selected_region, selected_year):
    region_data = df[df['Region'] == selected_region]
    year_region_data = region_data[region_data['Year'] == selected_year]
    
    # Gráfico 1: Promedio mensual del área estimada de incendios
    avg_fire_area = year_region_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(avg_fire_area, values='Estimated_fire_area', names='Month', 
                  title=f"{selected_region} : Monthly Average Estimated Fire Area in {selected_year}")

    # Gráfico 2: Promedio mensual de píxeles de incendios vegetales presuntos
    avg_veg_fire = year_region_data.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(avg_veg_fire, x='Month', y='Count', 
                  title=f"{selected_region} : Average Count of Pixels for Presumed Vegetation Fires in {selected_year}")
    
    return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)]

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server()
