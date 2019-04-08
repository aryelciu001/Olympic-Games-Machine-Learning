import dash
import dash_html_components as html
import dash_core_components as dcc
import prediction
import data

app = dash.Dash(__name__)

app.layout = html.Div(children = [
    html.Div(children = [
        html.H1(children='How Physically Prepared Are You for The Olympic?', id='app2-title'),
        html.Div(children = [
            html.H5(children='Height'),
            html.Div(dcc.Input(id='input-box-height', type='text')),
            html.H5(children='Weight'),
            html.Div(dcc.Input(id='input-box-weight', type='text')),
            html.H5(children='Age'),
            html.Div(dcc.Input(id='input-box-age', type='text')),
            html.H5(children='Sport'),
            dcc.Dropdown(
            id='my-dropdown',
            options=[
                {'label': 'Swimming', 'value': 'swimming'},
                {'label': 'Athletics', 'value': 'athletics'},
                {'label': 'Gymnastics', 'value': 'gymnastics'}
            ],
            value='swimming'
            ),
            html.H5(children='Gender'),
            dcc.Dropdown(
            id='my-dropdown-gender',
            options=[
                {'label': 'Male', 'value': 'm'},
                {'label': 'Female', 'value': 'f'}
            ],
            value='f'
            ),
            html.Button('Submit', id='button'),
            html.Div(id='container-button-basic',
                     children="Let's see how far you can go in the olympic")
            ], className = 'form')
        ], className='container2'),
    html.Div(children=[
        html.Div(style={'backgroundColor':'#transparent'}, id='medal-picture')
        ], className='container3')
], className='container')


@app.callback(
    [dash.dependencies.Output('container-button-basic', 'children'),dash.dependencies.Output('medal-picture', 'style')],
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box-height', 'value'), dash.dependencies.State('input-box-weight', 'value'), dash.dependencies.State('input-box-age', 'value'), dash.dependencies.State('my-dropdown', 'value'), dash.dependencies.State('my-dropdown-gender', 'value')])
def update_output(n_clicks, value_height, value_weight, value_age, sport, gender):
    if(value_height == None or value_weight == None or value_age == None or value_height == '' or value_weight == '' or value_age == ''):
        return "Let's see how far you can go in the olympic"
    else:
        value_height = int(value_height)
        value_weight = int(value_weight)
        value_age = int(value_age)
        result = prediction.make_prediction(value_height, value_weight, value_age,sport, gender, data.export_data)
        if result == 0:
            return 'You are unlikely to win :(', {'background':'url(./assets/sad.png)', 'backgroundSize':'cover','backgroundPosition':'center'}
        elif result == 1:
            return 'You are likely to win BRONZE', {'background':'url(./assets/bronze-medal.png)', 'backgroundSize':'cover','backgroundPosition':'center'}
        elif result == 2:
            return 'You are likely to win SILVER', {'background':'url(./assets/silver-medal.png)', 'backgroundSize':'cover','backgroundPosition':'center'}
        elif result == 3:
            return 'You are likely to win GOLD', {'background':'url(./assets/gold-medal.png)', 'backgroundSize':'cover','backgroundPosition':'center'}

if __name__ == '__main__':
    app.run_server(debug=True)