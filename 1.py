import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

app = Dash(__name__)

colorscales = px.colors.named_colorscales()
#df = pd.read_csv("D:/College/4Semester/DS250/3b/co2.csv")
df = pd.read_csv("co2.csv")
df = df[['Year','Country','Total']]
timedf = df['Year'].unique()
timeline = []
for r in range(len(timedf)):
    time = timedf[r]
    r = {}
    r["label"] = str(time)
    r["value"] = int(time)
    timeline.append(r)
# App layout
app.layout = html.Div([

    html.H1("World CO2 dashboard using Dash", style={'text-align': 'center'}),
    
    dcc.Dropdown(id="slct_year",
                #  options=[
                #      {"label": "1872", "value": 1872},
                #      {"label": "1971", "value": 1971},
                #      {"label": "2000", "value": 2000},
                #      {"label": "2014", "value": 2014}],
                options = timeline,
                 multi=False,
                 value=2014,
                 style={'width': "40%"}
                 ),
    dcc.Dropdown(
        id='dropdown', 
        options=colorscales,
        value='viridis',
        style={'width': "40%"}
    ),
    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_co2_map', figure={})

])

# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_co2_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')],
    [Input(component_id='dropdown', component_property='value')]
)
def update_graph(option_slctd,dropdown):
    # print(option_slctd)
    # print(type(option_slctd))
    
    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]
    #dff = dff[dff["Affected by"] == "Varroa_mites"]
    # print(dff.head())
    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='country names',
        locations='Country',
        scope="world",
        color='Total',
        hover_data=['Country', 'Total'],
        color_continuous_scale=dropdown,
        labels={'Total co2 by country'},
        #template='plotly_dark'
    )
    fig.update_layout(height=370, margin={"r":0,"t":0,"l":0,"b":0})
    return container, fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)