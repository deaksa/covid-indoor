import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.express as px
import indoors as ind
from indoors import Indoors

"""
main.py contains the core functionality of the Dash app. It is responsible for taking inputs,
feeding those inputs to the model (indoors.py), and displaying the model outputs in an effective, concise
manner.

Properties: 
Dash App Setup
COVID-19 Calculator Setup
Dropdown Preset Values
Tab CSS Styles
Custom HTML Headers
Main App 

Methods: 
def update_figure: Calculate model & update displayed values
def update_risk_tol_disp: Update risk tolerance display value
def update_air_frac_disp: Update air fraction display value
"""

# Dash App Setup
app = dash.Dash(__name__)
# Used for Heroku deployment
server = app.server

# COVID-19 Calculator Setup
myInd = ind.Indoors()
results_df = myInd.calc_n_max_series(2, 100, 1.0)
fig = px.line(results_df, x="Maximum Exposure Time (hours)", y="Maximum Occupancy",
              title="Occupancy vs. Exposure Time",
              height=400, color_discrete_map={"Maximum Occupancy": "#de1616"})

presets = [
    {'label': "Custom", 'value': 'custom'},
    {'label': "House", 'value': 'house'},
    {'label': "Restaurant", 'value': 'restaurant'},
    {'label': "Classroom", 'value': 'classroom'},
]

preset_settings = {
    'house': {
        'floor-area': 2000,
        'ceiling-height': 12,
        'ventilation': 3,
        'filtration': 6,
        'recirc-rate': 1,
        'exertion': 0.49,
        'exp-activity': 29,
        'masks': 0.15
    },
    'classroom': {
        'floor-area': 900,
        'ceiling-height': 12,
        'ventilation': 3,
        'filtration': 6,
        'recirc-rate': 1,
        'exertion': 0.49,
        'exp-activity': 29,
        'masks': 0.15
    },
    'restaurant': {
        'floor-area': 5000,
        'ceiling-height': 12,
        'ventilation': 9,
        'filtration': 6,
        'recirc-rate': 1,
        'exertion': 0.49,
        'exp-activity': 72,
        'masks': 1
    }
}

# Dropdown Preset Values
ventilation_default = preset_settings['classroom']['ventilation']
is_custom_vent = False
ventilation_types = [
    {'label': "Custom (see Advanced)", 'value': -1},
    {'label': "Closed windows (0.3 Outdoor ACH)", 'value': 0.3},
    {'label': "Open windows (2 Outdoor ACH)", 'value': 2},
    {'label': "Mechanical Ventilation (3 Outdoor ACH)", 'value': 3},
    {'label': "Open windows with fans (6 Outdoor ACH)", 'value': 6},
    {'label': "Mechanical Ventilation (8 Outdoor ACH)", 'value': 8},
    {'label': "Laboratory, Restaurant (9 Outdoor ACH)", 'value': 9},
    {'label': "Bar (15 Outdoor ACH)", 'value': 15},
    {'label': "Hospital (18 Outdoor ACH)", 'value': 18},
    {'label': "Toxic Laboratory (25 Outdoor ACH)", 'value': 25},
]

filter_default = preset_settings['classroom']['filtration']
is_custom_filter = False
filter_types = [
    {'label': "Custom (see Advanced)", 'value': -1},
    {'label': "None", 'value': 0},
    {'label': "Residential Window AC (MERV 1-4)", 'value': 2},
    {'label': "Residential/Commercial/Industrial (MERV 5-8)", 'value': 6},
    {'label': "Residential/Commercial/Hospital (MERV 9-12)", 'value': 10},
    {'label': "Hospital & General Surgery (MERV 13-16)", 'value': 14},
    {'label': "HEPA (MERV 17-20)", 'value': 17}
]

recirc_default = preset_settings['classroom']['recirc-rate']
is_custom_recirc = False
recirc_types = [
    {'label': "Custom (see Advanced)", 'value': -1},
    {'label': "None (0 ACH)", 'value': 0},
    {'label': "Slow (0.3 ACH)", 'value': 0.3},
    {'label': "Moderate (1 ACH)", 'value': 1},
    {'label': "Fast (10 ACH)", 'value': 10},
]

