'''
    dcc.Graph(
        id='fig1',
        figure=fig_sv_sex
    ),

    html.H5(children='Data',
            style={'textAlign': 'left',
                   'color': style.colors['text']}),

    generate_table(df)'''