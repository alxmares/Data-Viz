import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Lista de años para el menú desplegable de selección de año
year_list = [i for i in range(1980, 2024)]
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv")

# Definir el layout de la aplicación
app.layout = html.Div(children=[
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': '24px'
        }
    ),
    dcc.Dropdown(
        id='dropdown-statistics',
        options=[
            {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
            {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
        ],
        placeholder='Select a report type',
        value='Select Statistics',
        style={
            'width': '80%',
            'padding': '3px',
            'font-size': '20px',
            'text-align-last': 'center'
        }
    ),
    dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in year_list],
        placeholder='Select-year',
        value='Select-year',
        style={
            'width': '80%',
            'padding': '3px',
            'font-size': '20px',
            'text-align-last': 'center'
        }
    ),
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flex-wrap': 'wrap'})
    ])
])

@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistic):
    if selected_statistic == 'Yearly Statistics':
        return False
    else:
        return True

@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), 
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistic, selected_year):
    if selected_statistic == 'Recession Period Statistics':
        # Filtrar los datos para los períodos de recesión
        recession_data = df[df['Recession'] == 1]
        
        # Plot 1: Gráfico de líneas para las ventas de automóviles durante el período de recesión (año a año)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Automobile Sales Fluctuate over Recession Period")
        )
        
        # Plot 2: Gráfico de barras para el número promedio de vehículos vendidos por tipo de vehículo
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average Number of Vehicles Sold by Vehicle Type")
        )
        
        # Plot 3: Gráfico de pastel para la participación en el gasto total por tipo de vehículo durante las recesiones
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title="Total Expenditure Share by Vehicle Type during Recessions")
        )
        
        # Plot 4: Gráfico de barras para el efecto de la tasa de desempleo en el tipo de vehículo y las ventas
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data,
                x='unemployment_rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                title='Effect of Unemployment Rate on Vehicle Type and Sales')
        )
        
        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart4)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3)], style={'display': 'flex'})
        ]

    elif selected_statistic == 'Yearly Statistics':
        # Filtrar los datos para el año seleccionado
        yearly_data = df[df['Year'] == selected_year]
        
        # Plot 1: Gráfico de líneas para las ventas de automóviles anuales
        yas = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas, 
                x='Year',
                y='Automobile_Sales',
                title='Yearly Automobile Sales')
        )
        
        # Plot 2: Gráfico de líneas para las ventas mensuales de automóviles
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas,
                x='Month',
                y='Automobile_Sales',
                title='Total Monthly Automobile Sales')
        )
        
        # Plot 3: Gráfico de barras para el número promedio de vehículos vendidos durante el año dado
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title=f'Average Vehicles Sold by Vehicle Type in the year {selected_year}')
        )
        
        # Plot 4: Gráfico de pastel para el gasto total en publicidad por tipo de vehículo
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data, 
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Advertisement Expenditure for Each Vehicle')
        )
        
        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart4)], style={'display': 'flex'})
        ]

    return []


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server()