exertion_types = [
    {'label': "Resting", 'value': 0.49},
    {'label': "Standing", 'value': 0.54},
    {'label': "Light Exercise", 'value': 1.38},
    {'label': "Moderate Exercise", 'value': 2.35},
    {'label': "Heavy Exercise", 'value': 3.30},
]

expiratory_types = [
    {'label': "Breathing (nose)", 'value': 1.1},
    {'label': "Breathing (nose-nose)", 'value': 8.8},
    {'label': "Breathing (deep-fast)", 'value': 4.2},
    {'label': "Breathing (fast-deep)", 'value': 8.5},
    {'label': "Speaking (quiet speech)", 'value': 29},
    {'label': "Speaking (whispered counting)", 'value': 37},
    {'label': "Speaking (normal speech)", 'value': 72},
    {'label': "Speaking (voiced counting)", 'value': 72},
    {'label': "Speaking (loud speech)", 'value': 142},
    {'label': "Singing (whispered 'aah')", 'value': 103},
    {'label': "Singing (voiced 'aah')", 'value': 970},
]

mask_types = [
    {'label': "None (0% filtration)", 'value': 1},
    {'label': "Bandana (5% filtration)", 'value': 0.95},
    {'label': "Neck Gaiter (10% filtration)", 'value': 0.90},
    {'label': "2-layer cloth (20% filtration)", 'value': 0.80},
    {'label': "2-layer silk (30% filtration)", 'value': 0.70},
    {'label': "2-ply Batik cotton (50% filtration)", 'value': 0.50},
    {'label': "Surgical (85% filtration)", 'value': 0.15},
    {'label': "N95 Respirator (95% filtration)", 'value': 0.05},
    {'label': "2-ply cloth/MBP filter (98% filtration)", 'value': 0.02},
]

# Nmax values for main red text output
model_output_n_vals = [2, 3, 4, 5, 10, 25, 50, 100]
model_output_n_vals_big = [50, 100, 200, 300, 400, 500, 750, 1000]

# CSS Styles for Tabs (currently known issue in Dash with overriding default css)
tab_style = {
    'padding-left': '1em',
    'padding-right': '1em'
}

