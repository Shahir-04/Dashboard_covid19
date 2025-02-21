import pandas as pd
import numpy as numpy
import dash
import plotly.graph_objects as go
import plotly.express as px
from dash import html,dcc
from dash.dependencies import Input,Output
# using bootstrap for css
# In Bootstrap the whole page is divide into 12 columns(parts)
external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': "stylesheet",
        'Integrity': 'shals4-08/SFPGESFIT300ngsV7Z2701uXPkF0wHERkLPO',
        'crossorigin': 'anonymous'
    }
]
# importing data
df=pd.read_csv('C:/Users/shahi/OneDrive/Desktop/pyhton/campus x/Dashboard_covid19/IndividualDetails.csv')
# cards
total_case=df.shape[0]
recovered=df[df['current_status']=='Recovered'].shape[0]
deceased=df[df['current_status']=='Deceased'].shape[0]
active=df[df['current_status']=='Hospitalized'].shape[0]
# Options for dropdown
option=[
    {'label':'All','value':'All'},
    {'label':'Recovered','value':'Recovered'},
    {'label':'Death','value':'Deceased'},
    {'label':'Hospitalized','value':'Hospitalized'}
]
# ploting graph
ndf=df['detected_state'].value_counts().reset_index()

# Cleaning Data and grouping Age
nndf=pd.read_csv('C:/Users/shahi/OneDrive/Desktop/pyhton/campus x/Dashboard_covid19/IndividualDetails.csv')
nndf.dropna(subset=['age'],inplace=True)
nndf['age']=pd.to_numeric(nndf['age'],errors='coerce')
# creating bins
nndf['grouped_age']=pd.cut(nndf['age'],bins=[0,20,40,60,80,100],labels=['0-20','21-40','41-60','61-80','81-100'])
p=nndf['grouped_age'].value_counts().reset_index()

# Creating Pie Chart
fig=px.pie(p,
    names='grouped_age',
    values='count',
    title='Age Distribution in Pie Chart',
    hover_name='grouped_age')

# Creating Line Chart
q=df['diagnosed_date'].value_counts().sort_values(ascending=True).reset_index()
q.columns=['Date','Covid Cases']
fig1=px.line(q,x='Date',y='Covid Cases',title='Day by Day Analysis',hover_name='Covid Cases')

# Creating Dashboard
app=dash.Dash(__name__,external_stylesheets=external_stylesheets)
app.layout=html.Div([
    html.Br(),
    html.H1('Covid-19 Dashboard',style={'color':'white','text-align':'center'}),
    html.Br(),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Total Case'),
                    html.H4(total_case)
                ],className='card-body')
            ],className='card bg-danger')
        ],className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Active'),
                    html.H4(active)
                ],className='card-body')
            ],className='card bg-info')
        ],className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Recovered'),
                    html.H4(recovered)
                ],className='card-body')
            ],className='card bg-warning')
        ],className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Death'),
                    html.H4(deceased+2)
                ],className='card-body')
            ],className='card bg-success')
        ],className='col-md-3'),
    ],className='row'),
    html.Div([
        html.Br()
    ],className='row'),
    html.Div([
        html.Div([
            dcc.Graph(id='line',figure=fig1)
        ],className='col-md-7'),
        html.Div([
            dcc.Graph(id='group_age',figure=fig)
        ],className='col-md-5')
    ],className='row'),
    html.Div([
        html.Br()
    ],className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='select',options=option,value='All'),
                    dcc.Graph(id='bar')
                ],className='card-body')
            ],className='card')
        ],className='col-md-12')
    ],className='row')
],className='container')

@app.callback(Output('bar','figure'),[Input('select','value')])
def plot(option):
    if option=='All':
        return {'data':[go.Bar(x=ndf['detected_state'],y=ndf['count'])],
                'layout':go.Layout(title='Covid Cases in each State')}
    else:
        a=df[df['current_status']==option]
        a=a['detected_city'].value_counts().reset_index()
        return{'data':[go.Bar(x=a['detected_city'],y=a['count'])],
                'layout':go.Layout(title='Covid cases in each State',xaxis_title='City',yaxis_title='Cases')} 
        

if(__name__=='__main__'):
    app.run_server(debug=True)