# Custom HTML Header
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>COVID-19 Indoor Safety</title>
        {%favicon%}
        {%css%}
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-143756813-2"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
        
          gtag('config', 'UA-143756813-2');
        </script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>'''

# Main App
app.layout = html.Div(children=[
    html.H1(children='MIT COVID-19 Indoor Safety Guideline'),
    html.Div([
        html.Div(children='''
        Kasim Khan (2020)
    '''),
        html.Div(children='''
        Martin Z. Bazant and John W. M. Bush, medRxiv preprint (2020):
        "Beyond Six Feet: A Guideline to Limit Indoor Airborne Transmission of COVID-19"
    '''),
        html.Div([
            html.A(href='http://web.mit.edu/bazant/www/COVID-19/',
                   children='''
                http://web.mit.edu/bazant/www/COVID-19/
            '''),
        ]),
        html.Div([
            html.A(href='https://github.com/kawesomekhan/covid-indoor',
                   children='''
                https://github.com/kawesomekhan/covid-indoor
            '''),
        ]),

    ], style={'font-size': '13px'}),

    html.Br(),
    html.Div(
        className='grid',
        children=[
            html.Div(
                className='card',
                children=[
                    dcc.Tabs(value='tab-1', children=[
                        dcc.Tab(
                            label='About',
                            className='custom-tab',
                            children=[
                                html.Div(className='custom-tab-container',
                                         children=[
                                             html.H6("About: "),
                                             html.Div('''
                                                    COVID-19 has been spreading in homes, restaurants, bars, classrooms, and other
                                                    enclosed spaces via tiny, infective aerosol droplets suspended in the air.
                                                    To mitigate this spread, official public health guidelines have taken the form 
                                                    of minimum social distancing rules (6 feet in the U.S.) or maximum occupancy 
                                                    (25 people in Massachusetts). 
                                                '''),
                                             html.Br(),
                                             html.Div('''
                                                    However, public health has been slow to catch up with rapidly advancing science.
                                                    Naturally, the risk of COVID-19 transmission would not only depend on physical 
                                                    distance, but also on factors such as exposure time, mask usage, and ventilation
                                                    systems, among other factors.
                                                '''),
                                             html.Br(),
                                             html.Div('''
                                                    This app uses a mathematical model, developed by MIT professors Martin Z. Bazant 
                                                    and John Bush, to improve upon
                                                    current distancing guidelines by providing a more accurate description of
                                                    indoor COVID-19 transmission risk.
                                                '''),
                                             html.Br(),
                                             html.Div('''
                                                    Adjust parameters in the other tabs and see how different spaces handle
                                                    indoor COVID-19 transmission.
                                                '''),
                                         ]),

                            ],
                            style=tab_style,
                            selected_style=tab_style
                        ),
                        dcc.Tab(
                            label='Room Specifications',
                            className='custom-tab',
                            children=[
                                html.Div(className='custom-tab-container',
                                         children=[
                                             html.H6("Room Specifications: "),
                                             html.Br(),
                                             html.Div(["Floor Area (sq. ft.): ",
                                                       dcc.Input(id='floor-area', value=900, type='number')]),
                                             html.Br(),
                                             html.Div(["Ceiling Height (ft.): ",
                                                       dcc.Input(id='ceiling-height', value=12, type='number')]),
                                             html.Br(),
                                             html.Div(className='card-dropdown',
                                                      children=[html.Div(["Ventilation System: "])]),
                                             html.Div(className='card-dropdown',
                                                      children=[dcc.Dropdown(id='ventilation-type',
                                                                             options=ventilation_types,
                                                                             value=ventilation_default,
                                                                             searchable=False,
                                                                             clearable=False)]),
                                             html.Br(),
                                             html.Div(["Filtration System: ",
                                                       dcc.Dropdown(id='filter-type',
                                                                    options=filter_types,
                                                                    value=filter_default,
                                                                    searchable=False,
                                                                    clearable=False)]),
                                             html.Br(),
                                             html.Div(["Recirculation Rate: ",
                                                       dcc.Dropdown(id='recirc-rate',
                                                                    options=recirc_types,
                                                                    value=recirc_default,
                                                                    searchable=False,
                                                                    clearable=False)]),
                                         ]),
                            ],
                            style=tab_style,
                            selected_style=tab_style
                        ),
                        dcc.Tab(
                            label='Human Behavior',
                            className='custom-tab',
                            children=[
                                html.Div(className='custom-tab-container',
                                         children=[
                                             html.H6("Human Behavior: "),
                                             html.Br(),
                                             html.Div(["Exertion Level: ",
                                                       dcc.Dropdown(id='exertion-level',
                                                                    options=exertion_types,
                                                                    value=0.49,
                                                                    searchable=False,
                                                                    clearable=False)]),
                                             html.Br(),
                                             html.Div(["Expiratory Activity: ",
                                                       dcc.Dropdown(id='exp-activity',
                                                                    options=expiratory_types,
                                                                    value=29,
                                                                    searchable=False,
                                                                    clearable=False)]),
                                             html.Br(),
                                             html.Div(["Masks? ",
                                                       dcc.Dropdown(id='mask-type',
                                                                    options=mask_types,
                                                                    value=0.15,
                                                                    searchable=False,
                                                                    clearable=False)]),
                                             html.Br(),
                                             html.Div(["Risk Tolerance: ",
                                                       html.Span(id='risk-tolerance-output'),
                                                       html.Div('''
                                                                   This represents the number of expected transmissions during the
                                                                   occupancy period. A vulnerable population, due to age or
                                                                   preexisting medical conditions, will generally require
                                                                   a lower risk tolerance. 
                                                          ''', style={'font-size': '13px', 'margin-left': '20px'}),
                                                       dcc.Slider(id='risk-tolerance',
                                                                  min=0.01,
                                                                  max=1,
                                                                  step=0.01,
                                                                  value=0.1,
                                                                  marks={
                                                                      0.01: {'label': '0.01: Contact Tracing',
                                                                             'style': {'max-width': '50px'}},
                                                                      1: {'label': '1.0: Unsafe'}
                                                                  })
                                                       ])
                                         ]),
                            ],
                            style=tab_style,
                            selected_style=tab_style
                        ),
                        dcc.Tab(
                            label='Advanced',
                            className='custom-tab',
                            children=[
                                html.Div(className='custom-tab-container',
                                         children=[
                                             html.H6("Advanced Input: "),
                                             html.Div(['''
                                                 Know your specific ACH or MERV specifications? Input them here:
                                             ''']),
                                             html.Br(),
                                             html.Div(["Ventilation System (ACH): ",
                                                       dcc.Input(id='ventilation-type-adv',
                                                                 value=ventilation_default,
                                                                 type='number')]),
                                             html.Br(),
                                             html.Div(["Filtration System (MERV): ",
                                                       dcc.Input(id='filtration-type-adv', value=filter_default,
                                                                 type='number')]),
                                             html.Br(),
                                             html.Div(["Recirculation Rate (ACH): ",
                                                       dcc.Input(id='recirc-rate-adv',
                                                                 value=recirc_default,
                                                                 type='number')]),
                                             html.Br(),
                                             html.H6("Graph Output: "),
                                             html.Div([
                                                 dcc.Graph(
                                                     id='safety-graph',
                                                     figure=fig
                                                 ),
                                             ])
                                         ]),
                            ],
                            style=tab_style,
                            selected_style=tab_style
                        )
                    ],
                             colors={
                                 "border": "#c9c9c9",
                                 "primary": "#de1616"
                             }),
                    html.Br()
                ]),
            html.Div(
                className='card',
                children=[
                    html.Div([
                        html.H6("Current room: "),
                        html.Div(
                            className='grid-preset',
                            children=[
                                html.Div(
                                    id='presets-div',
                                    children=[
                                        dcc.Dropdown(id='presets',
                                                     options=presets,
                                                     value='classroom',
                                                     searchable=False,
                                                     clearable=False),
                                    ]),
                            ], style={'max-width': '500px'}),
                        html.H3([
                            '''Based on this model, it should be safe for this room to have:
                    ''']),
                        html.H4(className='model-output-text', id='model-text-1'),
                        html.H4(className='model-output-text', id='model-text-2'),
                        html.H4(className='model-output-text', id='model-text-3'),
                        html.H4(className='model-output-text', id='model-text-4'),
                        html.H4(className='model-output-text', id='model-text-5'),
                        html.H4(className='model-output-text', id='model-text-6'),
                        html.H4(className='model-output-text', id='model-text-7'),
                        html.H4(className='model-output-text', id='model-text-8'),
                        html.Br(),
                        html.H3([
                            '''In comparison, current six feet distancing guidelines recommend no more than''',
                            html.Span(id='six-ft-output', children=''' 2 people ''', style={'color': '#de1616'}),
                            ''' in this room.''']),
                    ]),
                ], style={'padding-top': '0px'}),
        ]
    ),
])


# Model Update & Calculation
# See indoors.py def set_default_params(self) for parameter descriptions.
@app.callback(
    [Output('safety-graph', 'figure'),
     Output('model-text-1', 'children'),
     Output('model-text-2', 'children'),
     Output('model-text-3', 'children'),
     Output('model-text-4', 'children'),
     Output('model-text-5', 'children'),
     Output('model-text-6', 'children'),
     Output('model-text-7', 'children'),
     Output('model-text-8', 'children'),
     Output('six-ft-output', 'children'),
     Output('presets', 'value')],
    [Input('floor-area', 'value'),
     Input('ceiling-height', 'value'),
     Input('ventilation-type', 'value'),
     Input('recirc-rate', 'value'),
     Input('filter-type', 'value'),
     Input('exertion-level', 'value'),
     Input('exp-activity', 'value'),
     Input('mask-type', 'value'),
     Input('risk-tolerance', 'value'),
     Input('ventilation-type-adv', 'value'),
     Input('filtration-type-adv', 'value'),
     Input('recirc-rate-adv', 'value')]
)
def update_figure(floor_area, ceiling_height, air_exchange_rate, recirc_rate, merv,
                  breathing_flow_rate, infectiousness, mask_passage_prob, risk_tolerance, ach_adv, merv_adv,
                  recirc_rate_adv):
    # Make sure none of our values are none
    is_none = floor_area is None or ceiling_height is None or ach_adv is None or merv_adv is None or \
              recirc_rate_adv is None or recirc_rate is None
    if is_none:
        raise PreventUpdate

    # Check if we just moved to a preset; if not, change the preset dropdown to custom
    preset_dd_value = 'custom'
    is_preset = False
    for setting_key in preset_settings:
        setting = preset_settings[setting_key]
        is_preset = setting['floor-area'] == floor_area and \
                    setting['ceiling-height'] == ceiling_height and \
                    setting['ventilation'] == air_exchange_rate and \
                    setting['recirc-rate'] == recirc_rate and \
                    setting['filtration'] == merv and \
                    setting['exertion'] == breathing_flow_rate and \
                    setting['exp-activity'] == infectiousness and \
                    setting['masks'] == mask_passage_prob
        if is_preset:
            preset_dd_value = setting_key
            break

    # Check if any custom values are selected; if so, grab the ach from the advanced tab instead.
    if air_exchange_rate == -1:
        air_exchange_rate = ach_adv

    if merv == -1:
        merv = merv_adv

    if recirc_rate == -1:
        recirc_rate = recirc_rate_adv

    # Update model with newly-selected parameters
    aerosol_radius = 2
    aerosol_filtration_eff = Indoors.merv_to_eff(merv, aerosol_radius)

    # Convert recirc rate to outdoor air fraction
    outdoor_air_fraction = air_exchange_rate / (air_exchange_rate + recirc_rate)

    myInd.physical_params = [floor_area, ceiling_height, air_exchange_rate, outdoor_air_fraction,
                             aerosol_filtration_eff]
    myInd.physio_params = [breathing_flow_rate, aerosol_radius]
    myInd.disease_params = [infectiousness, 0.3]
    myInd.prec_params = [mask_passage_prob, risk_tolerance]
    myInd.calc_vars()

    # Update the figure with a new model calculation
    new_df = myInd.calc_n_max_series(2, 100, 1.0)
    new_fig = px.line(new_df, x="Maximum Exposure Time (hours)", y="Maximum Occupancy",
                      title="Occupancy vs. Exposure Time", height=400,
                      color_discrete_map={"Maximum Occupancy": "#de1616"})
    new_fig.update_layout(transition_duration=500)

    # Update the red text output with new model calculations
    model_output_text = ["", "", "", "", "", "", "", ""]
    index = 0

    # Check if we should use the normal n vals, or the big n vals
    n_val_series = model_output_n_vals
    if myInd.calc_max_time(model_output_n_vals[-1]) > 48:
        n_val_series = model_output_n_vals_big

    for n_val in n_val_series:
        max_time = myInd.calc_max_time(n_val)  # hours
        units = 'hours'
        if round(max_time) < 1:
            units = 'minutes'
            max_time = max_time * 60
        elif round(max_time) > 48:
            units = 'days'
            max_time = max_time / 24

        if round(max_time) == 1:
            units = units[:-1]

        base_string = '{n_val} people for {val:.0f} ' + units + ','
        model_output_text[index] = base_string.format(n_val=n_val, val=max_time)
        index += 1

    model_output_text[-2] = model_output_text[-2] + ' or'
    model_output_text[-1] = model_output_text[-1][:-1] + '.'

    six_ft_people = myInd.get_six_ft_n()
    if six_ft_people == 1:
        six_ft_text = ' {} person'.format(six_ft_people)
    else:
        six_ft_text = ' {} people'.format(six_ft_people)

    # Update all relevant display items (figure, red output text)
    return new_fig, model_output_text[0], model_output_text[1], model_output_text[2], model_output_text[3], \
           model_output_text[4], model_output_text[5], model_output_text[6], model_output_text[7], \
           six_ft_text, preset_dd_value


# Update options based on selected presets. Also, because
# multiple Outputs cannot point to the same dash core component,
# this function also handles some functionality related to
# custom ventilation and filtration inputs.
@app.callback(
    [Output('floor-area', 'value'),
     Output('ceiling-height', 'value'),
     Output('ventilation-type', 'value'),
     Output('recirc-rate', 'value'),
     Output('filter-type', 'value'),
     Output('exertion-level', 'value'),
     Output('exp-activity', 'value'),
     Output('mask-type', 'value')],
    [Input('presets', 'value'),
     Input('ventilation-type-adv', 'value'),
     Input('filtration-type-adv', 'value'),
     Input('recirc-rate-adv', 'value')]
)
def update_presets(preset, air_exchange_rate, merv, recirc_rate):
    ctx = dash.callback_context
    if ctx.triggered:
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'presets':
            # Update the room and behavior options based on the selected preset
            if preset == 'custom':
                raise PreventUpdate
            else:
                curr_settings = preset_settings[preset]
                return curr_settings['floor-area'], curr_settings['ceiling-height'], curr_settings['ventilation'], \
                       curr_settings['recirc-rate'], curr_settings['filtration'], curr_settings['exertion'], \
                       curr_settings['exp-activity'], curr_settings['masks']
        elif triggered_id == 'ventilation-type-adv':
            # Update ventilation dropdown if set to a custom or preset value
            for vent_type in ventilation_types:
                if vent_type['value'] == air_exchange_rate:
                    return dash.no_update, dash.no_update, air_exchange_rate, dash.no_update, dash.no_update, \
                           dash.no_update, dash.no_update, dash.no_update

            return dash.no_update, dash.no_update, -1, dash.no_update, dash.no_update, \
                   dash.no_update, dash.no_update, dash.no_update
        elif triggered_id == 'filtration-type-adv':
            # Update filtration dropdown if set to a custom value
            for filter_type in filter_types:
                if filter_type['value'] == merv:
                    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, merv, \
                           dash.no_update, dash.no_update, dash.no_update

            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, -1, \
                   dash.no_update, dash.no_update, dash.no_update
        elif triggered_id == 'recirc-rate-adv':
            # Update filtration dropdown if set to a custom value
            for recirc_type in recirc_types:
                if recirc_type['value'] == recirc_rate:
                    return dash.no_update, dash.no_update, dash.no_update, recirc_rate, dash.no_update, \
                           dash.no_update, dash.no_update, dash.no_update

            return dash.no_update, dash.no_update, dash.no_update, recirc_rate, dash.no_update, \
                   dash.no_update, dash.no_update, dash.no_update

    raise PreventUpdate


# Update Advanced ventilation setting based on dropdown selection.
# If the custom preset is selected, update the custom value to the default.
@app.callback(
    Output('ventilation-type-adv', 'value'),
    Input('ventilation-type', 'value')
)
def update_adv_ventilation_fwd(air_exchange_rate):
    global is_custom_vent
    if air_exchange_rate == -1:
        is_custom_vent = True
        raise PreventUpdate
    else:
        is_custom_vent = False
        return air_exchange_rate


# Update Advanced filtration setting based on dropdown selection.
# If the custom preset is selected, update the custom value to the default.
@app.callback(
    Output('filtration-type-adv', 'value'),
    Input('filter-type', 'value')
)
def update_adv_filtration_fwd(merv):
    global is_custom_filter
    if merv == -1:
        is_custom_filter = True
        raise PreventUpdate
    else:
        is_custom_filter = False
        return merv


# Update Advanced recirculation rate setting based on dropdown selection.
# If the custom preset is selected, update the custom value to the default.
@app.callback(
    Output('recirc-rate-adv', 'value'),
    Input('recirc-rate', 'value')
)
def update_adv_recirc_fwd(recirc_rate):
    global is_custom_recirc
    if recirc_rate == -1:
        is_custom_recirc = True
        raise PreventUpdate
    else:
        is_custom_recirc = False
        return recirc_rate


# Risk tolerance slider value display
@app.callback(
    [Output('risk-tolerance-output', 'children')],
    [Input('risk-tolerance', 'value')]
)
def update_risk_tol_disp(risk_tolerance):
    return ["{:.2f}".format(risk_tolerance)]


if __name__ == "__main__":
    app.run_server(debug=True)
